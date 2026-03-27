STAGES = [
    "procurement",
    "planning", # added planning
    "laser_cutting", # added laser cutting
    "cutting",
    "polishing",
    "grading",
    "inventory",
    "sold"
]

def is_valid_transition(current_stage, next_stage):
    try:
        current_idx = STAGES.index(current_stage)
        next_idx = STAGES.index(next_stage)
        # Allow moving forward only (could skip)
        return next_idx > current_idx
    except ValueError:
        # If the stage is not in standard list, it might be a custom process
        return True

def get_skipped_stages(current_stage, next_stage):
    try:
        current_idx = STAGES.index(current_stage)
        next_idx = STAGES.index(next_stage)
        if next_idx > current_idx + 1:
            return STAGES[current_idx + 1:next_idx]
        return []
    except ValueError:
        return []