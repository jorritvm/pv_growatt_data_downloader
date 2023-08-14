import os
from dotenv import load_dotenv

# raw file constants
EXCEL_FILES_LOCATION = r"C:\Users\jorrit\drive\finance\nutsvoorzieningen\zonnepanelen\growatt_data\data_download\maandrapport"

# selenium constants
MAXIMUM_GO_BACK_UNTIL_YEAR = 2017
MAXIMUM_GO_BACK_UNTIL_MONTH = 1
PLATFORM_URL = "https://server.growatt.com/login"

# db constants
load_dotenv()
USERNAME = os.getenv("growatt-username")
PASSWORD = os.getenv("growatt-password")
DATABASE_LOCATION = r"C:\Users\jorrit\drive\finance\nutsvoorzieningen\zonnepanelen\growatt_data\data_download\growatt.db"
