# Деплой на Hetzner Cloud — `infra/hetzner`

Эта директория содержит Terraform-конфигурацию для поднятия VM в Hetzner Cloud
и настроенный CI/CD (GitHub Actions), который выкатывает приложение на этот сервер.

Что поднимается на сервере через `docker-compose.yml` из корня репозитория:
`postgres` + `migrations` (alembic) + `app` (FastAPI/uvicorn) + `nginx` + `certbot`.

- **Тип сервера (по умолчанию):** `cpx22` (2 vCPU, 4 GB RAM, AMD/x86) — с запасом под postgres + app + nginx
- **Локация (по умолчанию):** `nbg1` (Nuremberg). `cpx22` доступен в `nbg1` / `hel1` / `sin`.
  ⚠️ Набор типов зависит от локации и аккаунта. Если получишь `server type ... not found`
  или `... is unavailable in ...`, посмотри доступные пары так:
  ```bash
  curl -s -H "Authorization: Bearer $HETZNER_TOKEN" \
    'https://api.hetzner.cloud/v1/datacenters?per_page=100'
  ```
  и подставь подходящий тип через `-var="server_type=..."` или `-var="location=..."`.
- **ОС:** Ubuntu 24.04, Docker + docker compose ставятся автоматически через `cloud-init`

## Файлы

| Файл | Назначение |
|------|-----------|
| `provider.tf` | Провайдер Hetzner (`hetznercloud/hcloud` ~> 1.68) |
| `variables.tf` | Переменные (тип сервера, ключи, firewall и т.д.) |
| `main.tf` | Ресурсы: SSH-ключ, сервер, firewall |
| `cloud-init.tpl` | Первичная настройка сервера: пользователь `deploy`, Docker, git, rsync |
| `outputs.tf` | Выводит IP, id сервера и готовую SSH-команду |
| `terraform.tfvars.example` | Пример переменных (скопировать в `terraform.tfvars`) |
| `.gitignore` | Игнорирует `*.tfstate`, `terraform.tfvars`, `.terraform` |

Рабочий CI/CD лежит в `.github/workflows/deploy-hetzner.yml` (в корне репозитория).

> В репозитории также остался AWS-вариант (`terraform/` + `.github/workflows/deploy.yml`).
> Он переведён в режим «только вручную» (`workflow_dispatch`), чтобы два пайплайна
> не деплоили одновременно на push в `main`.

---

## Шаг 0. Получить Hetzner API Token

