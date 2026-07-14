from app.extensions import db


class ExpenseSubfield(db.Model):
    """Ad-hoc extra expense line item an admin can add under a report's
    Expenses section, beyond the fixed categories."""

    __tablename__ = "expense_subfields"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("transparency_reports.id"), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    amount_cents = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    report = db.relationship("TransparencyReport", backref=db.backref(
        "expense_subfields", order_by="ExpenseSubfield.sort_order", cascade="all, delete-orphan"
    ))

    @property
    def amount(self):
        return self.amount_cents / 100

    def __repr__(self):
        return f"<ExpenseSubfield {self.label!r}>"


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
    expense_irs_cents = db.Column(db.Integer, nullable=False, default=0)
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
    def expense_irs(self):
        return self.expense_irs_cents / 100

    @property
    def expense_lab(self):
        return self.expense_lab_cents / 100

    def __repr__(self):
        return f"<TransparencyReport {self.period!r}>"
