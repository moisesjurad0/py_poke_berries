import asyncio
import base64
import json
# import json
import logging
import time
from collections import Counter
from functools import reduce
from io import BytesIO
from typing import Annotated, Dict, List

import aiopoke
import boto3
import matplotlib.pyplot as plt
import numpy as np
import requests
from fastapi import APIRouter, FastAPI, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.requests import Request
import pprint
router = APIRouter()


class AnimalModel(BaseModel):
    name: str
    legs: int


class AllBerryStatsResponseModel(BaseModel):
    berries_names: List
    min_growth_time: int
    median_growth_time: float
    max_growth_time: int
    variance_growth_time: float
    mean_growth_time: float
    frequency_growth_time: Dict


@router.get("/allBerryStats")
async def all_berry_stats() -> AllBerryStatsResponseModel:

    response = requests.get(
        'https://pokeapi.co/api/v2/berry/?limit=200&offset=0')
    response.raise_for_status()
    r_json = response.json()
    berries_count = int(r_json['count'])

    # this works in python 3.10
    results = []
    async with aiopoke.AiopokeClient() as client:
        tasks = [
            asyncio.create_task(
                client.get_berry(i))
            for i in range(1, berries_count + 1)]
        results = await asyncio.gather(*tasks)

    # # this works in python 3.11
    # results = []
    # async with asyncio.TaskGroup() as tg:
    #     async with aiopoke.AiopokeClient() as client:
    #         for i in range(1, berries_count + 1):
    #             task = tg.create_task(client.get_berry(i))
    #             results.append(await task)

    dict_name_n_growth = {x.name: x.growth_time for x in results}
    print(dict_name_n_growth)

    berries_names = list(dict_name_n_growth.keys())
    growth_times = list(dict_name_n_growth.values())

    retorno = AllBerryStatsResponseModel(
        berries_names=berries_names,
        min_growth_time=np.min(growth_times),
        median_growth_time=np.median(growth_times),
        max_growth_time=np.max(growth_times),
        variance_growth_time=np.var(growth_times),  # ddof=1),
        mean_growth_time=np.mean(growth_times),
        frequency_growth_time=dict(Counter(growth_times))
    )

    logging.info(f'response=>{retorno}')
    return retorno


@router.get("/histogram")
async def generate_histogram():
    response = await all_berry_stats()
    data_dict = response.frequency_growth_time
    print(data_dict)
    data = [key for key, value in data_dict.items() for _ in range(value)]
    print(data)
    plt.xticks(range(1, 30))
    plt.yticks(range(1, 30))
    plt.hist(data, bins=30)
    plt.title("Histogram")
    plt.xlabel("Growth Time")
    plt.ylabel("Frequency")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.read()).decode()

    html_response = f"""
    <html>
    <head>
        <title>Histogram</title>
    </head>
    <body>
        <h1>Poke-Berries Growth Histogram</h1>
        <img src="data:image/png;base64, {img_base64}" alt="Histogram">
    </body>
    </html>
    """

    return HTMLResponse(content=html_response)


@router.get("/slow_method")
async def slow_method(
    # X_Amz_Invocation_Type: str | None = Header(default="'Event'"),
    InvocationType: str | None = Header(default="RequestResponse "),
):
    # x_amz_invocation_type
    # X_Amz_Invocation_Type
    # X-Amz-Invocation-Type

    for i in range(45):
        logging.info(f'i->{i}')
        time.sleep(1)


@router.post("/hello")
def hello(request: Request, animal: AnimalModel) -> AnimalModel:
    logging.info('m01.hello')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope)
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.event'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.context'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')

    # logging.info(pprint.pprint(request.scope))

    return animal
    # return json.dumps(request)
    # return {"aws_event": request.scope["aws.event"]}
    # return 'hello'


@router.post("/hi")
def hi(request: Request, animal: AnimalModel) -> AnimalModel:
    logging.info('m01.hi')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope)
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.event'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.context'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')

    # scope['aws.event']
    # scope['aws.context']
    # return {"aws_event": request.scope["aws.event"]}

    function_arn = request.scope['aws.context'].invoked_function_arn
    region = request.scope['aws.context'].invoked_function_arn.split(":")[3]

    # lambda_client = boto3.client('lambda', config=boto3.config.Config(region=region))
    lambda_client = boto3.client('lambda')

    response = lambda_client.invoke(
        FunctionName=function_arn,
        InvocationType='Event',
        Payload=json.dumps({

            "path": '/api/v1/poke-berries/hello',
            # "path": request.scope['aws.event']['path'],  # "/my/custom/path",
            # {"param1": "value1","param2": "value2"},
            # "pathParameters": request.scope['aws.context']['path_params'],
            # {"data": "payload_data"}
            "body": request.scope['aws.event']['body']
        })
    )

    logging.info(response)

    return animal


@router.get("/hi2/{item_id}")
def hi2(item_id: int) -> int:
    logging.info('m01.hi2')
    logging.info('---')
    logging.info(item_id)
    logging.info('---')
    return item_id


@router.get("/hi3/{item_id}")
def hi3(request: Request, item_id: int) -> int:
    logging.info('m01.hi3')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope)
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.event'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info(request.scope['aws.context'])
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')
    logging.info('---')

    # scope['aws.event']
    # scope['aws.context']
    # return {"aws_event": request.scope["aws.event"]}

    function_arn = request.scope['aws.context'].invoked_function_arn
    # region = request.scope['aws.context'].invoked_function_arn.split(":")[3]

    # lambda_client = boto3.client('lambda', config=boto3.config.Config(region=region))
    lambda_client = boto3.client('lambda')

    response = lambda_client.invoke(
        FunctionName=function_arn,
        InvocationType='Event',
        Payload=json.dumps({
            "resource": "/{proxy+}",
            "path": '/api/v1/poke-berries/hi2/' + str(item_id),
            "httpMethod": "GET",
            "requestContext": {
                "accountId": "123456789012",
                "resourceId": "123456",
                "stage": "prod",
                "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
                "requestTime": "09/Apr/2015:12:34:56 +0000",
                "requestTimeEpoch": 1428582896000,
                "identity": {
                    "cognitoIdentityPoolId": None,
                    "accountId": None,
                    "cognitoIdentityId": None,
                    "caller": None,
                    "accessKey": None,
                    "sourceIp": "127.0.0.1",
                    "cognitoAuthenticationType": None,
                    "cognitoAuthenticationProvider": None,
                    "userArn": None,
                    "userAgent": "Custom User Agent String",
                    "user": None
                },
                "path": "/prod/path/to/resource",
                "resourcePath": "/{proxy+}",
                "httpMethod": "POST",
                "apiId": "1234567890",
                "protocol": "HTTP/1.1"
            }
            # "requestContext": request.scope['aws.context'],
            # "requestContext": "{}"
            # "path": request.scope['aws.event']['path'],  # "/my/custom/path",
            # {"param1": "value1","param2": "value2"},
            # "pathParameters": request.scope['aws.context']['path_params'],
            # {"data": "payload_data"}
            # "body": request.scope['aws.event']['body']
        })
    )

    logging.info(response)

    return item_id