1. Войдите в [Hetzner Cloud Console](https://console.hetzner.cloud)
2. Выберите проект (или создайте новый)
3. **Security → API Tokens → Generate API Token** (права **Read & Write**)
4. Дайте имя (например `autopro-terraform`) и скопируйте токен — **показывается один раз!**
5. ⚠️ **Никогда не коммитьте токен в репозиторий.**

## Шаг 1. SSH-ключ

Нужен для доступа Terraform/CI к серверу. Если ключа нет:

```bash
ssh-keygen -t ed25519 -C "autopro-deploy" -f ~/.ssh/autopro_ed25519
```

- Публичный ключ (`~/.ssh/autopro_ed25519.pub`) → передаётся в Terraform (`ssh_public_key`).
- Приватный ключ (`~/.ssh/autopro_ed25519`) → в GitHub Secret `SSH_PRIVATE_KEY`.

## Шаг 2. Поднять сервер (Terraform)

```bash
cd infra/hetzner
terraform init
```

Дальше — один из двух способов передать переменные.

**Способ A — переменные окружения (для разработки):**
```bash
export HETZNER_TOKEN="ваш_токен"

terraform plan \
  -var="hcloud_token=$HETZNER_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/autopro_ed25519.pub)"

terraform apply -auto-approve \
  -var="hcloud_token=$HETZNER_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/autopro_ed25519.pub)"
```

**Способ B — `terraform.tfvars` (не коммитится, в `.gitignore`):**
```bash
cp terraform.tfvars.example terraform.tfvars
# впишите hcloud_token и ssh_public_key в terraform.tfvars
terraform plan
terraform apply -auto-approve
```

Получить IP сервера:
```bash
terraform output server_ipv4_address
```

Проверить SSH-доступ (пользователь `deploy` создаётся автоматически):
```bash
ssh -i ~/.ssh/autopro_ed25519 deploy@$(terraform output -raw server_ipv4_address)
```

> Docker ставится через cloud-init в фоне — после `apply` дайте серверу
> ~1-2 минуты. Признак готовности: `test -f /tmp/hetzner-provisioned`.

Удалить всю инфраструктуру:
```bash
terraform destroy -auto-approve \
  -var="hcloud_token=$HETZNER_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/autopro_ed25519.pub)"
```

## Шаг 3. Настроить GitHub Secrets

Repository → **Settings → Secrets and variables → Actions → New repository secret**
(или через `gh` CLI):

| Secret | Что положить |
|--------|--------------|
| `SSH_PRIVATE_KEY` | Содержимое приватного ключа `~/.ssh/autopro_ed25519` (целиком, с `-----BEGIN...`) |
| `HETZNER_HOST` | IPv4 сервера из `terraform output server_ipv4_address` |
| `ENV_FILE` | Полное содержимое рабочего `.env` (см. `.env.template` в корне) |

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/autopro_ed25519
gh secret set HETZNER_HOST --body "$(cd infra/hetzner && terraform output -raw server_ipv4_address)"
gh secret set ENV_FILE < .env
```

## Шаг 4. Деплой (CI/CD)

Workflow `.github/workflows/deploy-hetzner.yml` запускается:
- автоматически на `push` в ветку `main`;
- вручную — вкладка **Actions → CI / Deploy to Hetzner → Run workflow**.

Что делает workflow:
1. **test** — ставит зависимости через Poetry (`poetry install --with dev`, группа
   `dev` помечена `optional = true`, поэтому флаг обязателен), гоняет
   `ruff check` и `ruff format --check`, затем `pytest` (если есть директория с тестами).
2. **deploy** — по SSH:
   - `rsync` кода проекта в `/home/deploy/app` (исключая `.git`, `.github`, `infra`,
     `terraform`, `tutorials`, локальный `.env` и кэши);
   - записывает `.env` из секрета `ENV_FILE`;
   - `docker compose up -d --build` + `docker compose restart nginx` + `docker image prune -f`;
   - `docker compose ps` для проверки.

## Шаг 5. HTTPS (certbot) — первый запуск

В `docker-compose.yml` есть сервисы `nginx` и `certbot`.

⚠️ **Важно:** `nginx/prod/default.conf` монтируется как обычный файл
(`./nginx/prod/default.conf:/etc/nginx/conf.d/default.conf:ro`), а в нём стоит
плейсхолдер `${DOMAIN_NAME}`. Nginx **не** подставляет переменные окружения в
`conf.d/*.conf` — подставьте свой домен в файл руками (или переведите монтирование
на механизм шаблонов `/etc/nginx/templates/*.conf.template`, который nginx
раскрывает через `envsubst`).

Наведите A-запись домена на IP сервера, затем на сервере получите сертификат один раз:

```bash
ssh -i ~/.ssh/autopro_ed25519 deploy@<IP>
cd /home/deploy/app
docker compose run --rm certbot certonly --webroot -w /var/www/certbot -d ваш-домен
docker compose restart nginx
```

Продление идёт автоматически (сервис `certbot` в compose крутит `certbot renew`).

---

## 🔒 Безопасность токена

- ❌ **Никогда** не коммитьте токен/приватный ключ в Git, не вставляйте в документацию/скриншоты/Slack.
- ✅ Для CI/CD — только GitHub Secrets; для локальной работы — переменные окружения или `terraform.tfvars` (в `.gitignore`).
- ✅ Отдельные токены под разные проекты; ротация при компрометации.

**Если токен скомпрометирован:** Hetzner Console → Security → API Tokens →
удалить старый → создать новый → обновить секрет/переменную → проверить логи доступа.
