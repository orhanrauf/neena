from typing import Any, Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.auth import Auth0User, auth

router = APIRouter()

#TODO: Fix User endpoints

@router.put("/", response_model=str)
def update_user(
    *,  
    db: Session = Depends(deps.get_db),
    obj_in: schemas.UserUpdate,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Update user.
    """
    # current_user_data = jsonable_encoder(current_user)
    # user_in = schemas.UserUpdate(**current_user_data)
    # if obj_in.password is not None:
    #     user_in.password = obj_in.password
    # if obj_in.full_name is not None:
    #     user_in.full_name = obj_in.full_name
    # if obj_in.email is not None:
    #     check_user = crud.user.get_by_email(db, email=obj_in.email)
    #     if check_user and check_user.email != current_user.email:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="This username is not available.",
    #         )
    #     user_in.email = obj_in.email
    # user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return "The API endpoint is not yet implemented."


@router.get("/", response_model=str) 
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: Auth0User = Depends(auth.get_user)
) -> Any:
    """
    Get current user.
    """
    
    user = crud.user.get_by_email(db, email=current_user.email)
    
    return user


# @router.get("/all", response_model=List[schemas.User])
# def read_all_users(
#     *,
#     db: Session = Depends(deps.get_db),
#     skip: int = 0,
#     limit: int = 100,
#     current_user: Auth0User = Depends(auth.get_user),
# ) -> Any:
#     """
#     Retrieve all current users.
#     """
#     return crud.user.get_multi(db=db, skip=skip, limit=limit)

@router.post("/create_if_not_exists", response_model=schemas.User)
def create_user_if_not_exists(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create new user in database. Verifies validity through signed auth0 token.
    """
    
    if user_in.email != current_user.email:
        raise HTTPException(
            status_code=400,
            detail="You are not authorized to create this user.",
        )
    
    user = crud.user.get_by_email(db, email=user_in.email)
    
    # If user exists, return user
    if user:
        return user
        
    # If user does not exist, create user
    user = crud.user.create(db, obj_in=user_in)
    return user