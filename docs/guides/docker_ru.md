1|# Докер
2|
3|## Команды разработки
4|Используйте файл dev Compose для локальной базы данных/Redis.
5|```баш
6|docker compose -f docker-compose.dev.yml up -d
7|docker compose -f docker-compose.dev.yml logs -f
8|docker compose -f docker-compose.dev.yml вниз
9|```
10|
11|## Производственные команды
12|Используйте оболочки Makefile для основного файла компоновки.
13|```баш
14|сделать сборку докеров
15|сделать докер
16|сделать докер-логи SERVICE=bot
17|```
18|
19|## Полезные команды
20|Быстрые помощники для обычных проверок докера.
21|```баш
22|докер составить PS
23|docker составить журналы -f --tail=200
24|docker compose exec db psql -U $DB__USER -d $DB__NAME
25|```
26|