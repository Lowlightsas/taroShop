# taroShop
taroShop

![bandicam 2024-10-30 18-25-59-828](https://github.com/user-attachments/assets/fa5dddf6-1439-4b11-a0ec-858690faeaac)

<div align="center">
  <img src="https://github.com/user-attachments/assets/9d9c0391-dee9-4046-b8c8-ed1f7e881f50" width="300" />
  <img src="https://github.com/user-attachments/assets/32d1baff-255e-44ae-97c2-5369bbcb8999" width="300" />
  <img src="https://github.com/user-attachments/assets/d586e734-b3fa-49f5-8141-7adadc97e723" width="300" />
  <img src="https://github.com/user-attachments/assets/e0eb5662-e325-4451-831a-8f11d48eb9ac" width="300" />
  <img src="https://github.com/user-attachments/assets/27b0a7c0-040e-4e5d-9e7f-7aa6baf66c1d" width="300" />
  <img src="https://github.com/user-attachments/assets/784114d9-994a-424e-9d4c-cac1c28e5122" width="300" />
  <img src="https://github.com/user-attachments/assets/96082a89-4aeb-4fef-adc0-68d680c6e8e4" width="300" />
  <img src="https://github.com/user-attachments/assets/6b39b364-ef8a-46a3-92f7-320912bcd423" width="300" />
  <img src="https://github.com/user-attachments/assets/e762047d-c02e-4a46-b5e4-bb09d9120298" width="300" />
  <img src="https://github.com/user-attachments/assets/b0506e23-6671-442b-98ae-562fa61384ef" width="300" />
</div>

### 1. Убедитесь, что RabbitMQ установлен и запущен


После установки RabbitMQ запустите его:

```bash
# Для Windows
rabbitmq-server

# Для Linux (если установлен через apt)
sudo systemctl start rabbitmq-server
```

Вы можете проверить, что RabbitMQ работает, открыв веб-интерфейс по адресу `http://localhost:15672`. Войдите, используя учетные данные по умолчанию: `guest` / `guest`.

### 2. Запустите сервер Django

Перейдите в корневую директорию вашего Django проекта и выполните команду:

```bash
python manage.py runserver
```

Это запустит сервер на `http://127.0.0.1:8000` (по умолчанию).

### 3. Запустите Celery worker

Откройте новый терминал и перейдите в директорию вашего проекта, затем запустите Celery worker:

```bash
celery -A myshop worker --loglevel=info
```

Замените `myshop` на имя вашего приложения, если оно другое. Это запустит Celery и подключит его к RabbitMQ.

### 4. Проверка

Теперь у вас должны работать три компонента:

- **Django сервер** на `http://127.0.0.1:8000`.
- **Celery worker**, который будет обрабатывать фоновые задачи.
- **RabbitMQ**, который будет использоваться как брокер сообщений.
