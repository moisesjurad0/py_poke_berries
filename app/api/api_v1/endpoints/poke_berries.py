import time
import asyncio
import base64
import logging
from collections import Counter
from functools import reduce
from io import BytesIO
from typing import Dict, List

import aiopoke
import matplotlib.pyplot as plt
import numpy as np
import requests
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter()


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
async def slow_method():

    for i in range(50):
        logging.info(f'i->{i}')
        time.sleep(1)
