# Кошачий благотворительный фонд
- version 0.0.1
- При разработке использовался Python 3.9.7.
- Аннотации типов в стиле 3.7
## Установка
Клонировать репозиторий и перейти в него:

```shell
git clone 
```

```shell
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```shell
python3 -m venv venv
```

* Если у вас Linux/macOS

```shell
source venv/bin/activate
```

* Если у вас windows

```shell
source venv/scripts/activate
```

Установить зависимости из файла requirements.txt:

```shell
python3 -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

Создать .env файл:
```shell
touch .env
```

Внести в файл следующие переменные:
```shell
echo "FIRST_SUPERUSER_EMAIL=your_email" > .env
echo "FIRST_SUPERUSER_PASSWORD=your_password" > .env
echo "DATABASE_URL=YOUR_DATABASE_URI_KEY" > .env
echo "SECRET=YOUR_SECRET_KEY" > .env
```

Применить миграции:
```shell
alembic upgrade head
```
## Запуск
```shell
uvicorn app.main:app
```

## Документация API.
/docs - swagger
/redoc - redoc

### Автор проекта
@epanchincev