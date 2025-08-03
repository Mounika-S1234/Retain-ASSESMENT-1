# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import re
import random
import string

def is_valid_url(url):
    regex = re.compile(
        r'^(https?://)'  # http or https required
        r'(([A-Za-z0-9-]+\\.)+[A-Za-z]{2,})'  # domain
        r'(/.*)?$', re.IGNORECASE
    )
    return re.match(regex, url) is not None

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))
