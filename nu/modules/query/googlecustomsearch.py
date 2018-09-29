# Google Custom Search API
# https://google-api-client-libraries.appspot.com/documentation/customsearch/v1/python/latest/customsearch_v1.cse.html

import pprint


from googleapiclient.discovery import build
from nu.modules.config import query_config

queryConfig = query_config()


class GoogleCustomSearchApi:

    def __init__(self, key):
        self.service = build('customsearch', 'v1', developerKey=key)

    def search(self, query, results=1):
        pprint( self.service.cse().list(q=query, num=results, filter='1', safe='high').execute() )
        return True

    def image(self, query, size='small', results=1):
        pprint( self.service.cse().list(q=query, imgSize=size, num=results, searchType='image', imgType='photo', filter='1', safe='high').execute() )
        return True


GoogleCustomSearch = GoogleCustomSearchApi(queryConfig.get('GoogleCustomSearch', 'apiKey'))
