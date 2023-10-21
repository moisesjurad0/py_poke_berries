from api.api_v1.api import router as api_router
from fastapi import FastAPI, Request 
from mangum import Mangum
# from mangum import Mangum, Contex
import logging
from fastapi.middleware.cors import CORSMiddleware


default_log_args = {
    'level': logging.INFO,
    'format': '[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(module)s] [%(funcName)s] [L%(lineno)d] [P%(process)d] [T%(thread)d] %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S',
    'force': True,
}
logging.basicConfig(**default_log_args)

description = """
PokeBerriesAPI helps you do operations with Berries from PokeAPI. 🚀

## PokeBerries

You will be able to:

* **allBerryStats** (Create & Update & batch).
* **histogram**.
"""

app = FastAPI(
    title="PokeBerries-API",
    description=description,
    summary="do PokeBerries operations.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "moisesjurad0",
        "url": "https://linktr.ee/moisesjurad0",
        # "email": "moises003@outlook.com",
    },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    #root_path='/Prod'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/ok")
# @app.get("/test")
# async def test_ok():
#     ok = 'ok'
#     print(ok)
#     logging.info(ok)
#     return ok

app.include_router(api_router, prefix="/api/v1")

handler = Mangum(app)
