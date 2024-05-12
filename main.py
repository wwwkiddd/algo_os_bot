import telebot
from telebot import types
from parse import read_file
import os

# Вставь свой токен, полученный от BotFather
TOKEN = "6859686203:AAFECvej96xYwCKzRWz0LtImq3g57GD0uvs"

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Глобальные переменные для отслеживания состояния пользователя
current_course = ""
current_module = ""
current_lesson = ""
current_module_lesson = ""
last_message_id = None  # Добавим переменную для хранения ID последнего отправленного сообщения

# Курсы, их модули, уроки и названия уроков
courses_info = {
    "ОЛИП": {
        "modules": {
            "1. Линейные алгоритмы": {
                "lessons": ["Урок 1. Исполнитель и алгоритмы", "Урок 2. Программа и блок памяти", "Урок 3. Учимся считывать и выполнять программы", "Урок 4. Собираем линейные алгоритмы", "Урок 5. Собираем линейные алгоритмы"]
            },
            "2. Циклы": {
                "lessons": ["Урок 1. Знакомство с циклами", "Урок 2. Собираем циклические алгоритмы", "Урок 3. Собираем циклические алгоритмы"]
            },
            "3. Знакомство со Scratch Jr": {
                "lessons": ["Урок 1. Знакомство со средой Scratch Jr", "Урок 2. Scratch Jr. События («Когда спрайт нажат»), команды раздела «Движение»", "Урок 3. Команды раздела «Внешность»", "Урок 4. Циклы. Повторение. Интерактивный проект"]
            },
            "4. События. Мультипликация": {
                "lessons": ["Урок 1. События. Программирование параллельных (одновременных) действий при запуске проекта", "Урок 2. Программирование автоматической смены сцен при запуске проекта", "Урок 3. Создание мультипликации (начало). Вид героев при старте. Запись и использование звуков в Scratch", "Урок 4. Создание мультипликации (финализация), демонстрация проектов, повторение тем модуля"]
            },
            "5. Сообщения": {
                "lessons": ["Урок 1. Сообщения", "Урок 2. Использование сообщений в игре", "Урок 3. Программирование кнопок с использованием сообщений", "Урок 4. Программирование кнопок для управления героем"]
            },
            "6. Условие (касания) в качестве события": {
                "lessons": ["Урок 1. Программирование кнопок для управления героем.", "Урок 2. Передача сообщения при касании", "Урок 3. Создание игры с мультипликацией. Начало", "Урок 4. Создание игры с мультипликацией. Финализация"]
            },
            "7. Реализация игровой механики в проекте по выбору группы": {
                "lessons": ["Урок 1 .Выбор и начало реализации большого проекта группы", "Урок 2. Продолжение реализации большого проекта группы", "Урок 3. Продолжение реализации проекта группы", "Урок 4 .Презентация проектов"]
            },
            "8. Выбор и реализация финального проекта": {
                "lessons": ["Урок 1. Выбор и начало работы над финальным индивидуальным проектом курса", "Урок 2. Создание собственного индивидуального проекта по выбору", "Урок 3. Создание собственного индивидуального проекта по выбору", "Урок 4. Презентация итоговых проектов. Награждение"]
            },
        }
    },
    "КГ": {
        "modules": {
            "1. Базовая подготовка": {
                "lessons": ["Урок 1. Что такое информация и как компьютер с ней работает", "Урок 2. Организуем хранение информации на компьютере", "Урок 3. Как перенести информацию с одного компьютера на другой", "Урок 4. Проектный урок. Введение в стоп моушн"]
            },
            "2. Создание цифровых рисунков": {
                "lessons": ["Урок 1. Знакомимся с пикселем", "Урок 2. Рисуем в растре", "Урок 3. Рисуем в векторе", "Урок 4. Проектный урок. Иллюстрируем текст"]
            },
            "3. Коммуникация в сети": {
                "lessons": ["Урок 1. Персональная информация", "Урок 2. Способы коммуникации в сети", "Урок 3. Эффективная коммуникация", "Урок 4. Проектный урок. Создаём свою группу в социальной сети «Алгоритмика»"]
            },
            "4. Поиск информации в сети": {
                "lessons": ["Урок 1. Поиск графической информации в Сети", "Урок 2. Поиск текстовой информации в Сети", "Урок 3. Поиск по сайту", "Урок 4. Проектный урок. Делаем общий сайт"]
            },
            "5. Создание презентаций для устных выступлений": {
                "lessons": ["Урок 1. Знакомство с презентациями", "Урок 2. Структурируем презентацию", "Урок 3. Учимся оформлять истории", "Урок 4. Проектный урок. Создаем презентацию для устного выступления"]
            },
            "6. Табличное представление информации": {
                "lessons": ["Урок 1. Составление таблиц", "Урок 2. Знакомство с табличным редактором", "Урок 3. Оформление ячеек", "Урок 4. Проектный урок. Играем в 'Морской бой' при помощи табличного редактора"]
            },
            "7. Создание инфографики": {
                "lessons": ["Урок 1. Что такое инфографика?", "Урок 2. Создаём диаграммы", "Урок 3. Основы типографики", "Урок 4. Проектный урок. Используем инфографику в презентации"]
            },
            "8. Основы финансовой грамотности": {
                "lessons": ["Урок 1. Понятие о деньгах и бюджете", "Урок 2. Безналичные финансы", "Урок 3. Проектный урок. Планируем расходы на вечеринку"]
            },
            "9. Комикс": {
                "lessons": ["Урок 1. Знакомство с нейросетями", "Урок 2. Генерация картинок и сцены", "Урок 3. Проработка персонажа", "Урок 4. Окончательная сборка и анимации"]
            }
        }
    },
    "ВП": {
        "modules": {
            "1. Введение": {
                "lessons": ["Урок 1. Линейный алгоритм", "Урок 2. Циклы", "Урок 3. Начальная расстановка", "Урок 4. События", "Урок 5. Проект. Визитка"]
            },
            "2. Пространство": {
                "lessons": ["Урок 1. Координаты", "Урок 2. Повороты в направлении", "Урок 3. Вращение и градусы", "Урок 4. Сообщения", "Урок 5. Проект. Мультфильм"]
            },
            "3. Игра": {
                "lessons": ["Урок 1. Условия и оператор выбора", "Урок 2. Изменение координат", "Урок 3. Процедуры", "Урок 4. Планирование игры", "Урок 5. Тестирование игр", "Урок 6. Презентация игр"]
            },
            "4. Логика": {
                "lessons": ["Урок 1. Логические операторы И, ИЛИ, НЕ", "Урок 2. Цикл с условием", "Урок 3. Случайные числа и диапазоны", "Урок 4. Области координат", "Урок 5. Групповой проект", "Урок 6. Групповой проект. Доработка и презентация"]
            },
            "5. Переменные": {
                "lessons": ["Урок 1. Переменные в циклах", "Урок 2. Типы данных и операторы", "Урок 3. Переменные в играх", "Урок 4. Переменная как параметр", "Урок 5. Проект 'Чат-бот'", "Урок 6. Финализация и презентация проекта"]
            },
            "6. Клоны": {
                "lessons": ["Урок 1. Классы и объекты", "Урок 2. Локальные и глобальные переменные", "Урок 3. Интерфейсы", "Урок 4. Создание игры «Зеркала»", "Урок 5. Завершение игры «Зеркала»"]
            },
            "7. Финальный проект": {
                "lessons": ["Урок 1. Подготовка к финальному проекту", "Урок 2. Завершение финального проекта"  ]
            },
        }
    },
    "ГД": {
        "modules": {
            "1. Мир Roblox Studio": {
                "lessons": ["Урок 1. Roblox.com Vs Roblox Studio", "Урок 2. Моя первая настоящая 3D-игра", "Урок 3. Создаём игру для профессиональных киберспортсменов", "Урок 4. Совершенствуем игру-платформер", "Урок 5. Совершенствуем игру-платформер"]
            },
            "2. Мир, в котором я живу": {
                "lessons": ["Урок 1. Создаём свой мир: ландшафт и растения", "Урок 2. Создаём свой мир: здания", "Урок 3. Добавление скриптов. Практика", "Урок 4. Создаём свой мир: сюрпризы и препятствия", "Урок 5. Мир, в котором я живу (презентации миров)"]
            },
            "3. Мир, полный загадок (создание квеста)": {
                "lessons": ["Урок 1. Что такое геймдизайн?", "Урок 2. Добавление чат-ботов в игру", "Урок 3. Системный дизайн и переходы между уровнями", "Урок 4. Добавляем загадки и головоломки в квест", "Урок 5. Моя игра-квест"]
            },
            "4. Мир, полный сюрпризов (создание RPG)": {
                "lessons": ["Урок 1. Что такое Role-playing game?", "Урок 2. Добавление персонажей в игру", "Урок 3. Создаём атаку в игре", "Урок 4. Проектируем достижения игрока", "Урок 5. Представляем свою игру"]
            },
            "5. Мы такие разные (создание шутера)": {
                "lessons": ["Урок 1. Что такое шутер?", "Урок 2. Создаём карту для шутера", "Урок 3. Как сделать шутер многопользовательским?", "Урок 4. Проводим киберспортивный турнир"]
            },
            "6. Мир гоночных трасс": {
                "lessons": ["Урок 1. Что такое симуляторы?", "Урок 2. Оформляем карту для гонок", "Урок 3. Создаём свой квадроцикл", "Урок 4. Представляем симулятор гонок"]
            },
            "7. Переходим на новый уровень": {
                "lessons": ["Урок 1. Что такое аркады?", "Урок 2. Создание атак в аркадах", "Урок 3. Разработка мобильной версии игры", "Урок 4. Выпускной. Создание игры King of the Hill"]
            },
        }
    },
    "UNITY": {
        "modules": {
            "1. Основы Unity": {
                "lessons": ["Урок 1. Знакомство с Unity", "Урок 2. Работа с игровыми объектами и префабами", "Урок 3. Работа с материалами и текстурами", "Урок 4. Творческий урок. Создание прототипа"]
            },
            "2. Дизайн 3D-уровней": {
                "lessons": ["Урок 1. Начало работы с ландшафтом", "Урок 2. Детализация ландшафта", "Урок 3. Настройка света", "Урок 4. Визуальные и звуковые эффекты"]
            },
            "3. Программирование игр на языке C#": {
                "lessons": ["Урок 1. Введение в язык C#", "Урок 2. Переменные и типы данных", "Урок 3. Классы объектов", "Урок 4. Функции и методы", "Урок 5. Условные конструкции", "Урок 6. Интерфейс игрока", "Урок 7. Модульная разработка"]
            },
            "4. Анимация 3D-объектов": {
                "lessons": ["Урок 1. Введение в анимацию", "Урок 2. Анимация персонажа. Часть 1", "Урок 3. Анимация персонажа. Часть 2", "Урок 4. Завершение проекта. Работа с Timeline"]
            },
            "5. Специфика 2D-игр. Мобильная платформа": {
                "lessons": ["Урок 1. Введение в 2D-игры", "Урок 2. Создание космического шутера. Часть 1", "Урок 3. Создание космического шутера. Часть 2", "Урок 4. Работа с 2D-окружением. Релиз игры"]
            },
            "6. Создание гоночной 3D-игры": {
                "lessons": ["Урок 1. Знакомство с жанром гоночных игр", "Урок 2. Создание препятствий. Физический движок", "Урок 3. Добавление соперников с искусственным интеллектом", "Урок 4. Запись геймплейного ролика"]
            },
            "7. Создание ролевой игры в 2D": {
                "lessons": ["Урок 1. Игра в жанре RPG. Поворот и атака игрока", "Урок 2. Игра в жанре RPG. Перемещение и атака врага", "Урок 3. Игра в жанре RPG. Управление параметрами игрового уровня", "Урок 4. Игра в жанре RPG. Сохранение прогресса игрока. Система прокачки"]
            },
        }
    },
    "ПС1": {
        "modules": {
            "1. Основы языка": {
                "lessons": ["Урок 1. Введение в язык Python", "Урок 2. Переменные", "Урок 3. Строки", "Урок 4. Вложенные конструкции"]
            },
            "2. Управляющие конструкции": {
                "lessons": ["Урок 1. Условный оператор", "Урок 2. Вложенный условный оператор", "Урок 3. Циклы", "Урок 4. Циклы. Продолжение", "Урок 5. Вложенные управляющие конструкции"]
            },
            "3. Функции и модули": {
                "lessons": ["Урок 1. Функции", "Урок 2. Функции. Продолжение", "Урок 3. Модули random и time", "Урок 4. Создание модулей"]
            },
            "4. Модуль Turtle. Математика для разработчика": {
                "lessons": ["Урок 1. Turtle. Линейные алгоритмы.", "Урок 2. Turtle. Циклы", "Урок 3. Turtle. Условный оператор", "Урок 4. Проект 'Городская среда'"]
            },
            "5. Объектно-ориентированное программирование": {
                "lessons": ["Урок 1. ООП. Объекты и методы", "Урок 2. ООП. События", "Урок 3. ООП. Проект Simple Paint", "Урок 4. ООП. Классы", "Урок 5. ООП. Наследование", "Урок 6. ООП. Наследование. Продолжение"]
            },
            "6. Основы разработки игр на PyGame": {
                "lessons": ["Урок 1. Основы создания игр на Pygame", "Урок 2. Списки", "Урок 3. Игра Fast Clicker. Ч. 1", "Урок 4. Игра Fast Clicker. Ч. 2", "Урок 5. Игра Fast Clicker. Ч. 3", "Урок 6. Игра 'Арканоид'. Ч. 1", "Урок 7. Игра 'Арканоид'. Ч. 2", "Урок 8. Игра 'Арканоид'. Ч. 3"]
            },
            "7. Серия хакатонов": {
                "lessons": ["Урок 1. Воркшоп: навыки разработчика", "Урок 2. Хакатон. TestIT", "Урок 3. Хакатон. Simple Paint.", "Урок 4. Хакатон Grow Up"]
            },
        }
    },
    "ПС2": {
        "modules": {
            "1. Структуры данных": {
                "lessons": ["Урок 1. Повторение. Обработка исключений", "Урок 2. Повторение. Списки.", "Урок 3. Словари", "Урок 4. Вложенные структуры данных"]
            },
            "2. Разработка оконных приложений": {
                "lessons": ["Урок 1. Классы. Введение в PyQt", "Урок 2. Проектирование интерфейса", "Урок 3. Приложение Memory Card. Ч.1", "Урок 4. Приложение Memory Card. Ч2", "Урок 5. Приложение Memory Card. Ч.3", "Урок 6. Приложение Memory Card. Ч.4"]
            },
            "3. Работа с текстовыми файлами": {
                "lessons": ["Урок 1. Основы работы с файлами", "Урок 2. Приложение 'Умные заметки'. Ч. 1", "Урок 3. Приложение 'Умные заметки'. Ч. 2", "Урок 4. Приложение 'Умные заметки'. Ч. 3"]
            },
            "4. Автоматическая обработка изображений": {
                "lessons": ["Урок 1. Основы обработки изображений", "Урок 2. Приложение Easy Editor. Ч.1", "Урок 3. Приложение Easy Editor. Ч.2", "Урок 4. Приложение Easy Editor. Ч.3"]
            },
            "5. Продвинутая разработка игр на PyGame": {
                "lessons": ["Урок 1. Основы создания игр", "Урок 2. Игра 'Лабиринт'. Ч. 1", "Урок 3. Игра 'Лабиринт'. Ч. 2", "Урок 4. Игра 'Лабиринт'. Ч. 3", "Урок 5. Игра 'Шутер'. Ч. 1", "Урок 6. Игра 'Шутер'. Ч. 2", "Урок 7. Игра 'Шутер'. Ч. 3", "Урок 8. Игра 'Шутер'. Ч. 4", "Урок 9. Доработка и презентация проекта"]
            },
            "6. Публикация и распространение ПО": {
                "lessons": ["Урок 1. Сборка проекта в приложение", "Урок 2. Повторение. Введение в Git", "Урок 3. Игра 'Пинг-понг'. Ч. 1", "Урок 4. Игра 'Пинг-понг'. Ч. 2"]
            },
        }
    },
    "СС": {
        "modules": {
            "1. Создай свой первый сайт": {
                "lessons": ["Урок 1. Что такое сайт?", "Урок 2. Из чего сайт состоит?", "Урок 3. Проект (индивидуальный)"]
            },
            "2. Базовые правила создания сайтов": {
                "lessons": ["Урок 1. Внешний вид сайта", "Урок 2. Текст на сайте", "Урок 3. Изображения для сайта", "Урок 4. Меню сайта", "Урок 5. Проект (групповой)"]
            },
            "3. Сам себе конструктор": {
                "lessons": ["Урок 1. Разметка простых объектов на HTML", "Урок 2. Таблицы и их оформление", "Урок 3. Стили объектов разного типа", "Урок 4. Проект (индивидуальный)"]
            },
            "4. Управляй стилями": {
                "lessons": ["Урок 1. Селекторы по тегу", "Урок 2. Контекстные селекторы", "Урок 3. Каскадные таблицы стилей", "Урок 4. Проект (индивидуальный)"]
            },
            "5. Макет веб-страницы": {
                "lessons": ["Урок 1. Принципы создания макета", "Урок 2. Виды отступов и границ", "Урок 3. Списки маркированные и нумерованные", "Урок 4. Проект (индивидуальный)"]
            },
            "6. Блоки, встаньте в ряд": {
                "lessons": ["Урок 1. Контейнеры. Знакомство", "Урок 2. Виды контейнеров", "Урок 3. Флексбоксы", "Урок 4. Проект (индивидуальный)"]
            },
            "7. Профессиональная вёрстка": {
                "lessons": ["Урок 1. Псевдоклассы", "Урок 2. Псевдоэлементы", "Урок 3. Абсолютное позиционирование", "Урок 4. Проект (индивидуальный)"]
            },
            "8. Градиенты, трансформации, мультимедиа на сайте": {
                "lessons": ["Урок 1. Линейные градиенты", "Урок 2. Двумерные трансформации", "Урок 3. Размещаем видео и аудио на сайте", "Урок 4. Выпускной урок курса"]
            },
        }
    },
    "ГрД": {
        "modules": {
            "1. Растровый рисунок": {
                "lessons": ["Урок 1. Введение в графический дизайн  ", "Урок 2. Светотень. Основы работы с цветом", "Урок 3. Основы композиции и перспективы", "Урок 4. Творческий урок. Рисуем космос"]
            },
            "2. Коллажирование": {
                "lessons": ["Урок 1. Введение в коллажирование", "Урок 2. Паттерн - коммерческий коллаж", "Урок 3. Творческий урок. Создаём постер."]
            },
            "3. Ретушь": {
                "lessons": ["Урок 1. Введение в ретушь", "Урок 2. Творческий урок. Погружаемся в фэнтези"]
            },
            "4. 3D моделирование": {
                "lessons": ["Урок 1. Введение в 3D-моделирование", "Урок 2. Работа с основными формами", "Урок 3. Работа с основными формами. Продолжение", "Урок 4. Творческий урок. Игровая локация", "Урок 5. Игровая локация. Продолжение"]
            },
            "5. Книжная вёрстка": {
                "lessons": ["Урок 1. Введение в вёрстку", "Урок 2. Творческий урок. Буклет"]
            },
            "6. Векторная иллюстрация": {
                "lessons": ["Урок 1. Введение в векторную графику", "Урок 2. Оформляем to-do list", "Урок 3. Творческий урок. Оформляем календарь"]
            },
            "7. Инфографика": {
                "lessons": ["Урок 1. Введение в инфографику", "Урок 2. Творческий урок. Капсула времени"]
            },
            "8. Айдентика": {
                "lessons": ["Урок 1. Айдентика — дизайн бренда", "Урок 2. Творческий урок. Открываем бизнес"    ]
            },
            "9. Персонаж и хуманизация": {
                "lessons": ["Урок 1. Введение в создание персонажей", "Урок 2. Пропорции персонажей", "Урок 3. Творческий урок. Хуманизация", "Урок 4. Хуманизация. Продолжение"]
            },
            "10. Простейшая покадровая анимация": {
                "lessons": ["Урок 1. Введение в анимацию", "Урок 2. Ассеты и клипы", "Урок 3. Сценарии перемещения", "Урок 4. Творческий урок. Рекламная анимация"]
            },
        }
    },
    "ВБ": {
        "modules": {
            "1. Мобильная съёмка": {
                "lessons": ["Урок 1. Залог успешного видеоблога", "Урок 2. Монтаж видео. Переходы", "Урок 3. Что такое композиция кадра?", "Урок 4. Крупности кадра", "Урок 5. Продвинутые техники монтажа"]
            },
            "2. Основы видеомонтажа": {
                "lessons": ["Урок 1. Что такое скетч-ролик?", "Урок 2. Знакомство с OpenShot", "Урок 3. Разделение кадра в OpenShot", "Урок 4. Озвучка видеороликов", "Урок 5. Создание ролика в жанре VS", "Урок 6. Саунд-дизайн"]
            },
            "3. Эффекты видеомонтажа": {
                "lessons": ["Урок 1. Техника хромакей", "Урок 2. Создаём голограмму в видеоролике", "Урок 3. Что такое глитч эффект?", "Урок 4. Создаём интерфейс будущего в видеоролике", "Урок 5. Работа с изображениями в OpenShot"]
            },
            "4. Разнообразный контент": {
                "lessons": ["Урок 1. Жанры видеоблогинга", "Урок 2. Создание ролика в жанре Распаковка", "Урок 3. Создание DIY-видео", "Урок 4. Создание ролика в жанре топ", "Урок 5. Создаём разнообразный контент", "Урок 6. Что такое летсплей?", "Урок 7. Мой летсплей", "Урок 8. Что такое стоп-моушен?"]
            },
            "5. Оформление и настройка канала": {
                "lessons": ["Урок 1. Мой канал в социальной сети", "Урок 2. Создаём трейлер канала", "Урок 3. Продвижение видеоблога", "Урок 4. Виды и форматы сториз", "Урок 5. Создаём интерактивные сториз", "Урок 6. Виды монетизации", "Урок 7. Проведение марафона", "Урок 8. Выпускной. Создание музыкального клипа"]
            },
        }
    },

}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    global last_message_id  # Объявим переменную глобальной
    markup = types.InlineKeyboardMarkup(row_width=2)
    courses_buttons = [types.InlineKeyboardButton(course, callback_data=f"course_{course}") for course in courses_info.keys()]
    global back_to_course_button
    back_to_course_button = types.InlineKeyboardButton("Вернуться к выбору курса", callback_data=f"back_to_course")
    markup.add(*courses_buttons)

    # Отправляем новое сообщение с кнопками
    sent_message = bot.send_message(message.chat.id, "Привет! Выбери курс:", reply_markup=markup)

    # Сохраняем ID последнего отправленного сообщения
    last_message_id = sent_message.message_id

