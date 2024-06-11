from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from models.base import Base

class Komentar(Base):
    __tablename__ = 'komentari'

    id = Column(Integer, primary_key=True)
    objava_id = Column(Integer, ForeignKey('objave.id', ondelete="CASCADE"), nullable=False)
    korisnik_id = Column(Integer, ForeignKey('korisnici.id', ondelete="CASCADE"), nullable=False)
    sadrzaj = Column(Text)
    datum_komentara = Column(DateTime)

    objava = relationship("Objava", back_populates="komentari")
    korisnik = relationship("Korisnik", back_populates="komentari")