from sqlalchemy import Column, Integer, String, create_engine, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///Selenium_app/Base_De_Datos_Data.db', echo=True)
Base = declarative_base()

class Data_Extraida(Base):
    __tablename__ = 'Data_extraida_DB'
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Texto_N1 = Column(String(500), nullable=False, unique=False)
    Texto_N2 = Column(String(500), nullable=False, unique=False)
    Src_imagenes = Column(String(500), nullable=False, unique=False)
    href_productos = Column(String(500), nullable=False, unique=False)
    created_at = Column(DateTime(), default=datetime.now())

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.create_all(engine)