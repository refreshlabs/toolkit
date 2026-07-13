from app.extensions import db


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=False, default="")
    registration_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f"<Event {self.title!r}>"
