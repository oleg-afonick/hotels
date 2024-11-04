from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.schemas.bookings import BookingSchema
from src.schemas.rooms import RoomSchema, RoomM2MSchema
from src.models.hotels import HotelsModel
from src.schemas.hotels import HotelSchema
from src.models.users import UsersModel
from src.schemas.users import UserSchema, UserSchemaLogin
from src.models.comforts import ComfortsModel, RoomsComfortsModel
from src.schemas.comforts import ComfortSchema, RoomComfortSchema
from src.mappers.base import DataMapper


class UserDataMapper(DataMapper):
    model_database = UsersModel
    model_schema = UserSchema

class UserLoginDataMapper(DataMapper):
    model_database = UsersModel
    model_schema = UserSchemaLogin

class HotelDataMapper(DataMapper):
    model_database = HotelsModel
    model_schema = HotelSchema

class RoomDataMapper(DataMapper):
    model_database = RoomsModel
    model_schema = RoomSchema

class RoomM2MDataMapper(DataMapper):
    model_database = RoomsModel
    model_schema = RoomM2MSchema


class BookingDataMapper(DataMapper):
    model_database = BookingsModel
    model_schema = BookingSchema


class ComfortDataMapper(DataMapper):
    model_database = ComfortsModel
    model_schema = ComfortSchema

class RoomComfortDataMapper(DataMapper):
    model_database = RoomsComfortsModel
    model_schema = RoomComfortSchema

UserMapper = UserDataMapper()
UserLoginMapper = UserLoginDataMapper()
HotelMapper = HotelDataMapper()
RoomMapper = RoomDataMapper()
RoomM2MMapper = RoomM2MDataMapper()
BookingMapper = BookingDataMapper()
ComfortMapper = ComfortDataMapper()
RoomComfortMapper = RoomComfortDataMapper()