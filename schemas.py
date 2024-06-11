import datetime
from pydantic import BaseModel
from typing import Optional

class Komentar_schema(BaseModel):
    sadrzaj: str
    objava_id: int
    korisnik_id: int
    datum_komentara: datetime.datetime = datetime.datetime.now()

class Korisnik_schema(BaseModel):
    korisnickoime: str
    sifra: str

class Token_data(BaseModel):
    korisnik_id: int
    username: str

class Objava_schema(BaseModel):
    naslov_objave: Optional[str]
    datum_objave: datetime.datetime = datetime.datetime.now()
    sadrzaj: str
    korisnik_id: int
    id_medija: int

class Token_data(BaseModel):
    objava_id: int
    username: str
