import os
import re
import shutil
from datetime import datetime

import constants as C


def find_starting_point_for_download():
    most_recent_date = get_most_recent_date(C.EXCEL_FILES_LOCATION)
    if most_recent_date:
        return {'year': most_recent_date.year, 'month': most_recent_date.month}
    else:
        return C.MAXIMUM_GO_BACK_UNTIL_YEAR, C.MAXIMUM_GO_BACK_UNTIL_MONTH


def extract_year_month(filename):
    # Extracts year and month using regex
    match = re.search(r'(\d{4}-\d{1,2})', filename)
    if match:
        year_month = match.group(1)
        year, month = map(int, year_month.split('-'))
        return year, month
    else:
        return None


def get_most_recent_date(folder_path):
    excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xls')]

    if not excel_files:
        return None

    most_recent_date = None
    for excel_file in excel_files:
        year, month = extract_year_month(excel_file)
        date = datetime(year, month, 1)  # Assuming day 1 of the month
        if most_recent_date is None or date > most_recent_date:
            most_recent_date = date

    return most_recent_date


def copy_back_monthly_excel_reports(source_folder):
    target_folder = C.EXCEL_FILES_LOCATION

    # List all files in the source folder
    files = os.listdir(source_folder)
    out = []

    # Copy the file from source to target, overwriting if exists
    for file in files:
        source_path = os.path.join(source_folder, file)
        target_path = os.path.join(target_folder, file)
        print(f"Writing {target_path}")
        shutil.copy2(source_path, target_path)
        out.append(target_path)

    return out
