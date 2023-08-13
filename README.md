# pv_growatt_data_downloader
download data from growatt web portal using selenium and parse it into sqlite

## Data process
1. Look into your excel file dump folder what the latest file is you have downloaded. Chances are this 'monthly report' is incomplete so it will be overwritten.
2. Open Selenium and browse to the portal to automatically grab all monthly reports between the current month and the one found in step 1.
3. Transfer these monthly reports from the temp storage into your excel file dump folder.
4. Parse these files to extract the clean data.
5. Import the data into the designated DB.

## How to run
* clone the repo
* python -m venv venv
* pip -r requirements.txt
* configure in main.py
* run main.py

## Author
Jorrit Vander Mynsbrugge