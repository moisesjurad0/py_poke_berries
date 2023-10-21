from fastapi import APIRouter

from .endpoints import poke_berries

router = APIRouter()
router.include_router(poke_berries.router, prefix="/poke-berries", tags=["Poke-Berries"])