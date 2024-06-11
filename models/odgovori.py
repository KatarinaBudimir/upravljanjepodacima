from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Odgovor(Base):
    __tablename__ = 'odgovori'

    id = Column(Integer, primary_key=True)
    sadrzaj = Column(Text)
    datum_odgovora = Column(DateTime)
    korisnik_id = Column(Integer, ForeignKey('korisnici.id', ondelete="CASCADE"), nullable=False)
    komentar_id = Column(Integer, ForeignKey('komentari.id', ondelete="CASCADE"), nullable=False)

    korisnik = relationship("Korisnik", back_populates="odgovori")
    komentar = relationship("Komentar")