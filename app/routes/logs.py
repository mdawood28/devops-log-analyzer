import os
import logging

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
)
from werkzeug.utils import secure_filename

from app.models import LogFile, LogEntry, db
from app.forms import UploadForm, SearchForm
from app.services import LogParser

logger = logging.getLogger(__name__)

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)

        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)

        counter = 1
        base, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(upload_dir, filename)
            counter += 1

        file.save(filepath)
        file_size = os.path.getsize(filepath)

        log_file = LogFile(
            filename=filename,
            original_filename=secure_filename(file.filename),
            file_size=file_size,
            file_path=filepath,
        )
        db.session.add(log_file)
        db.session.commit()

        parser = LogParser()
        entries = parser.parse_file(filepath)
        counts = parser.count_levels(entries)

        for entry_data in entries:
            entry = LogEntry(
                log_file_id=log_file.id,
                timestamp=entry_data.get("timestamp", ""),
                level=entry_data["level"],
                message=entry_data["message"],
                line_number=entry_data["line_number"],
                raw_line=entry_data.get("raw_line", ""),
            )
            db.session.add(entry)

        log_file.entry_count = len(entries)
        log_file.info_count = counts["INFO"]
        log_file.warning_count = counts["WARNING"]
        log_file.error_count = counts["ERROR"]
        log_file.debug_count = counts["DEBUG"]
        log_file.critical_count = counts["CRITICAL"]
        db.session.commit()

        logger.info("Uploaded and parsed file: %s (%d entries)", filename, len(entries))
        flash(
            f"File '{filename}' uploaded and parsed successfully "
            f"({len(entries)} entries found).",
            "success",
        )
        return redirect(url_for("logs.detail", file_id=log_file.id))

    return render_template("upload.html", form=form)


@logs_bp.route("/")
def index():
    form = SearchForm(request.args, meta={"csrf": False})
    query = LogFile.query

    if form.filename.data:
        query = query.filter(LogFile.filename.ilike(f"%{form.filename.data}%"))
    if form.level.data:
        query = query.filter(getattr(LogFile, f"{form.level.data.lower()}_count") > 0)
    if form.date.data:
        query = query.filter(db.func.date(LogFile.uploaded_at) == form.date.data)

    query = query.order_by(LogFile.uploaded_at.desc())
    files = query.all()

    return render_template("logs_list.html", files=files, form=form)


@logs_bp.route("/<int:file_id>")
def detail(file_id):
    log_file = LogFile.query.get_or_404(file_id)
    level_filter = request.args.get("level", "")

    entries_query = LogEntry.query.filter_by(log_file_id=log_file.id)
    if level_filter:
        entries_query = entries_query.filter_by(level=level_filter.upper())

    entries = entries_query.order_by(LogEntry.line_number).all()

    level_breakdown = {
        "INFO": LogEntry.query.filter_by(log_file_id=log_file.id, level="INFO").count(),
        "WARNING": LogEntry.query.filter_by(
            log_file_id=log_file.id, level="WARNING"
        ).count(),
        "ERROR": LogEntry.query.filter_by(
            log_file_id=log_file.id, level="ERROR"
        ).count(),
        "DEBUG": LogEntry.query.filter_by(
            log_file_id=log_file.id, level="DEBUG"
        ).count(),
        "CRITICAL": LogEntry.query.filter_by(
            log_file_id=log_file.id, level="CRITICAL"
        ).count(),
    }

    return render_template(
        "log_detail.html",
        log_file=log_file,
        entries=entries,
        level_filter=level_filter,
        level_breakdown=level_breakdown,
    )


@logs_bp.route("/<int:file_id>/delete", methods=["POST"])
def delete(file_id):
    log_file = LogFile.query.get_or_404(file_id)

    if os.path.exists(log_file.file_path):
        os.remove(log_file.file_path)

    LogEntry.query.filter_by(log_file_id=log_file.id).delete()
    db.session.delete(log_file)
    db.session.commit()

    logger.info("Deleted log file: %s", log_file.filename)
    flash(f"File '{log_file.filename}' deleted successfully.", "success")
    return redirect(url_for("logs.index"))
