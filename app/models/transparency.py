from app.extensions import db


class TransparencyReport(db.Model):
    """One row per reporting period (e.g. 'Q3 2026'). Designed for an annual/quarterly
    reporting cadence - new periods are added over time, never edited in place once
    published, so the page can show a history."""

    __tablename__ = "transparency_reports"

    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(50), nullable=False, unique=True)

    donations_total_cents = db.Column(db.Integer, nullable=False, default=0)
    expense_website_cents = db.Column(db.Integer, nullable=False, default=0)
    expense_content_cents = db.Column(db.Integer, nullable=False, default=0)
    expense_events_cents = db.Column(db.Integer, nullable=False, default=0)
    expense_lab_cents = db.Column(db.Integer, nullable=False, default=0)

    btc_purchased = db.Column(db.Float, nullable=False, default=0)
    btc_mined = db.Column(db.Float, nullable=False, default=0)
    hashpower_purchased = db.Column(db.String(100), nullable=False, default="0")
    resources_published = db.Column(db.Integer, nullable=False, default=0)
    events_hosted = db.Column(db.Integer, nullable=False, default=0)

    @property
    def donations_total(self):
        return self.donations_total_cents / 100

    @property
    def expense_website(self):
        return self.expense_website_cents / 100

    @property
    def expense_content(self):
        return self.expense_content_cents / 100

    @property
    def expense_events(self):
        return self.expense_events_cents / 100

    @property
    def expense_lab(self):
        return self.expense_lab_cents / 100

    def __repr__(self):
        return f"<TransparencyReport {self.period!r}>"
