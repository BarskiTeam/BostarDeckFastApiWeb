from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from crud_package import deck_crud
from database import SessionLocal
from schemas_package import deck_schemas

router = APIRouter(
    prefix="/decks",
    tags=["decks"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#################### POST ###################
@router.post("/", response_model=deck_schemas.DeckSchema)
async def create_deck(deck: deck_schemas.DeckBaseSchema, db: Session = Depends(get_db)):
    created_deck = deck_crud.create_deck(db=db, deck=deck)
    if created_deck is None:
        raise HTTPException(status_code=404, detail="Deck wasn't created")
    else:
        return created_deck


@router.post("/id_user={user_id}", response_model=deck_schemas.DeckSchema)
async def create_deck_for_user(user_id: int, deck: deck_schemas.DeckBaseSchema, db: Session = Depends(get_db)):
    created_deck = deck_crud.create_deck(db=db, deck=deck, user_id=user_id)
    if created_deck is None:
        raise HTTPException(status_code=404, detail="Decks wasn't created, are you sure that user exist?")
    else:
        return created_deck


##################### GET #####################
@router.get("/all", response_model=List[deck_schemas.DeckSchema])
async def get_all_decks(db: Session = Depends(get_db)):
    list_of_decks = deck_crud.get_list_of_decks(db)
    if list_of_decks is None:
        raise HTTPException(status_code=404, detail="Decks has not found")
    else:
        return list_of_decks


@router.get("/id_deck={deck_id}", response_model=deck_schemas.DeckSchema)
async def get_deck_by_id(deck_id: int, db: Session = Depends(get_db)):
    deck = deck_crud.get_deck(db, deck_id=deck_id)
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck with this id dont exist")
    return deck


################ DELETE ##################
@router.delete("/id={deck_id}")
async def delete_deck_by_id(deck_id: int, db: Session = Depends(get_db)):
    result_str = deck_crud.delete_deck_by_id(db, deck_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"deck with id {deck_id} not exist"})


@router.delete("/all")
async def delete_all_decks(db: Session = Depends(get_db)):
    result_str = deck_crud.delete_all_decks(db)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "I can't delete all decks"})

