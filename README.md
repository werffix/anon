# Анонимные сообщения — Telegram Bot

Бот для получения анонимных сообщений через персональные ссылки Telegram.

## Инструкция по запуску

### 1. Создание бота через BotFather

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram.
2. Отправьте команду `/newbot` и следуйте инструкциям.
3. После создания вы получите **BOT_TOKEN** — сохраните его.

### 2. Получение своего Telegram ID

Напишите [@userinfobot](https://t.me/userinfobot) — он покажет ваш Telegram ID.

### 3. Заполнение `.env`

Скопируйте файл `.env.example` в `.env` (или отредактируйте существующий):

```
BOT_TOKEN=ваш_токен_бота
LOG_RECEIVER_ID=ваш_telegram_id
```

### 4. Сборка и запуск контейнера

```bash
docker compose up -d --build
```

### 5. Просмотр логов

```bash
docker compose logs -f
```

### 6. Остановка бота

```bash
docker compose down
```
