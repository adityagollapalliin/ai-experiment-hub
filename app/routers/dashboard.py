from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import models
from app.database import get_db


router = APIRouter(
    tags=["Dashboard"],
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    project_count = (
        db.query(models.Project)
        .count()
    )

    experiment_count = (
        db.query(models.Experiment)
        .count()
    )

    completed_count = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.status == "completed"
        )
        .count()
    )

    running_count = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.status == "running"
        )
        .count()
    )

    failed_count = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.status == "failed"
        )
        .count()
    )

    recent_experiments = (
        db.query(models.Experiment)
        .order_by(
            models.Experiment.created_at.desc()
        )
        .limit(8)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "project_count": project_count,
            "experiment_count": experiment_count,
            "completed_count": completed_count,
            "running_count": running_count,
            "failed_count": failed_count,
            "recent_experiments": recent_experiments,
        },
    )


@router.get("/experiments/{experiment_id}")
def experiment_detail(
    experiment_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    experiment = (
        db.query(models.Experiment)
        .filter(
            models.Experiment.id == experiment_id
        )
        .first()
    )

    if experiment is None:
        raise HTTPException(
            status_code=404,
            detail="Experiment not found",
        )

    metrics = (
        db.query(models.Metric)
        .filter(
            models.Metric.experiment_id
            == experiment_id
        )
        .order_by(
            models.Metric.step,
            models.Metric.name,
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="experiment_detail.html",
        context={
            "experiment": experiment,
            "metrics": metrics,
        },
    )