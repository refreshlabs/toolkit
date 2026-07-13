import os
from dataclasses import dataclass, field
from datetime import date

import frontmatter
import markdown
from flask import current_app


@dataclass
class Tutorial:
    slug: str
    title: str
    description: str
    category: str
    date_published: date
    html: str = field(default="", repr=False)


def _tutorials_dir():
    return current_app.config["TUTORIALS_DIR"]


def _load_all():
    tutorials = []
    directory = _tutorials_dir()
    if not os.path.isdir(directory):
        return tutorials

    for filename in os.listdir(directory):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(directory, filename)
        post = frontmatter.load(path)
        slug = filename[:-3]
        tutorials.append(
            Tutorial(
                slug=slug,
                title=post.get("title", slug.replace("-", " ").title()),
                description=post.get("description", ""),
                category=post.get("category", "Uncategorized"),
                date_published=post.get("date", date.today()),
                html=markdown.markdown(post.content, extensions=["fenced_code", "tables"]),
            )
        )
    tutorials.sort(key=lambda t: t.date_published, reverse=True)
    return tutorials


def list_tutorials(query=None, category=None):
    tutorials = _load_all()
    if category and category != "All":
        tutorials = [t for t in tutorials if t.category == category]
    if query:
        q = query.strip().lower()
        tutorials = [
            t for t in tutorials
            if q in t.title.lower() or q in t.description.lower()
        ]
    return tutorials


def get_tutorial(slug):
    for t in _load_all():
        if t.slug == slug:
            return t
    return None


def all_categories():
    return sorted({t.category for t in _load_all()})
