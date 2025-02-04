from django.core.validators import RegexValidator

validate_only_letter_value = RegexValidator(r'^[a-zA-Z]+(\s[a-zA-Z]+)?$', 'The value should contain only letters.')

validate_only_digit_value = RegexValidator(r'^[0-9]*$', 'The value should contain only digits.')

validate_ten_digits = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")