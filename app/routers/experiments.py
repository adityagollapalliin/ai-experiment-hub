from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/api/experiments",
    tags=["Experiments"],
)


@router.get(
    "/",
    response_model=list[schemas.ExperimentResponse],
)
def get_experiments(
    db: Session = Depends(get_db),
):
    return db.query(models.Experiment).all()


@router.get(
    "/{experiment_id}",
    response_model=schemas.ExperimentResponse,
)
def get_experiment(
    experiment_id: int,
    db: Session = Depends(get_db),
):
    experiment = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.id == experiment_id
        )
        .first()
    )

    if not experiment:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    return experiment


@router.post(
    "/",
    response_model=schemas.ExperimentResponse,
    status_code=201,
)
def create_experiment(
    experiment: schemas.ExperimentCreate,
    db: Session = Depends(get_db),
):

    project = (
        db.query(models.Project)
        .filter(
            models.Project.id
            == experiment.project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    db_experiment = models.Experiment(
        **experiment.model_dump()
    )

    db.add(db_experiment)

    db.commit()

    db.refresh(db_experiment)

    return db_experiment