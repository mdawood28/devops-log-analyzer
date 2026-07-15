from app import db
from app.models import LogFile, LogEntry


def test_create_log_file(app):
    with app.app_context():
        log_file = LogFile(
            filename="test.log",
            original_filename="test.log",
            file_size=1024,
            file_path="/tmp/test.log",
            entry_count=5,
            info_count=2,
            warning_count=1,
            error_count=1,
            debug_count=1,
            critical_count=0,
        )
        db.session.add(log_file)
        db.session.commit()

        retrieved = LogFile.query.first()
        assert retrieved.filename == "test.log"
        assert retrieved.file_size == 1024
        assert retrieved.entry_count == 5


def test_create_log_entry(app):
    with app.app_context():
        log_file = LogFile(
            filename="test.log",
            original_filename="test.log",
            file_size=512,
            file_path="/tmp/test.log",
        )
        db.session.add(log_file)
        db.session.commit()

        entry = LogEntry(
            log_file_id=log_file.id,
            timestamp="2024-01-15 10:30:00",
            level="ERROR",
            message="Connection failed",
            line_number=1,
            raw_line="2024-01-15 10:30:00 ERROR Connection failed",
        )
        db.session.add(entry)
        db.session.commit()

        retrieved = LogEntry.query.first()
        assert retrieved.level == "ERROR"
        assert retrieved.message == "Connection failed"
        assert retrieved.log_file_id == log_file.id


def test_log_file_entries_relationship(app):
    with app.app_context():
        log_file = LogFile(
            filename="test.log",
            original_filename="test.log",
            file_size=512,
            file_path="/tmp/test.log",
        )
        db.session.add(log_file)
        db.session.commit()

        entry1 = LogEntry(
            log_file_id=log_file.id,
            level="INFO",
            message="Started",
            line_number=1,
            raw_line="INFO Started",
        )
        entry2 = LogEntry(
            log_file_id=log_file.id,
            level="ERROR",
            message="Failed",
            line_number=2,
            raw_line="ERROR Failed",
        )
        db.session.add_all([entry1, entry2])
        db.session.commit()

        assert len(log_file.entries) == 2


def test_cascade_delete(app):
    with app.app_context():
        log_file = LogFile(
            filename="test.log",
            original_filename="test.log",
            file_size=512,
            file_path="/tmp/test.log",
        )
        db.session.add(log_file)
        db.session.commit()

        entry = LogEntry(
            log_file_id=log_file.id,
            level="INFO",
            message="Test",
            line_number=1,
            raw_line="INFO Test",
        )
        db.session.add(entry)
        db.session.commit()

        db.session.delete(log_file)
        db.session.commit()

        assert LogEntry.query.count() == 0
