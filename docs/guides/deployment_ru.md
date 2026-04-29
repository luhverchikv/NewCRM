1|# Развертывание
2|
3|## Создание Docker
4|Используйте docker-compose.yml для бота + db + redis.
5|```баш
6|докер составить -d
7|docker составить журналы -f bot
8|докер завершить работу
9|```
10|
11|## Системный сервис
12|Минимальная сервисная единица для веб-перехватчика или опроса.
13|```ини
14|[Единица]
15|Description=Бот айограммы
16|После=network.target
17|
18|[Сервис]
19|WorkingDirectory=/opt/aiogram-bot-template
20|EnvironmentFile=/opt/aiogram-bot-template/.env
21|ExecStart=/usr/bin/uv запустить источник Python/__main__.py
22|Перезапустить=всегда
23|
24|[Установить]
25|WantedBy=multi-user.target
26|```
27|
28|## Контрольный список перед производством
29|- Установите `ENVIRONMENT=production` в `.env`.
30|- Установите `TG__WEBHOOK_USE=True` и `WEBHOOK__*` для режима веб-перехватчика.
31|- Запустите миграцию: `uv run alembic update head`.
32|- Проверьте подключение к БД/Redis и токен бота.
33|