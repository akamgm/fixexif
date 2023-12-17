import os
import sys
from datetime import datetime, timedelta

def generate_dates_for_year(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    date_set = set()

    while start_date <= end_date:
        date_set.add(start_date.strftime('%Y%m%d'))
        start_date += timedelta(days=1)

    return date_set

def find_missing_dates(directory_path, year=2023):
    all_dates = generate_dates_for_year(year)
    found_dates = set()

    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.jpg'):
            date_part = filename.split('.')[0]
            if date_part.isdigit() and len(date_part) == 8:
                found_dates.add(date_part)

    missing_dates = all_dates - found_dates
    return sorted(list(missing_dates))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python missing.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    missing_dates = find_missing_dates(directory_path)

    if missing_dates:
        print("Missing dates:")
        for date in missing_dates:
            print(date)
    else:
        print("No missing dates found.")


