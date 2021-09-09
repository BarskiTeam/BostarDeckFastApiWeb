from typing import Optional, List

from pydantic import BaseModel

from schemas_package.deck_schemas import DeckSchema


class UserBaseSchema(BaseModel):
    name: Optional[str] = None

    class Config:
        orm_mode = True


class UserSchema(UserBaseSchema):
    id: int


class UserSchemaNested(UserSchema):
    list_of_decks: List[DeckSchema]