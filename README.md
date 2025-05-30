# AvitoParseMachine

Приложение для парсинга данных с Avito.

## Возможности

- Парсинг названий, цен и ссылок товаров с Avito
- Сохранение результатов в Excel-файл
- Простой графический интерфейс на Kivy
- Реализация принципов SOLID:
  - Классы с единственной ответственностью
  - Внедрение зависимостей
  - Разделение интерфейсов
  - Открытость/закрытость архитектуры

## Требования

- Python 3.7+
- Установленные пакеты:
  - kivy
  - selenium
  - pandas
  - beautifulsoup4

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/вашusername/avito-parser.git
cd avito-parser

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

1. Запустите приложение:
```bash
python main.py
```

2. В приложении:
- Введите URL страницы Avito
- Нажмите кнопку "Начать парсинг"
- Просмотрите результаты в текстовом поле
- Результаты автоматически сохранятся в `results.xlsx`

## Структура проекта

```
src/
│── core/
│   ├── parsers/              # Реализации парсеров
│   │   └── avito_parser.py
│   ├── data_handlers/        # Обработка данных
│   │   └── excel_handler.py
│   └── factories/            # Фабрики
│       └── driver_factory.py
│── interfaces/               # Интерфейсы
│   ├── iparser.py
│   ├── idata_handler.py
│   └── idriver_factory.py
└── ui/                       # Графический интерфейс
    ├── main_window.py
    └── app.py
```

## Расширение функциональности

Чтобы добавить новый парсер:
1. Создайте класс, реализующий `IParser`
2. Зарегистрируйте в контейнере зависимостей

Пример:
```python
class NewSiteParser(IParser):
    def parse(self, url):
        # реализация парсера
```

## Лицензия

MIT License

## Участие в разработке

PR приветствуются. Для крупных изменений сначала откройте issue для обсуждения.
```
