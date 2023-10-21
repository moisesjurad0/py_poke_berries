import logging


from api.api_v1.api import router as api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# ************ ENABLE ON DEV ENV ************
# from pathlib import Path
# import datetime
# script_path = Path(__file__).absolute()
# script_dir = Path(__file__).parent.absolute()
# log_folder = script_dir / 'logs'
# log_folder.mkdir(parents=True, exist_ok=True)
# currentDT = datetime.datetime.now()
default_log_args = {
    'level': logging.INFO,
    'format': '[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(module)s] [%(funcName)s] [L%(lineno)d] [P%(process)d] [T%(thread)d] %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    # 'filename': log_folder / f'quiz01scraper.api.{currentDT.strftime("%Y%m%d%H%M%S")}.log', # ENABLE ON DEV ENV
    'force': True,
}
logging.basicConfig(**default_log_args)

description = """
PokeBerriesAPI helps you do operations with Berries from PokeAPI. 🚀

## PokeBerries

You will be able to:

* **allBerryStats** (get statistics from PokeAPI Berries).
* **histogram** (get histogram from statistics)
"""

app = FastAPI(
    title="PokeBerries-API",
    description=description,
    summary="do PokeBerries operations.",
    version="1.0.0",
    contact={
        "name": "moisesjurad0",
        "url": "https://linktr.ee/moisesjurad0",
    },
    root_path='/Prod'  # REMOVE ON DEV ENV
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

handler = Mangum(app)
