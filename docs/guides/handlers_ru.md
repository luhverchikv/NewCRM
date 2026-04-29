1|# обработчиков
2|
3|## Обработчики команд
4|Простые команды находятся в `user_commands_router`.
5|`source/telegram/handlers/user/commands.py`:
6|```питон
7|из команды импорта aiogram.filters
8|из сообщения импорта aiogram.types
9|из диалога импорта aiogram_dialog
10|из aiogram_dialog импортировать StartMode
11|
12|из source.telegram.states импорт DialogSG
13|
14|@user_commands_router.message(Команда("диалог"))
15|async def диалог_команда (сообщение: Сообщение, диалог_менеджер: DialogManager) -> Нет:
16|дождитесь диалога_manager.start(DialogSG.first, mode=StartMode.RESET_STACK)
17|```
18|
19|## Обработчики обратного вызова
20|Обратные вызовы фильтруются по данным и могут использовать DI.
21|`source/telegram/handlers/user/callbacks.py`:
22|```питон
23|из импорта айограммы F
24|из aiogram.types импортировать CallbackQuery
25|из импорта дишки FromDishka
26|из diskka.integrations.aiogram импортировать как aiogram_inject
27|
28|из source.services импорт UserService
29|из source.utils импорт I18n
30|
31|@user_callbacks_router.callback_query(F.data == "language_ru")
32|@aiogram_inject
33|async def Language_ru(
34|обратный вызов: CallbackQuery,
35|i18n: ОтДишка[I18n],
36|user_service: FromDishka[UserService],
37|) -> Нет:
38|ожидайте обратного вызова.ответ("")
39|await user_service.update_user(callback.from_user.id, {"language_code": "ru"})
40|i18n.invalidate_cache(callback.from_user.id)
41|```
42|
43|## обработчики автомата
44|Используйте состояния для управления многоэтапными потоками.
45|`источник/telegram/handlers/user/fsm.py`:
46|```питон
47|из aiogram.fsm.context импортировать FSMContext
48|из сообщения импорта aiogram.types
49|из импорта дишки FromDishka
50|из diskka.integrations.aiogram импортировать как aiogram_inject
51|
52|из источника.telegram.filters импортировать AgeValidator
53|из source.telegram.states импортировать FormSG
54|из source.utils импорт I18n
55|
56|@user_fsm_router.message(FormSG.name)
57|@aiogram_inject
58|async def имя_процесса(
59|сообщение: Сообщение, состояние: FSMContext, i18n: FromDishka[I18n]
60|) -> Нет:
61|ждут state.update_data(name=message.text)
62|ждут state.set_state(FormSG.age)
63|ожидайте сообщения.ответ(ожидайте i18n(message.from_user.id, "fsm-enter-age"))
64|
65|@user_fsm_router.message(FormSG.age, AgeValidator())
66|@aiogram_inject
67|async defprocess_age(
68|сообщение: Сообщение, состояние: FSMContext, i18n: FromDishka[I18n]
69|) -> Нет:
70|данные = ждут state.get_data()
71|дождитесь сообщения.ответ(
72|жду i18n(
73|сообщение.from_user.id,
74|"фсм-результат",
75|имя=данные["имя"],
76|возраст = сообщение.текст,
77|)
78|)
79|дождитесь состояния.clear()
80|```
81|
82|## С внедрением зависимостей (Дишка)
83|Внедряйте сервисы или утилиты с помощью FromDishka и @aiogram_inject.
84|`source/telegram/handlers/user/commands.py`:
85|```питон
86|из aiogram.filters import CommandStart
87|из сообщения импорта aiogram.types
88|из импорта дишки FromDishka
89|из diskka.integrations.aiogram импортировать как aiogram_inject
90|
91|из source.services импорт UserService
92|из source.utils импорт I18n
93|
94|@user_commands_router.message(CommandStart())
95|@aiogram_inject
96|async def start(
97|сообщение: Сообщение,
98|user_service: FromDishka[UserService],
99|i18n: ОтДишка[I18n],
100|) -> Нет:
101|ожидайте user_service.register_user(message.from_user.id)
102|ожидайте сообщения.ответ(ожидайте i18n(message.from_user.id, "приветствие"))
103|```
104|