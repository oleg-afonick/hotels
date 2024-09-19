import uvicorn
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from math import ceil

app = FastAPI()


@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",  # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])

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
    {"id": 10, "name": "Hotel 10", "address": "Address 10"},
    {"id": 11, "name": "Hotel 11", "address": "Address 11"}
]


@app.get("/hotels")
def get_hotels(
        page: int | None = Query(1, ge=1, le=len(hotels)),
        per_page: int | None = Query(len(hotels), ge=1, le=len(hotels))
) -> list[dict]:
    if per_page > ceil(len(hotels) / page):
        raise HTTPException(status_code=422, detail=f"per_page доступен не более {ceil(len(hotels) / page)}")
    elif page == 1:
        hotels_pagination = hotels[:per_page]
    else:
        hotels_pagination = hotels[(page - 1) * per_page:page * per_page]
    return hotels_pagination


@app.post("/hotels")
def post_hotels(name: str = Body(), address: str = Body()):
    hotels.append({"id": hotels[-1]["id"] + 1, "name": name, "address": address})
    return hotels


@app.put("/hotels/{hotel_id}")
def hotels_put(
        hotel_id: int,
        hotel_name: str = Body(),
        hotel_address: str = Body()
):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotel["name"] = hotel_name
        hotel["address"] = hotel_address
        return hotels
    return "Hotel not found"


@app.patch("/hotels/{hotel_id}")
def hotels_patch(
        hotel_id: int,
        hotel_name: str | None = Body(None),
        hotel_address: str | None = Body(None)
):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotel["name"] = hotel_name if hotel_name else hotel["name"]
        hotel["address"] = hotel_address if hotel_address else hotel["address"]
        return hotels
    return "Hotel not found"


@app.delete("/hotels/{hotel_id}")
def hotels_delete(hotel_id: int):
    get_hotel = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if get_hotel:
        hotel = get_hotel[0]
        hotels.remove(hotel)
        return hotels
    return "Hotel not found"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
