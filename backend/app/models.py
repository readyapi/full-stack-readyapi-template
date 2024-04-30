from sqldev import Field, Relationship, SQLDev


# Shared properties
# TODO replace email str with EmailStr when sqldev supports it
class UserBase(SQLDev):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqldev supports it
class UserRegister(SQLDev):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqldev supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqldev supports it
class UserUpdateMe(SQLDev):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLDev):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLDev):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLDev):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLDev):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLDev):
    message: str


# JSON payload containing access token
class Token(SQLDev):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLDev):
    sub: int | None = None


class NewPassword(SQLDev):
    token: str
    new_password: str
