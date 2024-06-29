from celery import shared_task
from app import celery

@shared_task
def assign_task(report_id, collector_id):
    # Assign task to collector
    task = Task(report_id=report_id, collector_id=collector_id)
    db.session.add(task)
    db.session.commit()
    return "Task assigned successfully"

@shared_task
def update_task_status(task_id, status):
    # Update task status
    task = Task.query.get(task_id)
    if task:
        task.status = status
        db.session.commit()
        return "Task status updated successfully"
    return "Task not found"