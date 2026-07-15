from app.services import LogParser


def test_parse_standard_log_line():
    parser = LogParser()
    line = "2024-01-15 10:30:00 INFO Application started"
    result = parser.parse_line(line)

    assert result is not None
    assert result["level"] == "INFO"
    assert result["message"] == "Application started"


def test_parse_error_line():
    parser = LogParser()
    line = "2024-01-15 10:30:10 ERROR Database connection failed"
    result = parser.parse_line(line)

    assert result is not None
    assert result["level"] == "ERROR"
    assert result["message"] == "Database connection failed"


def test_parse_line_with_brackets():
    parser = LogParser()
    line = "[2024-01-15 10:30:00] WARNING Disk full"
    result = parser.parse_line(line)

    assert result is not None
    assert result["level"] == "WARNING"
    assert result["message"] == "Disk full"


def test_parse_invalid_line():
    parser = LogParser()
    line = "This is not a valid log line"
    result = parser.parse_line(line)

    assert result is None


def test_parse_empty_line():
    parser = LogParser()
    result = parser.parse_line("")

    assert result is None


def test_parse_content(sample_log_content):
    parser = LogParser()
    entries = parser.parse_content(sample_log_content)

    assert len(entries) == 5
    assert entries[0]["level"] == "INFO"
    assert entries[4]["level"] == "CRITICAL"


def test_count_levels(sample_log_content):
    parser = LogParser()
    entries = parser.parse_content(sample_log_content)
    counts = parser.count_levels(entries)

    assert counts["INFO"] == 1
    assert counts["WARNING"] == 1
    assert counts["ERROR"] == 1
    assert counts["DEBUG"] == 1
    assert counts["CRITICAL"] == 1


def test_parse_file(tmp_path, sample_log_content):
    log_file = tmp_path / "test.log"
    log_file.write_text(sample_log_content)

    parser = LogParser()
    entries = parser.parse_file(str(log_file))

    assert len(entries) == 5
    assert all("line_number" in e for e in entries)
