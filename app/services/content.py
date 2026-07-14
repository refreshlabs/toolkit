from app.extensions import db
from app.models.page_content import PageContent


def get_content(key, default):
    row = db.session.get(PageContent, key)
    return row.value if row else default


def set_content(key, value):
    row = db.session.get(PageContent, key)
    if row:
        row.value = value
    else:
        row = PageContent(key=key, value=value)
        db.session.add(row)
    db.session.commit()
