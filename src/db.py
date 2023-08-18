import os
import re
import pandas as pd
import xlrd
from dateutil.parser import parse
from sqlalchemy import create_engine, text
from schema import engine, tbl_solar
import constants as C


def parse_files_to_dataframe(new_files):
    """
    :param new_files: list of absolute file paths to parse
    :return:
        df.dtypes
        year              int64
        month             int64
        day               int64
        solar           float64
        date     datetime64[ns]
        dtype: object
    """

    all_data_list = []

    for fpfn in new_files:
        # year & month
        matches = re.search(r"(\d{4}).*?(\d{1,2})\.xls", os.path.basename(fpfn))
        yyyy = int(matches.group(1))
        mm = int(matches.group(2))

        # read daily data file
        wb = xlrd.open_workbook(fpfn)
        ws = wb.sheet_by_index(0)
        data = [ws.row_values(rowx) for rowx in range(16, 18)]
        columns = data[0][3:37]  # Assuming the data starts from column D and ends at AL
        values = data[1][3:37]

        # cleanup
        last_data_col = columns.index("Total(kWh)")
        columns = [int(x) for x in columns[:last_data_col]]
        values = [float(x) if x != '' else 0 for x in values[:last_data_col]]

        dt = pd.DataFrame({'day': columns,
                           'solar': values})
        dt["year"] = yyyy
        dt["month"] = mm
        dt = dt[['year', 'month', 'day', 'solar']]

        all_data_list.append(dt)

    df = pd.concat(all_data_list, ignore_index=True, axis=0)
    df["date"] = df.apply(lambda row: parse(f"{str(int(row['year']))}-{str(int(row['month']))}-{str(int(row['day']))}"), axis=1)

    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def write_df_to_db(df):
    """
    parses a df into the database, overwriting values with existing primary key and appending new values
    :param df:
    :return: /
    """

    # load into db, can't use df.to_sql because it overwrites all or appends all ...
    connection = engine.connect()
    for index, row in df.iterrows():
        update_sql = text(
            "INSERT OR REPLACE INTO solar_generation (year, month, day, solar, date) "
            "VALUES (:year, :month, :day, :solar, :date)"
        )
        connection.execute(update_sql,
                           {'year': row['year'],
                            'month': row['month'],
                            'day': row['day'],
                            'solar': row['solar'],
                            'date': row['date'].date()})

    connection.commit()
    connection.close()
