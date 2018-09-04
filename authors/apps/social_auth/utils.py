from datetime import datetime


def create_unique_number():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")
