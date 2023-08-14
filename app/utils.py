from fastapi import FastAPI


def reverse(fastapi_app: FastAPI, name: str, **params) -> str:
    return fastapi_app.url_path_for(name, **params)
