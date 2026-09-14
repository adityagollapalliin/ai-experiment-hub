from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/api/experiments",
    tags=["Metrics"],
)


@router.post(
    "/{experiment_id}/metrics",
    response_model=schemas.MetricResponse,
    status_code=201,
)
def create_metric(
    experiment_id: int,
    metric: schemas.MetricCreate,
    db: Session = Depends(get_db),
):

    experiment = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.id
            == experiment_id
        )
        .first()
    )

    if not experiment:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    db_metric = models.Metric(
        experiment_id=experiment_id,
        name=metric.name,
        value=metric.value,
        step=metric.step,
        timestamp=datetime.utcnow(),
    )

    db.add(db_metric)

    db.commit()

    db.refresh(db_metric)

    return db_metric


@router.get(
    "/{experiment_id}/metrics",
    response_model=list[schemas.MetricResponse],
)
def get_metrics(
    experiment_id: int,
    db: Session = Depends(get_db),
):

    return (
        db.query(models.Metric)
        .filter(
            models.Metric.experiment_id
            == experiment_id
        )
        .all()
    )