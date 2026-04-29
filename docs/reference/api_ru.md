1|# Справочник по API
2|
3|## Пользовательский сервис
4|Использовать службу в обработчиках или других службах через DI.
5|```питон
6|пользователь = ожидание user_service.register_user(message.from_user.id)
7|пользователь = ожидание user_service.get_user(message.from_user.id)
8|ожидайте user_service.update_user(message.from_user.id, {"language_code": "en"})
9|```
10|
11|##Сервис кэша
12|Кэшируйте небольшие пользовательские значения, такие как язык.
13|```питон
14|lang = ожидание кэш_сервиса.get_user_language(user_id)
15|ожидайте кэш_сервис.set_user_language(user_id, "en", ttl=3600)
16|ожидайте кэш_service.invalidate_user_language(user_id)
17|```
18|
19|## Пользовательский репозиторий
20|Использование из UoW для прямого доступа к данным.
21|```питон
22|пользователь = ожидайте uow.users.get_by_filters(user_id=user_id)
23|users = await uow.users.list_by_filters(language_code="en")
24|```
25|