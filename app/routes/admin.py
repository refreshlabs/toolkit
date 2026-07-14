import hmac
import secrets
import time
from datetime import date
from functools import wraps

from flask import Blueprint, current_app, jsonify, redirect, render_template, request, session, url_for

from app.extensions import db
from app.models.transparency import ExpenseSubfield, TransparencyReport
from app.services.content import set_content
from app.services import tutorials as tutorials_service

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

_MAX_ATTEMPTS = 5
_LOCKOUT_SECONDS = 900
_failed_attempts = {}


def _client_ip():
    return request.remote_addr or "unknown"


def _is_locked_out(ip):
    _, locked_until = _failed_attempts.get(ip, (0, 0))
    return locked_until > time.time()


def _register_failure(ip):
    count, _ = _failed_attempts.get(ip, (0, 0))
    count += 1
    locked_until = time.time() + _LOCKOUT_SECONDS if count >= _MAX_ATTEMPTS else 0
    _failed_attempts[ip] = (count, locked_until)


def _clear_failures(ip):
    _failed_attempts.pop(ip, None)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        ip = _client_ip()
        if _is_locked_out(ip):
            error = "Too many failed attempts. Try again later."
        else:
            password = request.form.get("password", "")
            expected = current_app.config["ADMIN_PASSWORD"]
            if hmac.compare_digest(password, expected):
                _clear_failures(ip)
                session.clear()
                session.permanent = True
                session["is_admin"] = True
                session["csrf_token"] = secrets.token_hex(16)
                return redirect(url_for("main.home"))
            _register_failure(ip)
            error = "Incorrect password."
    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))


def _check_api_auth():
    if not session.get("is_admin"):
        return jsonify({"error": "unauthorized"}), 403
    token = request.headers.get("X-CSRF-Token", "")
    if not hmac.compare_digest(token, session.get("csrf_token", "")):
        return jsonify({"error": "invalid csrf token"}), 403
    return None


@admin_bp.route("/api/content", methods=["PATCH"])
def update_content():
    auth_error = _check_api_auth()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    key = data.get("key")
    value = data.get("value")
    if not isinstance(key, str) or not key or not isinstance(value, str):
        return jsonify({"error": "invalid payload"}), 400
    if len(key) > 200 or len(value) > 5000:
        return jsonify({"error": "payload too large"}), 400

    set_content(key, value)
    return jsonify({"ok": True})


@admin_bp.route("/api/expense-subfields", methods=["POST"])
def create_expense_subfield():
    auth_error = _check_api_auth()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    report_id = data.get("report_id")
    label = data.get("label")
    description = data.get("description") or None
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid amount"}), 400

    if not isinstance(label, str) or not label.strip():
        return jsonify({"error": "label is required"}), 400
    if len(label) > 200:
        return jsonify({"error": "label too long"}), 400
    if description is not None and len(description) > 1000:
        return jsonify({"error": "description too long"}), 400
    if amount < 0:
        return jsonify({"error": "amount must be non-negative"}), 400

    report = db.session.get(TransparencyReport, report_id)
    if report is None:
        return jsonify({"error": "report not found"}), 404

    next_order = len(report.expense_subfields)
    subfield = ExpenseSubfield(
        report_id=report.id,
        label=label.strip(),
        amount_cents=round(amount * 100),
        description=description,
        sort_order=next_order,
    )
    db.session.add(subfield)
    db.session.commit()
    return jsonify({
        "id": subfield.id,
        "label": subfield.label,
        "amount": subfield.amount,
        "description": subfield.description,
    })


@admin_bp.route("/api/expense-subfields/<int:subfield_id>", methods=["DELETE"])
def delete_expense_subfield(subfield_id):
    auth_error = _check_api_auth()
    if auth_error:
        return auth_error

    subfield = db.session.get(ExpenseSubfield, subfield_id)
    if subfield is None:
        return jsonify({"error": "not found"}), 404

    db.session.delete(subfield)
    db.session.commit()
    return jsonify({"ok": True})


@admin_bp.route("/tutorials/new", methods=["GET", "POST"])
@login_required
def new_tutorial():
    form = {
        "title": "",
        "description": "",
        "category": "",
        "date": date.today().isoformat(),
        "body": "",
    }
    errors = []
    categories = tutorials_service.all_categories()

    if request.method == "POST":
        token = request.form.get("csrf_token", "")
        if not hmac.compare_digest(token, session.get("csrf_token", "")):
            errors.append("Your session expired. Please try again.")

        form["title"] = request.form.get("title", "").strip()
        form["description"] = request.form.get("description", "").strip()
        form["category"] = request.form.get("category", "").strip()
        form["date"] = request.form.get("date", "").strip()
        form["body"] = request.form.get("body", "").strip()

        if not form["title"]:
            errors.append("Title is required.")
        if not form["description"]:
            errors.append("Description is required.")
        if form["category"] not in categories:
            errors.append("Choose a valid category.")
        if not form["body"]:
            errors.append("Body is required.")

        try:
            date_published = date.fromisoformat(form["date"]) if form["date"] else date.today()
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")
            date_published = date.today()

        slug = tutorials_service.slugify(form["title"]) if form["title"] else ""
        if form["title"] and not slug:
            errors.append("Title must contain at least one letter or number.")
        elif slug and tutorials_service.slug_exists(slug):
            errors.append(f'A tutorial with slug "{slug}" already exists. Choose a different title.')

        if not errors:
            tutorials_service.save_tutorial(
                slug=slug,
                title=form["title"],
                description=form["description"],
                category=form["category"],
                date_published=date_published,
                body=form["body"],
            )
            return redirect(url_for("learn.tutorial_detail", slug=slug))

    return render_template("admin/tutorial_form.html", form=form, errors=errors, categories=categories)
