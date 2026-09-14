from fastapi import APIRouter, Depends, Request
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
    project_count = db.query(
        models.Project
    ).count()

    experiment_count = db.query(
        models.Experiment
    ).count()

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