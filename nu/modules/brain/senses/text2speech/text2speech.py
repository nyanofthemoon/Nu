# Text2Speech
# https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#notes-on-the-structure-of-the-language-data

import os
import re
import speech_recognition as sr
from pocketsphinx import pocketsphinx, Jsgf, FsgModel
from sphinxbase.sphinxbase import *
from nu.modules.config import nu_config
from nu.modules.sense import Sense
from nu.modules.query import SentimentAnalyzer

config = nu_config()


r = sr.Recognizer()

language = config.get('language', 'default')

model_dir = os.getcwd() + '/nu/modules/brain/senses/text2speech/languages/' + language;
grammar_path = model_dir + '/grammars'
config = pocketsphinx.Decoder.default_config()
config.set_string('-hmm', model_dir + '/accoustic-model')
config.set_string('-lm', model_dir + '/language-model.bin')
config.set_string('-dict', model_dir + '/pronounciation-dictionary.dict')
config.set_string("-logfn", os.devnull)
jsgf = Jsgf(grammar_path)


grammar_decoders = []
pattern = re.compile('public <(.*?)> =')

with open(grammar_path, 'rt') as in_file:
    for linenum, line in enumerate(in_file):
        grammar_key = pattern.findall(line)
        if grammar_key != []:
            decoder = pocketsphinx.Decoder(config)
            ruleGrammar = jsgf.get_rule(('structure.' + grammar_key[0]).format(grammar_path))
            fsgNext = jsgf.build_fsg(ruleGrammar, decoder.get_logmath(), 7.5)
            decoder.set_fsg(grammar_key[0], fsgNext)
            decoder.set_search(grammar_key[0])
            grammar_decoders.append(decoder)


class Text2Speech:

    CHANNEL = 'text2speech'
    CHANNEL_TYPE = 'brain'

    @staticmethod
    def id():
        return Sense.id(__class__)

    @staticmethod
    def set(value):
        return Sense.set(__class__, value)

    @staticmethod
    def get():
        return Sense.get(__class__)

    @staticmethod
    def publish(type, value=None, sentiment=None):
        data = {
            'type': type,
            'text': value,
            'sentiment': sentiment
        }
        return Sense.publish(__class__, data)

    @staticmethod
    def subscribe(subscriber):
        return Sense.subscribe(__class__, subscriber)

    @staticmethod
    def listen(segment):
        r.listen_in_background(source=sr.Microphone(), callback=__class__.parse, phrase_time_limit=segment)

    @staticmethod
    def parse(selfR, audio):
        try:
            raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
            decodedType = None
            decodedValue = None
            # Using Sphynx Grammars
            for grammar_decoder in grammar_decoders:
                grammar_decoder.start_utt()
                grammar_decoder.process_raw(raw_data, False, True)
                grammar_decoder.end_utt()
                hypothesis = grammar_decoder.hyp()
                if hypothesis != None:
                    decodedType = grammar_decoder.get_search()
                    decodedScore = hypothesis.best_score
                    if decodedType in ['answer', 'callout']:
                        if decodedScore >= -2100:
                            decodedValue = str(hypothesis.hypstr)
                            break
                    elif decodedScore >= -4800:
                        decodedValue = str(hypothesis.hypstr)
                        break
            # Using Google Audio API
            #if decodedValue == None:
            #    decodedType = 'complex'
            #    decodedValue = str(r.recognize_google(audio))
            #    decodedSentiment = SentimentAnalyzer.evaluate(decodedValue)
            if decodedValue != None:
                Text2Speech.publish(decodedType, decodedValue, {'polarity': 'neutral', 'perspective': 'neutral'})
        except:
            return False
