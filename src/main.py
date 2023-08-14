from raw import find_starting_point_for_download, copy_back_monthly_excel_reports
from webportal import download_files_from_online_portal
from db import parse_files_to_dataframe, write_df_to_db


def main():
    print("Step 1: find the most recent file where we have to restart downloading...")
    halt_at = find_starting_point_for_download()

    print("Step 2: fetch from web portal using selenium...")
    temp_dir = download_files_from_online_portal(halt_at)

    print("Step 3: copy temp files to excel folder...")
    new_files = copy_back_monthly_excel_reports(temp_dir)
    print(new_files)

    print("Step 4: parse the files into a dataframe...")
    df = parse_files_to_dataframe(new_files)

    print("Step 5: ingest into db...")
    write_df_to_db(df)


if __name__ == "__main__":
    main()

