from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from crud_package import user_crud
from database import SessionLocal
from schemas_package import user_schemas

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not"}}
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


################ POST ###############
@router.post("/", response_model=user_schemas.UserBaseSchema)
async def create_user(user: user_schemas.UserBaseSchema, db: Session = Depends(get_db)):
    return user_crud.create_user(db=db, user=user)


############### GET ################
@router.get("/all", response_model=List[user_schemas.UserSchema])
async def get_all_users(db: Session = Depends(get_db)):
    list_of_users = user_crud.get_list_of_users(db)
    if list_of_users is None:
        raise HTTPException(status_code=404, detail="Users has not found")
    return list_of_users


@router.get("/id_user={user_id}", response_model=user_schemas.UserSchema)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User by this id not exist")
    return user


################ DELETE ##################
@router.delete("/id={user_id}")
async def delete_id_user(user_id: int, db: Session = Depends(get_db)):
    result_str = user_crud.delete_user(db, user_id)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    elif result_str is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"user with id {user_id} not exist"})


@router.delete("/all")
async def delete_all_users(db: Session = Depends(get_db)):
    result_str = user_crud.delete_all_users(db)
    if result_str is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": result_str})
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "I can't delete all users"})
