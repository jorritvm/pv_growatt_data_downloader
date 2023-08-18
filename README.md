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
* make sure you have your webportal secret set up in a .env file, use the .env.template as basis
* configure in constants.py
* run main.py

## Project learnings
### Python
* tempdir is a nice way of creating a temporary directory with full write access

### Pandas
* openpyxl does not handle .xls, for that you need xlrd
  
### Selenium
* Selenium no longer requires a chromiumdriver
* To get the path to the correct element, it's best to use the inspector and copy the full xpath. Finding elements by id or class sometimes results in a 'not interactable' bug.
* Make sure to add some time.sleep() because if you go to fast, you also get 'not interactable' bug when the elements are not yet loaded in the browser.

### SQLalchemy
* in CORE no Session object is required
* it's good to have a schema definition file, but for real DB schema management you need a data migration tool like alembic.
* SQLalchemy is finicky about its data types, especially dates!
* there are two ways of doing SQL DDL: 
  1. using CORE concepts like MetaData and Table, insantiate the Table class and pass it a metadata object constructor argument along with column arguments. 
  2. using ORM concepts like declarativebase. you can create_all in the declarative base without worrying about truncating existing tables, this throws errors in CORE 
* there are two ways of doing SQL DQL:
  1. using pure SQL defined by the text() function (to prevent sql injection!)
  2. using select() update() insert() delete() wrappers




## Author
Jorrit Vander Mynsbrugge