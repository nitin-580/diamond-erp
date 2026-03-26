STAGES = [
    "procurement",
    "cutting",
    "polishing",
    "grading",
    "inventory",
    "sold"
]

def is_valid_transition(current_stage, next_stage):
    try:
        return STAGES.index(next_stage) == STAGES.index(current_stage) + 1
    except ValueError:
        return False