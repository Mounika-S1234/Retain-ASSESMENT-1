import re

def is_valid_email(email):
    # Very basic email validation using regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
