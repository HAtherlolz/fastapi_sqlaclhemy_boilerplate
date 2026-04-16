# 🚀 CI/CD: GitHub Actions → AWS EC2

Инструкция по настройке автоматического деплоя через GitHub Actions.

---

## Как это работает

1. Пуш в ветку `main` → запускается workflow
2. **Job `test`** — линтинг (ruff) и тесты (pytest)
3. **Job `deploy`** — подключение к EC2 по SSH, pull кода, пересборка контейнеров

---

## Настройка

### Шаг 1. Добавьте секреты в GitHub

Перейдите в **Settings → Secrets and variables → Actions → New repository secret** и добавьте:

| Секрет | Описание |
|--------|----------|
| `EC2_HOST` | Elastic IP вашего EC2 (например `3.120.45.67`) |
| `EC2_SSH_KEY` | Содержимое приватного SSH-ключа (`cat ~/.ssh/my-aws-key.pem`) |
| `ENV_FILE` | Полное содержимое вашего `.env` файла |

### Шаг 2. Настройте Git на EC2

На сервере нужно настроить доступ к репозиторию. Если репозиторий **публичный** — ничего не нужно. Если **приватный**:

```bash
ssh -i ~/.ssh/my-aws-key.pem ubuntu@<EC2_HOST>

# Сгенерируйте deploy key
ssh-keygen -t ed25519 -C "deploy" -f ~/.ssh/github_deploy -N ""
cat ~/.ssh/github_deploy.pub
```

Добавьте публичный ключ в **GitHub → Settings → Deploy keys**.

Настройте SSH на сервере:

```bash
cat >> ~/.ssh/config << 'EOF'
Host github.com
  IdentityFile ~/.ssh/github_deploy
  StrictHostKeyChecking no
EOF
```

### Шаг 3. Первый деплой

Первый раз можно запустить вручную:

1. Перейдите в **Actions → Deploy to AWS EC2 → Run workflow**
2. Или просто сделайте пуш в `main`

### Шаг 4. Проверка

```bash
# На сервере
ssh -i ~/.ssh/my-aws-key.pem ubuntu@<EC2_HOST>
cd ~/app
docker compose ps
docker compose logs -f app
```

---

## Структура секрета `ENV_FILE`

Вставьте содержимое `.env` как есть:

```
PROJECT_NAME=MyProject
DB_USERNAME=postgres
DB_PASSWORD=supersecret
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=mydb
SECRET_KEY=your-jwt-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENV=prod
```

---

## Ручной запуск

Workflow поддерживает `workflow_dispatch` — можно запускать вручную из вкладки Actions в GitHub.

---

## ⚠️ Важно

- SSH-ключ в секрете должен быть **полным** (включая `-----BEGIN/END-----`)
- Порт 22 в Security Group должен быть открыт для IP GitHub Actions (или `0.0.0.0/0`)
- При первом деплое убедитесь что Docker установлен (Terraform user_data делает это автоматически)

