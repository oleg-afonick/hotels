import uvicorn
from fastapi import FastAPI, Body
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

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
    {"id": 2, "name": "Hotel 2", "address": "Address 2"}
]


@app.get("/hotels")
def get_hotels():
    return hotels


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
