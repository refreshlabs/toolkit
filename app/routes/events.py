from flask import Blueprint, render_template

from app.models import Event

events_bp = Blueprint("events", __name__, url_prefix="/events")


@events_bp.route("/")
def index():
    upcoming = Event.query.order_by(Event.event_date.asc()).all()
    return render_template("events.html", events=upcoming)
