from sqlalchemy.orm import Session

from app.repositories.diamond_repo import (
    create_diamond,
    get_diamond,
    update_diamond_stage
)

from app.repositories.process_log_repo import create_process_log

from app.domain.stage_rules import is_valid_transition


def create_new_diamond(db: Session, data: dict):
    return create_diamond(db, data)


def update_stage(db: Session, diamond_id: str, new_stage: str):
    # 1. Get diamond
    diamond = get_diamond(db, diamond_id)

    if not diamond:
        raise Exception("Diamond not found")

    old_stage = diamond.stage

    # 2. Validate stage transition
    if not is_valid_transition(old_stage, new_stage):
        raise Exception(f"Invalid transition: {old_stage} → {new_stage}")

    # 3. Update diamond stage
    updated = update_diamond_stage(db, diamond_id, new_stage)

    # 4. Create process log
    create_process_log(db, {
        "id": f"log_{diamond_id}_{new_stage}",
        "diamond_id": diamond_id,
        "from_stage": old_stage,
        "to_stage": new_stage
    })

    return updated