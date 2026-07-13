from flask import Blueprint, abort, render_template, request

from app.models import Video
from app.models.video import CATEGORIES
from app.services import tutorials as tutorials_service

learn_bp = Blueprint("learn", __name__, url_prefix="/learn")


@learn_bp.route("/")
def index():
    return render_template("learn/index.html")


@learn_bp.route("/videos")
def videos():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")

    videos_query = Video.query
    if category and category != "All":
        videos_query = videos_query.filter_by(category=category)
    if query:
        like = f"%{query}%"
        videos_query = videos_query.filter(
            Video.title.ilike(like) | Video.description.ilike(like)
        )
    results = videos_query.order_by(Video.published_date.desc()).all()

    return render_template(
        "learn/videos.html",
        videos=results,
        categories=CATEGORIES,
        selected_category=category,
        query=query,
    )


@learn_bp.route("/tutorials")
def tutorials():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")

    results = tutorials_service.list_tutorials(query=query, category=category)

    return render_template(
        "learn/tutorials.html",
        tutorials=results,
        categories=tutorials_service.all_categories(),
        selected_category=category,
        query=query,
    )


@learn_bp.route("/tutorials/<slug>")
def tutorial_detail(slug):
    tutorial = tutorials_service.get_tutorial(slug)
    if tutorial is None:
        abort(404)
    return render_template("learn/tutorial_detail.html", tutorial=tutorial)
