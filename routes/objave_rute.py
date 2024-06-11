from fastapi import APIRouter, HTTPException, Depends, status, Response
from models.base import get_db
from models.objava import Objava
from schemas import Objava_schema, Token_data
from sqlalchemy.orm import Session
from oauth2 import get_current_user
import redis
from kafka import KafkaProducer
import json


objava_router = APIRouter(
    prefix='/objava',
    tags=['objava']
)
r = redis.Redis(host='redis', port=6379, decode_responses=True)
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@objava_router.post("/", response_model=Objava_schema)
def stvori_objavu(objava: Objava_schema, db: Session = Depends(get_db)):
    nova_objava= Objava(sadrzaj=objava.sadrzaj,naslov=objava.naslov_objave, korisnik_id=objava.korisnik_id, datum_objave=objava.datum_objave, id_medija=objava.id_medija)
    db.add(nova_objava)
    db.commit()
    db.refresh(nova_objava)
    r.set('objava', nova_objava.naslov, ex=30)
    producer.send('objava_topic', {'action': 'create', 'naslov': nova_objava.naslov})
    return objava

@objava_router.get("/")
def dohvati_sve_objave(db: Session = Depends(get_db)):
    objave = db.query(Objava).all()
    return objave

@objava_router.get("/{id}")
def dohvati_objava_preko_id(id: int, db: Session = Depends(get_db)):
    objava = db.query(Objava).filter(Objava.id == id).first()
    if objava is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objava s id " + str(id) + " ne postoji!")
    return objava

@objava_router.delete("/{id}")
def delete_objava(id: int, db: Session = Depends(get_db)):
    objava = db.query(Objava).filter(Objava.id == id)

    if objava.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Objava s id " + str(id) + " ne postoji!")

    objava.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@objava_router.put("/{id}", response_model=Objava_schema)
def update_objava(id: int, updated_objava: Objava_schema, db: Session = Depends(get_db)):
    Objava_query = db.query(Objava).filter(Objava.id == id)
    Objava = Objava_query.first()
    if Objava:
        for attr, value in updated_objava.dict().items():
            setattr(Objava, attr, value)
        db.commit()
    return Objava_query.first()
