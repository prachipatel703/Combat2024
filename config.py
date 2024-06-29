CELERY_BEAT_SCHEDULE = {
    'assign-tasks': {
        'task': 'tasks.assign_task',
        'schedule': '0 8 * * *',  # Run every day at 8am
        'args': (1, 2)  # Report ID and Collector ID
    },
    'update-task-status': {
        'task': 'tasks.update_task_status',
        'schedule': '0 12 * * *',  # Run every day at 12pm
        'args': (1, 'in_progress')  # Task ID and Status
    }
}