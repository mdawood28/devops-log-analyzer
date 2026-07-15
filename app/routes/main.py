from flask import Blueprint, render_template

from app.models import LogFile, LogEntry, db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    total_files = LogFile.query.count()
    total_entries = LogEntry.query.count()

    level_counts = {
        "INFO": LogEntry.query.filter_by(level="INFO").count(),
        "WARNING": LogEntry.query.filter_by(level="WARNING").count(),
        "ERROR": LogEntry.query.filter_by(level="ERROR").count(),
        "DEBUG": LogEntry.query.filter_by(level="DEBUG").count(),
        "CRITICAL": LogEntry.query.filter_by(level="CRITICAL").count(),
    }

    recent_files = LogFile.query.order_by(LogFile.uploaded_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total_files=total_files,
        total_entries=total_entries,
        level_counts=level_counts,
        recent_files=recent_files,
    )
