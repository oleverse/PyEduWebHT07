- пакунок без setup.py
- для підключення до БД у каталозі **conf** повинен бути файл **db.ini**
- робота скрипту протестована з Python 3.11.3

Послідовність для запуску:
- клонуємо проєкт з репозиторію
> $ git clone git@github.com:oleverse/PyEduWebHT07.git
- встановлюємо залежності
> cd PyEduWebHT07

> poetry shell

> poetry update

- створюємо прожню базу даних
- задаємо sqlalchemy.url у файлі alembic.ini
- виконуємо міграцію
> alembic upgrade head
- переходимо у каталог з основним скриптом
> cd pyeduwebht07
- задаємо SQLAlchemy.url у файлі conf/db.ini
- заповнюємо БД даними
> python seed.py
- запускаємо сам скрипт
> python .
