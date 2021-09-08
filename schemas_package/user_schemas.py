from typing import Optional

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    id: int


class UserSchemaNested(UserSchema):
    #list_of_decks: List[DeckSchema]
    pass