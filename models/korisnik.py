from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Korisnik(Base):
    __tablename__ = 'korisnici'

    id = Column(Integer, primary_key=True)
    korisnickoime = Column(String(255))
    sifra = Column(String(255))
    
    komentari = relationship('Komentar', back_populates='korisnik')
    odgovori = relationship('Odgovor', back_populates='korisnik')
    recenzije = relationship('Recenzija', back_populates='korisnik')
    objave = relationship('Objava', back_populates='korisnik')