# 🚀 Деплой на Hetzner Cloud (Terraform + GitHub Actions)

Основной путь деплоя проекта. Terraform-конфигурация лежит в
[`infra/hetzner/`](../infra/hetzner/), CI/CD — в
`.github/workflows/deploy-hetzner.yml`.

Подробное описание всех файлов и шагов — в
[`infra/hetzner/README.md`](../infra/hetzner/README.md). Здесь — короткий чеклист.

---

## Что где лежит

| Путь | Что это |
|------|---------|
| `infra/hetzner/` | Terraform для Hetzner Cloud (сервер + firewall + SSH-ключ) |
| `.github/workflows/deploy-hetzner.yml` | CI/CD: lint + test, затем rsync + `docker compose up` по SSH |
| `terraform/` | Старый AWS/EC2 вариант (оставлен, см. [terraform-setup.md](terraform-setup.md)) |
| `.github/workflows/deploy.yml` | Старый AWS деплой — переведён в режим «только вручную» |

---

## Предварительные требования

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.3
- Аккаунт [Hetzner Cloud](https://console.hetzner.cloud) и API-токен (Read & Write)
- SSH-ключ (`ed25519`)
- `gh` CLI (опционально, для установки секретов)

---

## Чеклист

### 1. Токен и SSH-ключ

```bash
# токен: Hetzner Console → Security → API Tokens → Generate API Token
export HETZNER_TOKEN="ваш_токен"

ssh-keygen -t ed25519 -C "autopro-deploy" -f ~/.ssh/autopro_ed25519
```

### 2. Поднять сервер

```bash
cd infra/hetzner
terraform init

terraform apply -auto-approve \
  -var="hcloud_token=$HETZNER_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/autopro_ed25519.pub)"

terraform output server_ipv4_address
```

Сервер: Ubuntu 24.04, `cpx22` (2 vCPU / 4 GB), локация `nbg1`. Docker и
docker compose ставятся автоматически через `cloud-init` — дайте ~1–2 минуты.
Готовность:

```bash
ssh -i ~/.ssh/autopro_ed25519 deploy@<IP> "test -f /tmp/hetzner-provisioned && echo ready"
```

### 3. Секреты GitHub

```bash
gh secret set SSH_PRIVATE_KEY < ~/.ssh/autopro_ed25519
gh secret set HETZNER_HOST --body "$(cd infra/hetzner && terraform output -raw server_ipv4_address)"
gh secret set ENV_FILE < .env
```

| Secret | Значение |
|--------|----------|
| `SSH_PRIVATE_KEY` | приватный ключ целиком |
| `HETZNER_HOST` | IPv4 сервера |
| `ENV_FILE` | содержимое рабочего `.env` |

### 4. Задеплоить

Пуш в `main` — или **Actions → CI / Deploy to Hetzner → Run workflow**.

Проверка на сервере:

```bash
ssh -i ~/.ssh/autopro_ed25519 deploy@<IP>
cd /home/deploy/app && docker compose ps
```

### 5. HTTPS

Перед первым запуском подставьте домен в `nginx/prod/default.conf` вместо
плейсхолдера `${DOMAIN_NAME}` (nginx не раскрывает переменные окружения в
`conf.d/*.conf`), наведите A-запись на IP и получите сертификат:

```bash
docker compose run --rm certbot certonly --webroot -w /var/www/certbot -d ваш-домен
docker compose restart nginx
```

---

## Удалить инфраструктуру

```bash
cd infra/hetzner
terraform destroy -auto-approve \
  -var="hcloud_token=$HETZNER_TOKEN" \
  -var="ssh_public_key=$(cat ~/.ssh/autopro_ed25519.pub)"
```

---

## 🔒 Безопасность

- Токен и приватный ключ — **только** в GitHub Secrets / переменных окружения / `terraform.tfvars` (в `.gitignore`).
- `*.tfstate` содержит чувствительные данные и не коммитится (см. `.gitignore`).
- При компрометации: Hetzner Console → Security → API Tokens → удалить старый, создать новый, обновить секрет.
