from datetime import datetime

from app import db


class LogFile(db.Model):
    __tablename__ = "log_files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    entry_count = db.Column(db.Integer, default=0)
    info_count = db.Column(db.Integer, default=0)
    warning_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    debug_count = db.Column(db.Integer, default=0)
    critical_count = db.Column(db.Integer, default=0)

    entries = db.relationship(
        "LogEntry", backref="log_file", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def file_size_display(self):
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size / (1024 * 1024):.1f} MB"

    def __repr__(self):
        return f"<LogFile {self.original_filename}>"


class LogEntry(db.Model):
    __tablename__ = "log_entries"

    id = db.Column(db.Integer, primary_key=True)
    log_file_id = db.Column(db.Integer, db.ForeignKey("log_files.id"), nullable=False)
    timestamp = db.Column(db.String(50))
    level = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    line_number = db.Column(db.Integer, nullable=False)
    raw_line = db.Column(db.Text)

    def __repr__(self):
        return f"<LogEntry {self.level}: {self.message[:50]}>"
