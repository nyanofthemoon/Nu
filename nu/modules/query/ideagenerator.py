import requests


class IdeaGeneratorApi:

    def __init__(self):
        return None

    def generate(self):
        response = self._query()
        data = 'I am not feeling creative.'
        if response != None:
            data = response['this'] + ' for ' + response['that']
        return data

    def _query(self):
        req = requests.get('http://itsthisforthat.com/api.php?json')
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            return None


IdeaGenerator = IdeaGeneratorApi()
