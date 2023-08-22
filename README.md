Проект написан на FastAPI с использованием PostgreSQL в качестве БД. Проект
реализовывает REST API по работе с меню ресторана, все CRUD операции.

Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:

- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.

Условия:

- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд
  в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в
  этом подменю.

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

<details>
<summary><b>Дополнительные задания:</b></summary>

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
</details>
