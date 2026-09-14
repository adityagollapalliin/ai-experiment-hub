from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


@router.get(
    "/",
    response_model=list[schemas.ProjectResponse],
)
def get_projects(
    db: Session = Depends(get_db),
):
    return db.query(models.Project).all()


@router.get(
    "/{project_id}",
    response_model=schemas.ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@router.post(
    "/",
    response_model=schemas.ProjectResponse,
    status_code=201,
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    db_project = models.Project(
        name=project.name,
        description=project.description,
    )

    db.add(db_project)

    db.commit()

    db.refresh(db_project)

    return db_project