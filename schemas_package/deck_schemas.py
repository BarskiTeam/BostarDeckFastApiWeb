from typing import Optional, List

from pydantic import BaseModel

from schemas_package.flashcard_schemas import FlashcardSchema


class DeckBaseSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[str] = None
    public: Optional[bool]

    class Config:
        orm_mode = True


class DeckUpdateSchema(DeckBaseSchema):
    user_id: Optional[int] = None


class DeckSchema(DeckBaseSchema):
    id: int
    user_id: Optional[int] = None


class DeckNestedSchema(DeckSchema):
    list_of_flashcards: List[FlashcardSchema]