from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from models.base import Base

class Medij(Base):
    __tablename__ = 'mediji'

    id = Column(Integer, primary_key=True)
    naziv_datoteke = Column(String(255))
    putanja_datoteke = Column(String(255))
    datum_dodavanja = Column(DateTime)

    objave = relationship('Objava', back_populates='medij')