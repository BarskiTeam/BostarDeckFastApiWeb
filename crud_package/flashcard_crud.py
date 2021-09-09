


########### CREATE #################
from typing import Optional

from sqlalchemy.orm import Session

from core import models
from schemas_package import flashcard_schemas


################## CREATE #####################
def create_flashcard(db: Session, flashcard: flashcard_schemas.FlashcardBaseSchema, deck_id: Optional[int] = None,
                     level_id: Optional[int] = None):
    try:
        db_flashcard = models.Flashcard(avers=flashcard.avers,
                                        revers=flashcard.revers,
                                        tip=flashcard.tip,
                                        deck_id=deck_id,
                                        level_id=level_id)
        db.add(db_flashcard)
        db.commit()
        db.refresh(db_flashcard)
    except Exception as e:
        print(f"Error was raised while creating record in database. Check deck with this id {deck_id} and level with this id {level_id} exist.")
        return None
    return db_flashcard


################## GET ###################
def get_flashcard(db: Session, flashcard_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id)


def get_list_of_flashcards(db: Session):
    return db.query(models.Flashcard).all()


################## DELETE #################
def delete_flashcard_by_id(db: Session, flashcard_id: int):
    try:
        obj_to_delete = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = f"Flashcard with id {flashcard_id} was deleted"
    except Exception as e:
        result_str = "Except was caught while was tried deleted flashcard with id" + str(flashcard_id)
        print(result_str)
        return result_str


def delete_all_flashcards(db: Session):
    all_flashcards = db.query(models.Flashcard)
    if all_flashcards is not None:
        all_flashcards.delete()
        db.commit()
        return "All flashcard was deleted"
    else:
        return None
