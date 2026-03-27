from sqlalchemy.orm import Session
from sqlalchemy import func

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

    from app.domain.stage_rules import get_skipped_stages
    
    skipped = get_skipped_stages(old_stage, new_stage)
    
    description = f"Moved from {old_stage} to {new_stage}."
    is_skipped = False
    
    if skipped:
        description += f" Skipped: {', '.join(skipped)}"
        is_skipped = True

    # 3. Update diamond stage
    updated = update_diamond_stage(db, diamond_id, new_stage)

    # 4. Create process log
    create_process_log(db, {
        "id": f"log_{diamond_id}_{new_stage}_{int(func.now().timestamp())}",
        "diamond_id": diamond_id,
        "from_stage": old_stage,
        "to_stage": new_stage,
        "description": description,
        "is_skipped": is_skipped
    })

    # 5. Handle Incentives (Integration)
    if new_stage == "completed" and updated.current_worker_id:
        from app.services.incentive_service import add_incentive
        add_incentive(db, updated.current_worker_id, diamond_id)

    return updated