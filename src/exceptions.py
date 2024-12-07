class HotelsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelsException):
    detail = "Объект не найден"

class NoFreeRoomsException(HotelsException):
    detail = "Нет свободных номеров"
    
class ExistsEmailException(HotelsException):
    detail = "Пользователь с таким email уже существует"

class DateFromLaterDateToException(HotelsException):
    detail = "Дата заезда позже даты выезда"

class HotelNotFoundException(HotelsException):
    detail = "Отель не найден"

class RoomNotFoundException(HotelsException):
    detail = "Номер не найден"