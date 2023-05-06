from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import local_setting

Base = declarative_base()
engine = create_engine(local_setting.db_connection_str)

session = Session(engine)
