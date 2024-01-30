from typing import Any, List
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from app.core.auth import Auth0User, auth

router = APIRouter()

@router.post("/", response_model=schemas.Dependency)
def create_dependency(
    *,
    db: Session = Depends(deps.get_db),
    dependency_in: schemas.DependencyCreate = Body(...),
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Create a dependency.
    """

    dependency = crud.dependency.create(db, obj_in=dependency_in, current_user=current_user)
    return dependency


@router.get("/all", response_model=List[schemas.Dependency])
def read_all_dependencies(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Retrieve all dependencies.
    """
    
    response = crud.dependency.get_multi(db=db, skip=skip, limit=limit)
    return response


@router.get("/", response_model=schemas.Dependency)
def read_dependency(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Get dependency by id.
    """
    
    return crud.dependency.get(db, id)

@router.delete("/", response_model=schemas.Dependency)
def remove_dependency(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: Auth0User = Depends(auth.get_user),
) -> Any:
    """
    Delete dependency by id.
    """
    
    return crud.dependency.remove(db=db, id=id)
