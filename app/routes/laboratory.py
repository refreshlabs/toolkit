from flask import Blueprint, render_template

from app.models import LabStatus

laboratory_bp = Blueprint("laboratory", __name__, url_prefix="/living-laboratory")


@laboratory_bp.route("/")
def index():
    status = LabStatus.current()
    return render_template("laboratory/index.html", status=status)


@laboratory_bp.route("/economics")
def economics():
    economics_snapshot = {
        "period": "Q3 2026",
        "hashpower_purchased": "Coming Soon",
        "mining_expenses": "Coming Soon",
        "bitcoin_produced": "Coming Soon",
        "educational_outputs": "Coming Soon",
    }
    return render_template("laboratory/economics.html", snapshot=economics_snapshot)
