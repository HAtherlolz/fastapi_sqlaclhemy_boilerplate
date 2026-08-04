# 🚀 Деплой на AWS EC2 с помощью Terraform

Пошаговая инструкция по поднятию EC2-инстанса для проекта.

> ℹ️ **Это альтернативный (AWS) путь**, конфигурация лежит в `terraform/`.
> Основной деплой проекта — Hetzner Cloud (`infra/hetzner/`):
> см. [hetzner-setup.md](hetzner-setup.md).

---

## Предварительные требования

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- Аккаунт AWS с правами на создание EC2, Security Groups, Elastic IP
- SSH-ключ (Key Pair) в AWS

---

## Шаг 1. Настройка AWS CLI

```bash
aws configure
```

Введите ваш `AWS Access Key ID`, `Secret Access Key`, регион (например `eu-central-1`) и формат `json`.

---

## Шаг 2. Создание SSH Key Pair (если ещё нет)

```bash
aws ec2 create-key-pair \
  --key-name my-aws-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/my-aws-key.pem

chmod 400 ~/.ssh/my-aws-key.pem
```

---

## Шаг 3. Настройка переменных Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Отредактируйте `terraform.tfvars`:

```hcl
aws_region       = "eu-central-1"
instance_type    = "t3.small"        # или t3.micro для Free Tier
key_name         = "my-aws-key"      # имя вашего ключа из шага 2
project_name     = "fastapi-boilerplate"
allowed_ssh_cidr = "YOUR_IP/32"      # ваш IP для SSH доступа
root_volume_size = 20
```

> 💡 Узнать свой IP: `curl ifconfig.me`

---

## Шаг 4. Инициализация и запуск Terraform

```bash
# Инициализация (скачивание провайдеров)
terraform init

# Просмотр плана — что будет создано
terraform plan

# Применение — создание ресурсов
terraform apply
```

Введите `yes` для подтверждения. После завершения вы увидите:

```
Outputs:

public_ip    = "3.120.xxx.xxx"
ssh_command  = "ssh -i ~/.ssh/my-aws-key.pem ubuntu@3.120.xxx.xxx"
```

---

## Шаг 5. Подключение к серверу

```bash
ssh -i ~/.ssh/my-aws-key.pem ubuntu@<PUBLIC_IP>
```

Подождите 1–2 минуты после создания — `user_data` скрипт устанавливает Docker.

Проверьте что Docker установлен:

```bash
docker --version
docker compose version
```

---

## Шаг 6. Деплой приложения на сервер

```bash
# На локальной машине — копируем проект на сервер
scp -i ~/.ssh/my-aws-key.pem -r \
  ./ ubuntu@<PUBLIC_IP>:~/app

# На сервере
ssh -i ~/.ssh/my-aws-key.pem ubuntu@<PUBLIC_IP>
cd ~/app

# Создаём .env файл
cp .env.example .env   # или создайте вручную
nano .env
```

---

## Шаг 7. Запуск приложения

```bash
# Сборка и запуск
docker compose up -d --build

# Проверка статуса
docker compose ps

# Логи
docker compose logs -f app
```

---

## Шаг 8. Получение SSL-сертификата

Перед этим убедитесь, что DNS вашего домена указывает на `PUBLIC_IP` сервера.

```bash
# Получение сертификата
docker compose run --rm certbot certonly \
  --webroot -w /var/www/certbot \
  -d your-domain.com

# Перезапуск nginx для подхвата сертификата
docker compose restart nginx
```

---

## Управление инфраструктурой

```bash
# Посмотреть текущее состояние
terraform show

# Уничтожить все ресурсы
terraform destroy
```

---

## Открытые порты

| Порт | Протокол | Назначение |
|------|----------|------------|
| 22   | TCP      | SSH (ограничен вашим IP) |
| 80   | TCP      | HTTP (редирект на HTTPS) |
| 443  | TCP      | HTTPS (Nginx → App) |

---

## ⚠️ Важно

- **Никогда не коммитьте** `terraform.tfvars` и `.env` в git
- Ограничьте SSH-доступ своим IP через `allowed_ssh_cidr`
- Для продакшена рассмотрите использование RDS вместо PostgreSQL в Docker
- Регулярно обновляйте SSL: certbot в docker-compose делает это автоматически каждые 12 часов
