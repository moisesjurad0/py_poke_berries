# py_poke_berries

 repo for globant coding challenge

## Deployed on AWS

Check out the live version at: <https://w37tltqhef.execute-api.us-east-1.amazonaws.com/Prod/docs>

## How to run locally

1. run this commands

    ```sh
    # create virtual env
    python -m venv venv

    # activate virtual env
    .\venv\Scripts\activate.ps

    # install requirements
    pip install -r app/requirements.txt

    # run uvicorn server
    uvicorn app.main:app --reload
    ```

1. then check the OpenAPI specification on localhost
    - <http://127.0.0.1:8000/docs>
        - <http://127.0.0.1:8000/api/v1/poke-berries/allBerryStats>
        - <http://127.0.0.1:8000/api/v1/poke-berries/histogram>

## How to test

1. run this commands

    ```sh
    # create virtual env
    python -m venv venv

    # activate virtual env
    .\venv\Scripts\activate.ps

    # install requirements
    pip install -r tests/requirements.txt

    # run pytest
    pytest

    # or use -v to get more information
    pytest -v

    # can review coverage with this
    pytest --cov=app --cov-report=html

    # can also run mypy
    mypy app --ignore-missing-imports

    # or just run tox
    tox
    ```
