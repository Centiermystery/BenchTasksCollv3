# Evaluation script for client-portal

import asyncio
import json
import logging
import os

from app_specific.canvas.canvas_app import CanvasApp

logger = logging.getLogger(__name__)


async def evaluate_task(task_config, state):
    """Evaluate the client-portal task."""
    canvas = CanvasApp(
        base_url=os.environ.get("CANVAS_BASE_URL"),
        api_key=os.environ.get("CANVAS_API_TOKEN"),
    )

    # Get the course from state
    course_id = state.get("course_id")
    if not course_id:
        return {"success": False, "error": "No course_id in state"}

    # Get student enrollments
    enrollments = canvas.get_course_students(course_id)
    student_ids = [e["user_id"] for e in enrollments]

    # Check if students have user or pseudo users
    has_real_users = any(uid.startswith("user") for uid in student_ids)
    has_pseudo_users = any(uid.startswith("pseudo") for uid in student_ids)

    return {
        "success": True,
        "score": 1.0 if has_real_users or has_pseudo_users else 0.0,
        "has_real_users": has_real_users,
        "has_pseudo_users": has_pseudo_users,
        "student_count": len(student_ids),
    }


def main(task_config, state):
    return asyncio.run(evaluate_task(task_config, state))
