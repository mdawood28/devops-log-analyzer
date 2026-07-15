from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import Optional


class UploadForm(FlaskForm):
    file = FileField(
        "Log File",
        validators=[
            FileRequired(message="Please select a file."),
            FileAllowed(["log", "txt"], "Only .log and .txt files are allowed."),
        ],
    )
    submit = SubmitField("Upload & Analyze")


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    filename = StringField("Filename", validators=[Optional()])
    level = SelectField(
        "Log Level",
        choices=[
            ("", "All Levels"),
            ("INFO", "INFO"),
            ("WARNING", "WARNING"),
            ("ERROR", "ERROR"),
            ("DEBUG", "DEBUG"),
            ("CRITICAL", "CRITICAL"),
        ],
        validators=[Optional()],
    )
    date = StringField("Upload Date", validators=[Optional()])
