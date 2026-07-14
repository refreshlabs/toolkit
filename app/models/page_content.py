from app.extensions import db


class PageContent(db.Model):
    __tablename__ = "page_content"

    key = db.Column(db.String(200), primary_key=True)
    value = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<PageContent {self.key!r}>"
