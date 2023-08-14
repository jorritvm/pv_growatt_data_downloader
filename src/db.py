import pandas as pd
from sqlalchemy import create_engine, Column, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import constants as C


def parse_files_to_dataframe(new_files):
    # todo : better implementation
    data = {
        'date': ['2023-08-05', '2023-08-06', '2023-08-07'],
        'generation': [10000.5, 10500.2, 20000.7]
    }
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])

    return df


def write_df_to_db(df):
    ## todo: rewrite this using a staging table

    # Create an SQLite database engine
    engine = create_engine(f'sqlite:///{C.DATABASE_LOCATION}', echo=True)
    # Define a data model
    Base = declarative_base()

    class GenerationData(Base):
        __tablename__ = 'generation_data'

        date = Column(Date, primary_key=True)
        generation = Column(Float)

    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    # Write the DataFrame to the database, overwriting if primary key exists
    df.to_sql('generation_data', con=engine, if_exists='append', index=False)
    # Close the session
    session.close()