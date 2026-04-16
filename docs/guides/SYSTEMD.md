# Автозапуск Telegram-бота через systemd

> Полное руководство по настройке автоматического запуска и управления Telegram-ботом на базе Aiogram с использованием systemd в Linux.

![systemd](https://img.shields.io/badge/systemd-внедрение-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Aiogram](https://img.shields.io/badge/Aiogram-Telegram%20Bot-orange)

## Содержание

- [Описание](#описание)
- [Создание systemd-сервиса](#создание-systemd-сервиса)
- [Управление сервисом](#управление-сервисом)
- [Просмотр логов](#просмотр-логов)
- [Автоматическое обновление бота](#автоматическое-обновление-бота)
- [Настройка sudo без пароля](#настройка-sudo-без-пароля)
- [Возможные проблемы и решения](#возможные-проблемы-и-решения)

## Описание

Данное руководство поможет вам настроить автоматический запуск Telegram-бота при старте системы, его автоматический перезапуск при сбоях, а также удобное управление через консоль.

### Преимущества данного подхода

- **Автозапуск** — бот запускается автоматически при загрузке системы
- **Автовосстановление** — при краше бот автоматически перезапускается
- **Удобное управление** — стандартные команды systemctl для управления
- **Логирование** — централизованный доступ к логам через journalctl

## Создание systemd-сервиса

### Шаг 1: Создайте файл сервиса

```bash
sudo nano /etc/systemd/system/newcrm_bot.service
```

### Шаг 2: Внесите конфигурацию

```ini
[Unit]
Description=Aiogram Telegram Bot
After=network.target

[Service]
Type=simple
User=vitali_lukhverchyk
WorkingDirectory=/home/vitali_lukhverchyk/aiogram-bot-template
EnvironmentFile=/home/vitali_lukhverchyk/aiogram-bot-template/.env
ExecStart=/home/vitali_lukhverchyk/.local/bin/uv run python source/__main__.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Параметры конфигурации

| Параметр           | Описание                                        | Пример                            |
| ------------------ | ----------------------------------------------- | --------------------------------- |
| `Description`      | Описание сервиса                                | `Aiogram Telegram Bot`            |
| `User`             | Пользователь, от имени которого запускается бот | `vitali_lukhverchyk`              |
| `WorkingDirectory` | Директория проекта                              | `/home/user/aiogram-bot-template` |
| `EnvironmentFile`  | Путь к файлу с переменными окружения            | `.env`                            |
| `ExecStart`        | Команда запуска                                 | `/usr/bin/python3 bot.py`         |
| `Restart`          | Политика перезапуска                            | `always`, `on-failure`, `no`      |
| `RestartSec`       | Задержка перед перезапуском (секунды)           | `10`                              |

### Пояснения к ключевым параметрам

- **`User=`** — укажите ваш логин в системе
- **`WorkingDirectory=`** — полный путь к директории проекта
- **`ExecStart=`** — команда запуска бота (можно использовать `python3 -m logic.main`, если у вас модульная структура)
- **`Restart=always`** — бот будет автоматически перезапускаться при любом завершении

## Управление сервисом

### Активация и запуск

```bash
# Перезагрузить конфигурацию systemd
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

# Включить автозапуск при загрузке системы
sudo systemctl enable newcrm_bot.service

# Запустить сервис
sudo systemctl start newcrm_bot.service
```

### Основные команды управления

```bash
# Проверить статус бота
sudo systemctl status newcrm_bot.service

# Остановить бота
sudo systemctl stop newcrm_bot.service

# Перезапустить бота
sudo systemctl restart newcrm_bot.service

# Отключить автозапуск
sudo systemctl disable newcrm_bot.service
```

### Статусы сервиса

| Статус | Значение |
|--------|----------|
| `active (running)` | Бот успешно работает |
| `active (exited)` | Бот завершил работу (для one-shot сервисов) |
| `inactive (dead)` | Бот остановлен |
| `failed` | Произошла ошибка при запуске |

## Просмотр логов

### Основные команды

```bash
# Следить за логами в реальном времени
journalctl -u newcrm_bot.service -f

# Последние 100 строк лога
journalctl -u newcrm_bot.service -n 100

# Логи за сегодня
journalctl -u newcrm_bot.service --since today

# Логи за последний час
journalctl -u newcrm_bot.service --since "1 hour ago"

# Очистить старые логи (оставить последние 500 МБ)
sudo journalctl --vacuum-size=500M
```

### Фильтрация логов

```bash
# Найти ошибки
journalctl -u newcrm_bot.service -p err

# Найти предупреждения
journalctl -u newcrm_bot.service -p warning

# Поиск по ключевому слову
journalctl -u newcrm_bot.service | grep "ERROR"
```

## Автоматическое обновление бота

Создайте скрипт для удобного обновления бота из Git-репозитория.

### Создание скрипта

```bash
nano ~/update_newcrm_bot.sh
```

### Содержимое скрипта

```bash
#!/bin/bash

# Директория проекта
PROJECT_DIR="$HOME/aiogram-bot-template"

# Переходим в директорию проекта
cd "$PROJECT_DIR" || exit 1

# Выводим информацию
echo "=== Обновление бота ==="
echo "Время: $(date)"
echo "Директория: $PROJECT_DIR"
echo ""

# Получаем последние изменения из Git
echo ">> Выполняется git pull..."
git pull

# Перезапускаем сервис
echo ">> Перезапуск сервиса..."
sudo systemctl restart newcrm_bot.service

# Проверяем статус
echo ""
echo ">> Статус сервиса:"
sudo systemctl status newcrm_bot.service --no-pager

echo ""
echo "=== Обновление завершено ==="
```

### Сделайте скрипт исполняемым

```bash
chmod +x ~/update_newcrm_bot.sh
```

### Использование

```bash
# Обновить бота одной командой
./update_newcrm_bot.sh
```

## Настройка sudo без пароля

Для работы скрипта обновления без ввода пароля настройте соответствующие права.

### Редактирование sudoers

> **Внимание:** всегда используйте `visudo` для редактирования, так как он проверяет синтаксис файла!

```bash
sudo visudo /etc/sudoers
```

### Добавление строки

Добавьте в конец файла следующую строку (замените `vitali_lukhverchyk` на ваш логин):

```sudoers
vitali_lukhverchyk ALL=(ALL) NOPASSWD: /bin/systemctl restart newcrm_bot.service
```

### Проверка

```bash
# Теперь эта команда выполнится без запроса пароля
sudo systemctl restart newcrm_bot.service
```

## Возможные проблемы и решения

### Проблема: Permission denied

```
Failed to start newcrm_bot.service: Permission denied
```

**Решение:**

```bash
# Проверьте права на файл .env
ls -la /home/vitali_lukhverchyk/aiogram-bot-template/.env

# Установите правильные права (только владелец может читать)
chmod 600 /home/vitali_lukhverchyk/aiogram-bot-template/.env
```

### Проблема: WorkingDirectory не существует

```
Failed to start newcrm_bot.service: WorkingDirectory doesn't exist
```

**Решение:** Убедитесь, что путь `WorkingDirectory` существует и пользователь имеет доступ к нему.

### Проблема: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'aiogram'
```

**Решение:**

```bash
# Убедитесь, что используете правильную команду запуска
# Используйте виртуальное окружение или uv:
ExecStart=/home/vitali_lukhverchyk/.local/bin/uv run python source/__main__.py

# Или активируйте виртуальное окружение:
ExecStart=/home/vitali_lukhverchyk/venv/bin/python source/__main__.py
```

### Проблема: Бот не перезапускается автоматически

**Решение:** Проверьте параметр `Restart`:

```ini
Restart=always          # Перезапускать всегда
Restart=on-failure      # Перезапускать только при ошибках
Restart=no              # Не перезапускать
```

## Структура файлов

```
/etc/systemd/system/
└── newcrm_bot.service    # Файл сервиса systemd

$HOME/
├── aiogram-bot-template/  # Директория проекта бота
│   ├── .env               # Переменные окружения
│   └── source/            # Исходный код
└── update_newcrm_bot.sh   # Скрипт обновления (опционально)
```

## Дополнительные команды

```bash
# Посмотреть зависимости сервиса
systemctl list-dependencies newcrm_bot.service

# Маскировать сервис (предотвратить запуск)
sudo systemctl mask newcrm_bot.service

# Размаскировать сервис
sudo systemctl unmask newcrm_bot.service

# Список всех сервисов
systemctl list-units --type=service --state=running | grep bot
```

---

**Автор:** Документация создана на основе best practices systemd для Python-приложений.

**Лицензия:** MIT
