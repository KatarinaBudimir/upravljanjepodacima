from models.base import Base, engine, SessionLocal
from sqlalchemy import text

from models.korisnik import Korisnik
from models.pohranamedija import Medij
from models.objava import Objava
from models.komentar import Komentar
from models.recenzije import Recenzija
from models.odgovori import Odgovor
from typing import List
from oauth2 import get_current_user
from fastapi import FastAPI, status, HTTPException, Response
from schemas import Korisnik_schema
from schemas import Objava_schema
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import uvicorn
import utils
import oauth2
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from routes import komentar_rute
from routes import objave_rute
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json

app = FastAPI()
Base.metadata.create_all(bind=engine) 
db = SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
app.include_router(komentar_rute.komentar_router)
app.include_router(objave_rute.objava_router) 



#@app.post("/brojobjava")
#async def broji_objave(costumer: KafkaConsumer=Depends(KafkaConsumer)):
    



@app.post("/signup")
async def stvori_korisnika(korisnik: Korisnik_schema = Depends(Korisnik_schema)):


    korisnik_in_db = db.query(Korisnik).filter(Korisnik.korisnickoime == korisnik.korisnickoime).first()
    if korisnik_in_db:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Korisničko ime je već u upotrebi, molimo pokušajte s drugim!")

    hashed_password = utils.hash_password(korisnik.sifra)
    korisnik.sifra = hashed_password

    user_data = korisnik.model_dump()

    novi_korisnik = Korisnik(**user_data)
    db.add(novi_korisnik)
    db.commit()
    db.refresh(novi_korisnik)
    return novi_korisnik

@app.post("/login")
def login_korisnik(korisnik_credentials: OAuth2PasswordRequestForm = Depends()):
    korisnik = db.query(Korisnik).filter(Korisnik.korisnickoime == korisnik_credentials.username).first()

    if not korisnik:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Neispravno korisničko ime ili lozinka")

    if not utils.verify_password(korisnik_credentials.password, korisnik.sifra):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Neispravno korisničko ime ili lozinka")

    data = {"korisnik_id": str(korisnik.id), "username": korisnik.korisnickoime}
    access_token = oauth2.create_access_token(data)
    return {"access_token": access_token, "token_type": "Bearer"}


#novi_korisnik = Korisnik(korisnickoime = "lukaperic" , sifra="12lp")
#db.add(novi_korisnik)
#db.commit()
#print(novi_korisnik)

#novi_medij = Medij(naziv_datoteke = "slika3.png", putanja_datoteke = "/path/to/image/slika3.png", datum_dodavanja =datetime.datetime.now())
#db.add(novi_medij)
#db.commit()

#nova_objava = Objava(naslov = "Neka objava", datum_objave = datetime.datetime.now(),sadrzaj = "Sadrzaj objave", korisnik_id = 1, id_medija = 4)
#db.add(nova_objava)
#db.commit()