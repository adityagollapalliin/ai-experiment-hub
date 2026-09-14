from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ExperimentBase(BaseModel):
    project_id: int
    name: str

    model_name: str
    model_repo: str | None = None

    dataset_name: str
    dataset_repo: str | None = None

    training_type: str | None = None

    learning_rate: float | None = None
    batch_size: int | None = None
    epochs: int | None = None

    optimizer: str | None = None

    lora_rank: int | None = None

    gradient_accumulation_steps: int | None = None

    max_sequence_length: int | None = None

    seed: int | None = None

    status: str

    final_train_loss: float | None = None

    eval_accuracy: float | None = None

    gpu: str | None = None

    training_duration_minutes: int | None = None

    notes: str | None = None


class ExperimentCreate(ExperimentBase):
    pass


class ExperimentResponse(ExperimentBase):
    id: int
    created_at: datetime | None = None
    finished_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class MetricBase(BaseModel):
    name: str
    value: float
    step: int


class MetricCreate(MetricBase):
    pass


class MetricResponse(MetricBase):
    id: int
    experiment_id: int
    timestamp: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )