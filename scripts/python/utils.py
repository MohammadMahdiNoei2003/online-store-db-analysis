from datetime import datetime, timedelta
import random

DEFAULT_YEARS_BACK = 3

def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def generate_timestamps(years_back=DEFAULT_YEARS_BACK):
    end = datetime.now()
    start = end - timedelta(days=years_back * 365)
    created_at = random_date(start, end)
    updated_at = random_date(created_at, end)
    return created_at, updated_at

def generate_timestamps_list(count, years_back=DEFAULT_YEARS_BACK):
    return [generate_timestamps(years_back) for _ in range(count)]

