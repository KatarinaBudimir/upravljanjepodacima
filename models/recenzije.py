from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Recenzija(Base):
    __tablename__ = 'recenzije'

    id = Column(Integer, primary_key=True)
    korisnik_id = Column(Integer, ForeignKey('korisnici.id', ondelete="CASCADE"), nullable=False)
    objava_id = Column(Integer, ForeignKey('objave.id', ondelete="CASCADE"), nullable=False)
    sadrzaj = Column(Text)
    datum_recenzije = Column(DateTime)
    ocjena = Column(Integer)

    korisnik = relationship("Korisnik", back_populates="recenzije")
    objava = relationship("Objava", back_populates="recenzije")