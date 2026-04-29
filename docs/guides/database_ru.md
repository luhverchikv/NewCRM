1|# База данных
2|
3|## Создать модель
4|Определите модели ORM в `source/database/models/`.
5|`источник/база данных/модели/user.py`:
6|```питон
7|из импорта sqlalchemy BigInteger
8|из строки импорта sqlalchemy
9|из sqlalchemy.orm import Mapped, Mapped_column
10|
11|из ..tools import TableNameMixin
12|из базы импорта .base
13|
14|класс UserOrm(Base, TableNameMixin):
15|user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
16|языковой_код: Сопоставлено[str |Нет] = mapped_column(String(2), default="en")
17|```
18|
19|## Создать репозиторий
20|Репозитории оборачивают запросы и располагаются в `source/database/repositories/`.
21|`источник/база данных/репозитории/user.py`:
22|```питон
23|из source.database.models импортировать UserOrm
24|из source.database.repositories.base import AbstractRepository
25|
26|класс UserRepository(AbstractRepository[UserOrm, int]):
27|модель = ПользовательОрм
28|```
29|
30|## Добавить в UnitOfWork
31|Открыть репозитории UoW для использования в транзакциях.
32|`источник/база данных/инструменты/uow.py`:
33|```питон
34|из source.database.repositories импортировать UserRepository
35|
36|async def __aenter__(self) -> Self:
37|self._session = self._session_factory()
38|self._transaction = ожидайте self._session.begin()
39|self.users = UserRepository(self._session)
40|вернуть себя
41|```
42|
43|## Использование в эксплуатации
44|Сервисы оркеструют бизнес-логику с помощью UoW.
45|`source/services/user_service.py`:
46|```питон
47|async def add_user(self, data: dict[str, object]) -> UserOrm:
48|асинхронно с self._uow:
49|возвращение ждет self._uow.users.add(данные)
50|```
51|
52|## Миграции
53|Сгенерируйте и примените изменения схемы с помощью Alembic.
54|```баш
55|uv запустить перегонную ревизию --autogenerate -m "добавить пользователей"
56|УФ-обновление головки перегонного куба
57|```
58|