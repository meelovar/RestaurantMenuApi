# Запуск

Для запуска должны быть установлены Docker и docker-compose.

```shell
docker-compose up --build
```

# Запуск тестов

```shell
docker-compose -f docker-compose.test.yml up --build
```

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
