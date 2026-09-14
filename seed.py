import json
from datetime import datetime
from pathlib import Path

from app.database import SessionLocal, Base, engine
from app.models import Project, Experiment, Metric


DATA_FILE = Path("data/seed_data.json")


def parse_datetime(value):
    if not value:
        return None

    return datetime.fromisoformat(value)


def seed_database():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        existing_projects = db.query(Project).count()

        if existing_projects > 0:
            print(
                "Database already contains data."
            )
            return

        for item in data["projects"]:

            project = Project(
                id=item["id"],
                name=item["name"],
                description=item["description"],
                created_at=parse_datetime(
                    item["created_at"]
                ),
            )

            db.add(project)

        db.commit()

        for item in data["experiments"]:

            experiment = Experiment(
                id=item["id"],
                project_id=item["project_id"],
                name=item["name"],
                model_name=item["model_name"],
                model_repo=item["model_repo"],
                dataset_name=item["dataset_name"],
                dataset_repo=item["dataset_repo"],
                training_type=item["training_type"],
                learning_rate=item["learning_rate"],
                batch_size=item["batch_size"],
                epochs=item["epochs"],
                optimizer=item["optimizer"],
                lora_rank=item["lora_rank"],
                gradient_accumulation_steps=item[
                    "gradient_accumulation_steps"
                ],
                max_sequence_length=item[
                    "max_sequence_length"
                ],
                seed=item["seed"],
                status=item["status"],
                final_train_loss=item[
                    "final_train_loss"
                ],
                eval_accuracy=item[
                    "eval_accuracy"
                ],
                gpu=item["gpu"],
                training_duration_minutes=item[
                    "training_duration_minutes"
                ],
                created_at=parse_datetime(
                    item["created_at"]
                ),
                finished_at=parse_datetime(
                    item["finished_at"]
                ),
                notes=item["notes"],
            )

            db.add(experiment)

        db.commit()

        for item in data["metrics"]:

            metric = Metric(
                id=item["id"],
                experiment_id=item[
                    "experiment_id"
                ],
                name=item["name"],
                value=item["value"],
                step=item["step"],
                timestamp=parse_datetime(
                    item["timestamp"]
                ),
            )

            db.add(metric)

        db.commit()

        print("Seed complete.")

        print(
            f"Projects: "
            f"{db.query(Project).count()}"
        )

        print(
            f"Experiments: "
            f"{db.query(Experiment).count()}"
        )

        print(
            f"Metrics: "
            f"{db.query(Metric).count()}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()