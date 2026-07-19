from database.base import Base
from database.session import engine

Base.metadata.create_all(bind=engine)