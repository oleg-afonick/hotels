from fastapi import HTTPException


class BookingException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingException):
    detail = "Объект не найден"


class NoFreeRoomsException(BookingException):
    detail = "Нет свободных номеров"


class ExistsEmailException(BookingException):
    detail = "Пользователь с таким email уже существует"


class DateFromLaterDateToException(BookingException):
    detail = "Дата заезда позже даты выезда"


class HotelNotFoundException(BookingException):
    detail = "Отель не найден"


class RoomNotFoundException(BookingException):
    detail = "Номер не найден"


class BookingHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class HotelNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = "Отель не найден"

class DateFromLaterDateToHTTPException(BookingHTTPException):
    status_code = 409
    detail = "Дата заезда позже даты выезда"

class RoomNotFoundHTTPException(BookingHTTPException):
    status_code = 404
    detail = "Номер не найден"


class NoFreeRoomsHTTPException(BookingHTTPException):
    status_code = 409
    detail = "Нет свободных номеров"
