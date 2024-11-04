from fastapi import APIRouter

from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.comforts import router as comforts_router
from src.api.images import router as images_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(hotels_router)
api_router.include_router(rooms_router)
api_router.include_router(comforts_router)
api_router.include_router(bookings_router)
api_router.include_router(images_router)