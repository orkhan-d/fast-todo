import os
from typing import Annotated
from uuid import uuid4
from sqlalchemy import BIGINT, create_engine, String
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase, mapped_column, Mapped

engine = create_engine(os.getenv('DB_ADDRESS'))
SessionFactory = sessionmaker(bind=engine)

session = scoped_session(SessionFactory)

uuidpk = Annotated[str, mapped_column(type_=String, default=uuid4(), primary_key=True)]
intpk = Annotated[int, mapped_column(type_=BIGINT, primary_key=True)]

class Base(DeclarativeBase): ...