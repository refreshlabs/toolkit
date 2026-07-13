from flask import Blueprint, render_template

from app.models import TransparencyReport

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/donate")
def donate():
    return render_template("donate.html")


@main_bp.route("/transparency")
def transparency():
    reports = TransparencyReport.query.order_by(TransparencyReport.id.desc()).all()
    return render_template("transparency.html", reports=reports)


@main_bp.route("/github")
def github():
    dev_status = [
        ("Website", "Published"),
        ("Dashboard", "In Development"),
        ("Educational Tools", "Planned"),
        ("Documentation", "In Progress"),
    ]
    return render_template("github.html", dev_status=dev_status)
