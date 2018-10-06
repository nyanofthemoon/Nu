import requests


class CorporateBullshitApi:

    def __init__(self):
        return None

    def generate(self):
        response = self._query()
        data = 'I am not feeling creative.'
        if response != None:
            data = response['phrase']
        return data

    # https://corporatebs-generator.sameerkumar.website
    def _query(self):
        req = requests.get('https://corporatebs-generator.sameerkumar.website')
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            return None


CorporateBullshitGenerator = CorporateBullshitApi()
