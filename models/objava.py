from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
class Objava(Base):
    __tablename__ = 'objave'

    id = Column(Integer, primary_key=True)
    naslov = Column(String(100))
    datum_objave = Column(DateTime)
    sadrzaj = Column(Text)
    korisnik_id = Column(Integer, ForeignKey('korisnici.id', ondelete="CASCADE"), nullable=False)
    id_medija = Column(Integer, ForeignKey('mediji.id', ondelete="CASCADE"), nullable=False)

    korisnik = relationship("Korisnik", back_populates="objave")
    medij = relationship("Medij", back_populates="objave")
    komentari = relationship("Komentar", back_populates="objava")
    recenzije = relationship("Recenzija", back_populates="objava")