from sqlalchemy.orm import Session

from core import models
from schemas_package import user_schemas


############# CREATE #################
def create_user(db: Session, user: user_schemas.UserBaseSchema):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


############## GET #############
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_list_of_users(db: Session):
    return db.query(models.User).all()


############# DELETE ###############
def delete_user(db: Session, user_id: int):
    try:
        obj_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
        if obj_to_delete is None:
            return None
        db.delete(obj_to_delete)
        db.commit()
        result_str = f"User with id {user_id} was deleted"
        return result_str
    except Exception as e:
        result_str = "We caught exception when was tried deleted user with id" + str(user_id)
        print(result_str)
        return result_str


def delete_all_users(db: Session):
    all_users = db.query(models.User)
    if all_users is not None:
        all_users.delete()
        db.commit()
        return "All users was deleted"
    else:
        return None
