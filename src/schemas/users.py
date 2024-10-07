from pydantic import BaseModel, EmailStr


class UserSchemaRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserSchemaAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr


class UserSchemaLogin(UserSchema):
    hashed_password: str