# Обработчик выбора курса
@bot.callback_query_handler(func=lambda call: call.data.startswith("course_"))
def choose_course(call):
    global current_course, current_module_lesson, last_message_id
    current_course = call.data.split("_")[1]
    current_module_lesson = ""  # Обнуляем значение при выборе нового курса

    # Получаем информацию о модулях и уроках для выбранного курса
    course_info = courses_info[current_course]

    markup = types.InlineKeyboardMarkup(row_width=1)
    module_buttons = [types.InlineKeyboardButton(module, callback_data=f"module_{idx}") for idx, module in enumerate(course_info["modules"])]
    markup.add(*module_buttons)
    markup.add(back_to_course_button)

    # Заменяем предыдущее сообщение новым с кнопками
    bot.edit_message_text("Теперь выбери модуль:", call.message.chat.id, last_message_id, reply_markup=markup)

# Обработчик выбора модуля
@bot.callback_query_handler(func=lambda call: call.data.startswith("module_"))
def choose_module(call):
    global current_module, current_module_lesson, last_message_id
    module_idx = int(call.data.split("_")[1])
    current_module = list(courses_info[current_course]["modules"].keys())[module_idx]
    current_module_lesson = ""  # Обнуляем значение при выборе нового модуля

    # Получаем информацию о модулях и уроках для выбранного курса
    course_info = courses_info[current_course]
    module_info = course_info["modules"][current_module]

    markup = types.InlineKeyboardMarkup(row_width=1)
    lesson_buttons = [types.InlineKeyboardButton(lesson, callback_data=f"lesson_{idx}") for idx, lesson in enumerate(module_info["lessons"])]
    markup.add(*lesson_buttons)
    markup.add(back_to_course_button)

    # Заменяем предыдущее сообщение новым с кнопками
    bot.edit_message_text(f"Теперь выбери урок:", call.message.chat.id, last_message_id, reply_markup=markup)

