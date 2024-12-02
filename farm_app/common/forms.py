from django.forms.widgets import DateInput

class CustomDateInput(DateInput):
    input_type = 'date'
    format = '%d.%m.%Y'

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs=attrs or {}, format=format or self.format)
