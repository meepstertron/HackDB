from flask import Blueprint, jsonify, request
from app.models import Item
from app import db, rq
import logging

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify(message='Hello from HackDB!')

@main.route('/enqueue-task')
def enqueue_task():
    from app.tasks import example_task
    job = rq.enqueue(example_task, 2, 3)
    return jsonify(job_id=job.get_id(), status=job.get_status())



