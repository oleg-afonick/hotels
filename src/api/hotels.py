from fastapi import Body, APIRouter

from src.api.dependencies import paginator
from src.schemas.hotels import HotelSchema, HotelSchemaPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "name": "Hotel 1", "address": "Address 1"},
    {"id": 2, "name": "Hotel 2", "address": "Address 2"},
    {"id": 3, "name": "Hotel 3", "address": "Address 3"},
    {"id": 4, "name": "Hotel 4", "address": "Address 4"},
    {"id": 5, "name": "Hotel 5", "address": "Address 5"},
    {"id": 6, "name": "Hotel 6", "address": "Address 6"},
    {"id": 7, "name": "Hotel 7", "address": "Address 7"},
    {"id": 8, "name": "Hotel 8", "address": "Address 8"},
    {"id": 9, "name": "Hotel 9", "address": "Address 9"},
    {"id": 10, "name": "Hotel 10", "address": "Address 10"}
]


@router.get("")
def get_hotels(pagination: paginator):
    if pagination.page and pagination.per_page:
        start = (pagination.page - 1) * pagination.per_page
        end = start + pagination.per_page
        paginated_hotels = hotels[start:end]
        return paginated_hotels
    return hotels


@router.post("")
def post_hotels(hotel_data: HotelSchema):
    hotels.append({"id": hotels[-1]["id"] + 1, "name": hotel_data.name, "address": hotel_data.address})
    return hotels


@router.put("/{hotel_id}")
def hotels_put(hotel_id: int, hotel_data: HotelSchema):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotel["name"] = hotel_data.name
        hotel["address"] = hotel_data.address
        return hotels
    return "Hotel not found"


@router.patch("/{hotel_id}")
def hotels_patch(
        hotel_id: int, hotel_data: HotelSchemaPATCH):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotel["name"] = hotel_data.name if hotel_data.name else hotel["name"]
        hotel["address"] = hotel_data.address if hotel_data.address else hotel["address"]
        return hotels
    return "Hotel not found"


@router.delete("/{hotel_id}")
def hotels_delete(hotel_id: int):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotels.remove(hotel)
        return hotels
    return "Hotel not found"
