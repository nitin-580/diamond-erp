from app.repositories.process_repo import create_process, get_all_processes

def create_new_process(db, name, description, duration, is_custom=True):
    return create_process(db, name, description, duration, is_custom)

def list_processes(db):
    return get_all_processes(db)
