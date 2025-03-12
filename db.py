from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class IndexedFile(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_id = Column(String, nullable=False)
    file_name = Column(String, nullable=False)

# Initialize the database
engine = create_engine(os.getenv("DATABASE_URI"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
