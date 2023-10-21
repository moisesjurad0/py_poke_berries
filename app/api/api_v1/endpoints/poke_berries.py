import time
from fastapi import APIRouter
from typing import List, Optional  # , List
import logging
from typing import Union
from pydantic import BaseModel  # , PositiveInt, Field
from enum import Enum
from functools import reduce

router = APIRouter()


class AllBerryStatsResponseModel(BaseModel):
    berries_names: List
    min_growth_time: int  # PositiveInt
    median_growth_time: float
    max_growth_time: int
    variance_growth_time: float
    mean_growth_time: float
    frequency_growth_time: float


@router.get("/allBerryStats")
def all_berry_stats() -> AllBerryStatsResponseModel:
    retorno = AllBerryStatsResponseModel(
        berries_names=['hola', 'mundo'],
        min_growth_time=1,
        median_growth_time=1,
        max_growth_time=1,
        variance_growth_time=1,
        mean_growth_time=1,
        frequency_growth_time=1,
    )

    logging.info(f'response=>{retorno}')

    return retorno
