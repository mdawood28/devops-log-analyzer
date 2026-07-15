# DevOps Log Analyzer

A Flask web application for uploading, parsing, and analyzing DevOps log files. Provides a dashboard with statistics, filtering, and search capabilities.

## Features

- **Dashboard** — view statistics: total files, entries, and counts by log level (INFO, WARNING, ERROR, DEBUG, CRITICAL)
- **Upload** — accept `.log` and `.txt` files up to 10 MB
- **Auto-parse** — extract timestamps, log levels, and messages from common log formats
- **Search & filter** — find logs by filename, level, or upload date
- **Detail view** — per-file breakdown with entry listing
- **Delete** — remove uploaded files and associated records
- **Responsive UI** — Bootstrap 5 interface
- **Error pages** — custom 404 and 500 pages

## Tech Stack

- Python 3.9+
- Flask with Blueprints
- SQLAlchemy ORM + SQLite
- Flask-WTF for forms
- Bootstrap 5
- Pytest for testing
- Black + Flake8 for code quality
- GitHub Actions CI

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/devops-log-analyzer.git
cd devops-log-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your secret key

# Run the application
python run.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
devops-log-analyzer/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # SQLAlchemy models
│   ├── forms.py             # Flask-WTF forms
│   ├── services.py          # Log parsing service
│   ├── routes/
│   │   ├── __init__.py      # Blueprint registration
│   │   ├── main.py          # Dashboard routes
│   │   ├── logs.py          # Log management routes
│   │   └── errors.py        # Error handlers
│   ├── templates/           # Jinja2 templates
│   └── static/css/          # Custom styles
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_models.py
│   ├── test_services.py
│   └── test_routes.py
├── config.py                # App configuration
├── run.py                   # Entry point
├── requirements.txt
├── pytest.ini
└── .github/workflows/ci.yml
```

## Running Tests

```bash
pytest
pytest -v              # Verbose output
pytest --cov=app       # With coverage
```

## Linting & Formatting

```bash
flake8 app/ tests/ --max-line-length=120
black app/ tests/ --line-length=120
```

## Log Format Support

The parser recognizes entries matching:

```
YYYY-MM-DD HH:MM:SS - LEVEL - Message
YYYY-MM-DD HH:MM:SS,ms - LEVEL - Message
[YYYY-MM-DD HH:MM:SS] LEVEL: Message
```

Lines that don't match a known format are stored as raw entries without a parsed level or timestamp.

## License

MIT
