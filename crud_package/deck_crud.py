from typing import Optional

from sqlalchemy.orm import Session

from core import models
from schemas_package import deck_schemas


################# CREATE ###################
def create_deck(db: Session, deck: deck_schemas.DeckBaseSchema, user_id: Optional[int] = None):
    try:
        db_deck = models.Deck(name=deck.name,
                              tag=deck.tag,
                              description=deck.description,
                              public=deck.public,
                              user_id=user_id)

        db.add(db_deck)
        db.commit()
        db.refresh(db_deck)
    except Exception as e:
        print(f"Raise error in create record in database, check user with this id {user_id} exist")
        return None
    return db_deck


#################### GET #####################
def get_deck(db: Session, deck_id: int):
    return db.query(models.Deck).filter(models.Deck.id == deck_id).first()


def get_list_of_decks(db: Session):
    return db.query(models.Deck).all()


################ DELETE #############
def delete_deck_by_id(db: Session, deck_id: int):
    try:
        obj_to_delete = db.query(models.Deck).filter(models.Deck.id == deck_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = f"Deck with id {deck_id} was deleted"
        return result_str
    except Exception as e:
        result_str = "We caught exception when was tried deleted deck with id" + str(deck_id)
        print(result_str)
        return result_str


def delete_all_decks(db: Session):
    all_decks = db.query(models.Deck)
    if all_decks is not None:
        all_decks.delete()
        db.commit()
        return "All decks was deleted"
    else:
        return None