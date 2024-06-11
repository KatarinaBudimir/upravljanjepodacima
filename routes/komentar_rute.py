from fastapi import APIRouter, HTTPException, Depends, status, Response
from models.base import get_db
from models.komentar import Komentar
from schemas import Komentar_schema, Token_data
from sqlalchemy.orm import Session
from oauth2 import get_current_user


komentar_router = APIRouter(
    prefix='/komentar',
    tags=['komentari']
)

@komentar_router.post("/", response_model=Komentar_schema)
def stvori_komentar(komentar: Komentar_schema, db: Session = Depends(get_db)):
    novi_komentar = Komentar(sadrzaj=komentar.sadrzaj, objava_id=komentar.objava_id, korisnik_id=komentar.korisnik_id, datum_komentara=komentar.datum_komentara)
    db.add(novi_komentar)
    db.commit()
    db.refresh(novi_komentar)
    return novi_komentar

@komentar_router.get("/")
def dohvati_sve_komentare(db: Session = Depends(get_db)):
    komentari = db.query(Komentar).all()
    return komentari

@komentar_router.get("/{id}")
def dohvati_komentar_preko_id(id: int, db: Session = Depends(get_db)):
    komentar = db.query(Komentar).filter(Komentar.id == id).first()
    if komentar is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Komentar s id " + str(id) + " ne postoji!")
    return komentar

@komentar_router.delete("/{id}")
def delete_komentar(id: int, db: Session = Depends(get_db)):
    komentar = db.query(Komentar).filter(Komentar.id == id)

    if komentar.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Komentar s id " + str(id) + " ne postoji!")

    komentar.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@komentar_router.put("/{id}", response_model=Komentar_schema)
def update_komentar(id: int, updated_komentar: Komentar_schema, db: Session = Depends(get_db)):
    Komentar_query = db.query(Komentar).filter(Komentar.id == id)
    Komentar = Komentar_query.first()
    if Komentar:
        for attr, value in updated_komentar.dict().items():
            setattr(Komentar, attr, value)
        db.commit()
    return Komentar_query.first()
'''
redis = None
async def connect_to_redis():
    global redis
    redis = await aioredis.create_redis_pool('redis://redis:6379')
async def close_redis():
    redis.close()
    await redis.wait_closed()

@komentar_router.post("/", response_model=Komentar_schema)
async def stvori_komentar(komentar: Komentar_schema, db: Session = Depends(get_db), user_from_token: Token_data = Depends(get_current_user)):
    novi_komentar = Komentar(sadrzaj=komentar.sadrzaj, objava_id=komentar.objava_id, korisnik_id=komentar.korisnik_id, datum_komentara=komentar.datum_komentara)
    db.add(novi_komentar)
    db.commit()
    db.refresh(novi_komentar)
    await connect_to_redis()
    await redis.rpush("komentari:" + str(novi_komentar.objava_id), str(novi_komentar.id))
    await close_redis()
    return novi_komentar '''





