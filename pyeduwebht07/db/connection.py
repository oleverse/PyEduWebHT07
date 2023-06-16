from sqlalchemy.engine import create_engine
from db.config import get_connection_string
from pathlib import Path
from sqlalchemy.orm import sessionmaker

connection_string = get_connection_string(Path('conf/db.ini'))
engine = create_engine(connection_string)
session = sessionmaker(engine)()
