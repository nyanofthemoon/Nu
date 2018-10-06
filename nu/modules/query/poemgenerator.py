import requests


class PoemGeneratorApi:

    def __init__(self):
        return None

    def generate(self):
        response = self._query()
        data = 'I am not feeling creative.'
        if response != None:
            data = 'A poem titled... ' + response[0]['title'] + '.\n' + response[0]['content']
        return data

    def _query(self):
        req = requests.get('https://www.poemist.com/api/v1/randompoems')
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            return None


PoemGenerator = PoemGeneratorApi()
