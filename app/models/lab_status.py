from datetime import datetime

from app.extensions import db


class LabStatus(db.Model):
    """Current Living Laboratory dashboard snapshot. One row is the live record
    (highest id). Placeholder values now; intended to later be updated by a
    scheduled job pulling from a mining pool API / node / power monitor instead
    of being edited by hand."""

    __tablename__ = "lab_status"

    id = db.Column(db.Integer, primary_key=True)
    hashrate = db.Column(db.String(100), nullable=False, default="Coming Soon")
    mining_provider = db.Column(db.String(200), nullable=False, default="Coming Soon")
    mining_period = db.Column(db.String(100), nullable=False, default="Coming Soon")
    btc_produced = db.Column(db.String(100), nullable=False, default="Coming Soon")
    mining_costs = db.Column(db.String(100), nullable=False, default="Coming Soon")
    estimated_btc_value = db.Column(db.String(100), nullable=False, default="Coming Soon")
    educational_content_produced = db.Column(db.String(100), nullable=False, default="Coming Soon")
    status = db.Column(db.String(100), nullable=False, default="Planning")
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def current():
        return LabStatus.query.order_by(LabStatus.id.desc()).first()

    def __repr__(self):
        return f"<LabStatus {self.status!r}>"
