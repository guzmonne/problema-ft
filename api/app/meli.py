import json
from datetime import timedelta

from .redis import r
from .request import request


class Meli(object):
    host="https://api.mercadolibre.com"
    items_expiration_time=timedelta(minutes=1)
    domains_expiration_time=timedelta(hours=24)

    def get_data(self, key, url, expires=timedelta(minutes=1), transform=None):
        serialized_data = r.get(key)
        if serialized_data == None:
            response = request.get(url)
            r.set(key, response.text)
            r.expire(key, expires)
            data = response.json()
        else:
            data = json.loads(serialized_data)
        return data

    def get_item(self, item_id):
        url = self.host + f"/items/{item_id}"
        return self.get_data(item_id, url, expires=self.items_expiration_time)

    def get_domain(self, domain_id):
        url = self.host + f"/domains/{domain_id}/technical_specs/output"
        return self.get_data(domain_id, url, expires=self.domains_expiration_time)