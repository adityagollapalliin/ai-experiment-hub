from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)

from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    experiments = relationship(
        "Experiment",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
    )

    name = Column(String, nullable=False)

    model_name = Column(String, nullable=False)

    model_repo = Column(String, nullable=True)

    dataset_name = Column(String, nullable=False)

    dataset_repo = Column(String, nullable=True)

    training_type = Column(String, nullable=True)

    learning_rate = Column(Float, nullable=True)

    batch_size = Column(Integer, nullable=True)

    epochs = Column(Integer, nullable=True)

    optimizer = Column(String, nullable=True)

    lora_rank = Column(Integer, nullable=True)

    gradient_accumulation_steps = Column(
        Integer,
        nullable=True,
    )

    max_sequence_length = Column(
        Integer,
        nullable=True,
    )

    seed = Column(Integer, nullable=True)

    status = Column(String, nullable=False)

    final_train_loss = Column(Float, nullable=True)

    eval_accuracy = Column(Float, nullable=True)

    gpu = Column(String, nullable=True)

    training_duration_minutes = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(DateTime)

    finished_at = Column(
        DateTime,
        nullable=True,
    )

    notes = Column(Text, nullable=True)

    project = relationship(
        "Project",
        back_populates="experiments",
    )

    metrics = relationship(
        "Metric",
        back_populates="experiment",
        cascade="all, delete-orphan",
    )


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)

    experiment_id = Column(
        Integer,
        ForeignKey("experiments.id"),
        nullable=False,
    )

    name = Column(String, nullable=False)

    value = Column(Float, nullable=False)

    step = Column(Integer, nullable=False)

    timestamp = Column(DateTime)

    experiment = relationship(
        "Experiment",
        back_populates="metrics",
    )