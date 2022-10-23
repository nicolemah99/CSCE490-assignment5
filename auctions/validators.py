from datetime import datetime, timezone
from django.forms import ValidationError


def validate_date(date):
    if date < datetime.today().date():
        raise ValidationError("Date cannot be in the past")