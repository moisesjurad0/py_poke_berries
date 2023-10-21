from collections import Counter

import time
from fastapi import APIRouter
from typing import Dict, List, Optional  # , List
import logging
from typing import Union
from fastapi.responses import HTMLResponse
from pydantic import BaseModel  # , PositiveInt, Field
from enum import Enum
from functools import reduce
import asyncio
import aiopoke
import requests
import statistics

import matplotlib.pyplot as plt
from io import BytesIO
import base64

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

    results = []
    async with asyncio.TaskGroup() as tg:
        async with aiopoke.AiopokeClient() as client:
            for i in range(1, berries_count + 1):
                task = tg.create_task(client.get_berry(i))
                results.append(await task)
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
    # Generate sample data for the histogram
    data = [1, 1, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5]

    # Create a histogram using Matplotlib
    plt.hist(data, bins=5, edgecolor='black')
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")

    # Save the plot as a PNG image
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    # Encode the image in base64 for embedding in HTML
    img_base64 = base64.b64encode(img_buffer.read()).decode()

    # Generate the HTML to display the image
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
