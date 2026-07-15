import re


LOG_PATTERNS = [
    re.compile(
        r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}[.,]?\d*)\s+"
        r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"
        r"(?P<message>.*)"
    ),
    re.compile(
        r"\[(?P<timestamp>[^\]]+)\]\s+\[?(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\]?\s+"
        r"(?P<message>.*)"
    ),
    re.compile(
        r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s*[:\-]\s*"
        r"(?P<message>.*)"
    ),
]


class LogParser:
    """Parses log file content and extracts structured entries."""

    def parse_line(self, line):
        """Parse a single log line. Returns a dict or None."""
        line = line.strip()
        if not line:
            return None

        for pattern in LOG_PATTERNS:
            match = pattern.match(line)
            if match:
                groups = match.groupdict()
                return {
                    "timestamp": groups.get("timestamp", ""),
                    "level": groups["level"],
                    "message": groups["message"].strip(),
                }
        return None

    def parse_content(self, text):
        """Parse multi-line log text. Returns list of entry dicts."""
        entries = []
        lines = text.splitlines()

        for line_number, line in enumerate(lines, start=1):
            result = self.parse_line(line)
            if result:
                result["line_number"] = line_number
                result["raw_line"] = line.strip()
                entries.append(result)

        return entries

    def parse_file(self, filepath):
        """Read and parse a log file from disk."""
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return self.parse_content(content)

    def count_levels(self, entries):
        """Count entries by log level."""
        counts = {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
        }
        for entry in entries:
            level = entry.get("level", "")
            if level in counts:
                counts[level] += 1
        return counts
