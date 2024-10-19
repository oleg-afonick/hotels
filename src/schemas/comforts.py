from pydantic import BaseModel


class ComfortSchemaPostPut(BaseModel):
    title: str


class RoomSchema(ComfortSchemaPostPut):
    id: int

    class Config:
        from_attributes = True
