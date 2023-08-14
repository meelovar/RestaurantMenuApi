# Запуск

Для запуска должны быть установлены Docker и docker-compose.

Запуск без Celery
```shell
docker-compose up --build
```

Запуск с Celery
```shell
docker-compose --profile nonautomatic up --build
```

Файл `Menu.xlsx` примонтирован к контейнеру как volume, поэтому изменения
этого файла на хосте проявляются в контейнере.

# Запуск тестов

```shell
docker-compose -f docker-compose.test.yml up --build
```

# Дополнительные задания

- Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM
запрос.

(+/-) Файл [app/models.py](app/models.py). Вывод количества реализуется через
`column_property`, которые генерируют подзапросы.

Так же это можно было бы реализовать по-другому. Тогда запросы были бы такого
вида:
```python
select(
    Menu.id,
    Menu.title,
    Menu.description,
    func.count(Submenu.id).label('submenus_count'),
    func.count(Dish.id).label('dishes_count')
).outerjoin(
    Submenu, Submenu.menu_id == Menu.id
).outerjoin(
    Dish, Dish.submenu_id == Submenu.id
).group_by(
    Menu.id
)
```

- Реализовать тестовый сценарий "Проверка кол-ва блюд и подменю в меню" из
Postman с помощью pytest.

Файл [tests/test_counts.py](tests/test_counts.py).

- Реализовать в тестах аналог Django `reverse()` для FastAPI

Файл [app/utils.py](app/utils.py).

# pre-commit

pre-commit запускается через GitHub Actions.

Для того чтобы запустить его вручную, необходимо:

1. Создать и активировать виртуальное окружение

    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Установить пакет и хуки

    ```shell
   pip install pre-commit
   pre-commit install
   ```

3. Запустить проверку

    ```shell
   pre-commit run --all-files
   ```
