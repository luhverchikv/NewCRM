1|# услуг
2|
3|## Наследование BaseService
4|BaseService предоставляет помощники по доступу и ведению журналов UoW.
5|`source/services/base.py`:
6|```питон
7|класс BaseService(ABC, Generic[ModelType]):
8|def __init__(self, uow: AbstractUnitOfWork) -> Нет:
9|self._uow: AbstractUnitOfWork = uow
10|```
11|
12|## Создайте новый сервис
13|Расширьте BaseService и введите в него свою модель.
14|`source/services/user_service.py`:
15|```питон
16|из источника.импорт базы данных UserOrm
17|из source.services.base import BaseService
18|
19|класс UserService(BaseService[UserOrm]):
20|def __init__(self, uow: AbstractUnitOfWork) -> Нет:
21|супер().__init__(ууу)
22|```
23|
24|## Использование UnitOfWork
25|Оберните изменения БД в блоки `async with`.
26|`source/services/user_service.py`:
27|```питон
28|async def update_user(self, user_id: int, data: dict[str, object]) -> UserOrm |Нет:
29|асинхронно с self._uow:
30|return await self._uow.users.update(user_id, данные)
31|```
32|
33|## Добавить в ДИ (Дишка)
34|Зарегистрируйте поставщиков в AppProvider.
35|`source/factory/container.py`:
36|```питон
37|от импорта дишки, объем поставки
38|из импорта source.database AbstractUnitOfWork
39|из source.services импорт UserService
40|
41|@provide(scope=Scope.REQUEST)
42|def Provide_user_service(self, uow: AbstractUnitOfWork) -> UserService:
43|вернуть UserService(uow=uow)
44|```
45|