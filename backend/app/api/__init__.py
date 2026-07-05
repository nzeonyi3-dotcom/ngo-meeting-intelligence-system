"""Main API router."""

from fastapi import APIRouter

from app.api.v1 import api as v1_api

router = APIRouter()

router.include_router(v1_api.router, prefix="/v1")
