import asyncio
import base64
import logging
import statistics
from collections import Counter
from enum import Enum
from functools import reduce
from io import BytesIO
from typing import Dict, List, Optional, Union

import aiopoke
import matplotlib.pyplot as plt
import requests
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel  # , PositiveInt, Field

router = APIRouter()


class AllBerryStatsResponseModel(BaseModel):
    berries_names: List
    min_growth_time: int  # PositiveInt
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

    dict_final = {x.name: x.growth_time for x in results}

    print(dict_final)

    retorno = AllBerryStatsResponseModel(
        berries_names=list(dict_final.keys()),
        min_growth_time=min(dict_final.values()),
        median_growth_time=statistics.median(dict_final.values()),
        max_growth_time=max(dict_final.values()),
        variance_growth_time=statistics.variance(dict_final.values()),
        mean_growth_time=statistics.mean(dict_final.values()),
        frequency_growth_time=dict(Counter(dict_final.values()))
    )

    logging.info(f'response=>{retorno}')

    return retorno

@router.get("/histogram")
async def generate_histogram():
    response = await all_berry_stats()
    data = response.frequency_growth_time
    values = list(data.keys())
    frequencies = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(values, frequencies, color='skyblue', edgecolor='black')
    plt.title("Histogram")
    plt.xlabel("Berry Growth Time")
    plt.ylabel("Frequency")

    for i, freq in enumerate(frequencies):
        ax.text(values[i], freq, str(freq), ha='center', va='bottom')

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
        <h1>Histogram</h1>
        <img src="data:image/png;base64, {img_base64}" alt="Histogram">
    </body>
    </html>
    """

    return HTMLResponse(content=html_response)
