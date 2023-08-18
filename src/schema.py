from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, Float, Date
import constants as C

metadata = MetaData()

tbl_solar = Table(
    "solar_generation",
    metadata,
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("day", Integer, nullable=False),
    Column("solar", Float, nullable=False),
    Column("date", Date, primary_key=True),
)

if __name__ == "__main__":
    # Create the whole db schema
    engine = create_engine(f'sqlite:///{C.DATABASE_LOCATION}', echo=True)
    metadata.create_all(engine)
