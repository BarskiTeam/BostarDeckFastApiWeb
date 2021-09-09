from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from crud_package import flashcard_crud
from database import SessionLocal
from schemas_package import flashcard_schemas

router = APIRouter(
    prefix="/flashcards",
    tags=["flashcards"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#################### POST ###################
@router.post("/", response_model=flashcard_schemas.FlashcardSchema)
async def create_flashcard(flashcard: flashcard_schemas.FlashcardBaseSchema, db: Session = Depends(get_db)):
    created_flashcard = flashcard_crud.create_flashcard(db=db, flashcard=flashcard)
    if created_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard wasn't created")
    else:
        return created_flashcard


@router.post("/id_deck={deck_id}/id_level={level_id}", response_model=flashcard_schemas.FlashcardSchema)
async def create_flashcard_with_deck_and_level(deck_id: int, level_id: int, flashcard: flashcard_schemas.FlashcardBaseSchema, db: Session = Depends(get_db)):
    created_flashcard = flashcard_crud.create_flashcard(db=db, flashcard=flashcard, deck_id=deck_id, level_id=level_id)
    if created_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard wasn't created")
    else:
        return created_flashcard


##################### GET #####################
@router.get("/all", response_model=List[flashcard_schemas.FlashcardSchema])
async def get_all_flashcards(db: Session = Depends(get_db)):
    list_of_flashcards = flashcard_crud.get_list_of_flashcards(db=db)
    if list_of_flashcards is None:
        raise HTTPException(status_code=404, detail="Flashcards wasn't found")
    return list_of_flashcards


@router.get("/id_flashcard={flashcard_id}", response_model=flashcard_schemas.FlashcardSchema)
async def get_flashcard_by_id(flashcard_id: int, db: Session = Depends(get_db)):
    deck = flashcard_crud.get_flashcard(db, flashcard_id=flashcard_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck with this id dont exist")
    return deck


################ DELETE ##################
@router.delete("/id={flashcard_id}")
async def delete_id_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    result_str = flashcard_crud.delete_flashcard_by_id(db, flashcard_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"flashcard with id {flashcard_id} not exist"})


@router.delete("/all")
async def delete_all_flashcard(db: Session = Depends(get_db)):
    result_str = flashcard_crud.delete_all_flashcards(db)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "I can't delete all flashcards"})


