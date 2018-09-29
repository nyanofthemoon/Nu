# TextBlob
# https://textblob.readthedocs.io/en/dev/quickstart.html#create-a-textblob

from textblob import TextBlob
from nu.modules.config import query_config

queryConfig = query_config()


class SentimentAnalyzerApi:

    def __init__(self, positive, negative, subjective, objective):
        self.positive = positive
        self.negative = negative
        self.subjective = subjective
        self.objective = objective

    def evaluate(self, query):
        results = TextBlob(query)

        polarity = 'neutral'
        if results.sentiment.polarity >= self.positive:
          polarity = 'positive'
        elif results.sentiment.polarity <= self.negative:
          polarity = 'negative'

        perspective = 'neutral'
        if results.sentiment.subjectivity <= self.objective:
          perspective = 'objective'
        elif results.sentiment.subjectivity >= self.subjective:
          perspective = 'subjective'

        return {
          'polarity': polarity,
          'perspective': perspective
        }


SentimentAnalyzer = SentimentAnalyzerApi(queryConfig.get('SentimentAnalyzer', 'positiveThreshold'), queryConfig.get('SentimentAnalyzer', 'negativeThreshold'), queryConfig.get('SentimentAnalyzer', 'subjectiveThreshold'), queryConfig.get('SentimentAnalyzer', 'objectiveThreshold'))
