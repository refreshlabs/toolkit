from datetime import date

from app.extensions import db

CATEGORIES = ["Bitcoin", "Mining", "Open Source", "HAM Radio", "Networking", "Digital Literacy"]


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    category = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.Date, nullable=False, default=date.today)
    external_url = db.Column(db.String(500), nullable=True)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    is_placeholder = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Video {self.title!r}>"
