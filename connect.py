import redis
from models.korisnik import Korisnik


r = redis.Redis(host='redis', port=6379, decode_responses=True)

r.set('name', 'Ime Prezime', ex=50)
print(r.get('name'))