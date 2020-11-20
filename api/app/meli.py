import os
from datetime import timedelta
import requests
import redis

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    db=int(os.environ.get("REDIS_DB", "0"))    
)

class Meli(object):
    host="https://api.mercadolibre.com/"

    def get_data(self, key, url, expires=timedelta(minutes=1)):
        data = r.hgetall(key)
        if data == None:
            response = requests.get(url)
            data = response.json()
            r.hmset(data, expires)
        return data

    def get_item(self, item_id):
        return self.get_data(item_id, self.host + f"/items/{item_id}")

    def get_domain(self, domain_id):
        return self.get_data(domain_id, self.host + f"/domains/{domain_id}/technical_specs/output", expires=timedelta(hours=12))
