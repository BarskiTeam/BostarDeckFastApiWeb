from typing import Optional

from pydantic import BaseModel


class FlashcardBaseSchema(BaseModel):
    avers: Optional[str] = None
    revers: Optional[str] = None
    tip: Optional[str] = None

    class Config:
        orm_mode = True


class FlashcardSchema(FlashcardBaseSchema):
    id: int
    deck_id: Optional[int] = None
    level_id: Optional[int] = None