# Обработчик выбора урока
@bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_"))
def choose_lesson(call):
    global current_lesson, current_module_lesson, last_message_id
    lesson_idx = int(call.data.split("_")[1])
    current_lesson = courses_info[current_course]["modules"][current_module]["lessons"][lesson_idx]

    # Сохраняем номер модуля и номер урока в переменной current_module_lesson
    current_module_lesson = f"М{current_module[0]}У{lesson_idx + 1}"  # Используем первый символ модуля как его номер, увеличиваем на 1, так как порядковый номер начинается с 1

    # Заменяем предыдущее сообщение новым
    bot.edit_message_text(f"Ты выбрал {current_module_lesson}. Вот твоя обратная связь:", call.message.chat.id, last_message_id)
    folder_path = f'C:/Users/User/Desktop/{current_course}'
    file_name = f'{current_module_lesson}.txt'
    file_path = os.path.join(folder_path, file_name)
    print(f"Путь к файлу: {file_path}")
    file_content = read_file(file_path)
    print(f"Содержимое файла: {file_content}")

    bot.send_message(call.message.chat.id, file_content)

    # Добавляем кнопку для возврата к выбору курса
    markup = types.InlineKeyboardMarkup()
    markup.add(back_to_course_button)

    # Составляем строку с выбранным курсом, модулем и уроком в нужном формате
    selected_message = "Спасибо за визит!"

    # Отправляем новое сообщение с выбранными данными
    sent_message = bot.send_message(call.message.chat.id, selected_message, reply_markup=markup)

    # Сохраняем ID последнего отправленного сообщения
    last_message_id = sent_message.message_id

# Обработчик кнопки для возврата к выбору курса
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_course"))
def back_to_course(call):
    global last_message_id

    markup = types.InlineKeyboardMarkup(row_width=2)
    courses_buttons = [types.InlineKeyboardButton(course, callback_data=f"course_{course}") for course in courses_info.keys()]
    markup.add(*courses_buttons)

    # Заменяем предыдущее сообщение новым с кнопками
    bot.edit_message_text("Привет! Выбери курс:", call.message.chat.id, last_message_id, reply_markup=markup)

# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
    