# python nu/modules/brain/senses/text2speech/debug-grammars.py

import os
import re
from textblob import TextBlob
import speech_recognition as sr
from pocketsphinx import pocketsphinx, Jsgf, FsgModel
from sphinxbase.sphinxbase import *

r = sr.Recognizer()

language = 'en-US'
model_dir = os.getcwd() + '/nu/modules/brain/senses/text2speech/languages/' + language;
grammar_path = model_dir + '/grammars'
config = pocketsphinx.Decoder.default_config()
config.set_string('-hmm', model_dir + '/accoustic-model')
config.set_string('-lm', model_dir + '/language-model.bin')
config.set_string('-dict', model_dir + '/pronounciation-dictionary.dict')
#config.set_string('-jfsg', grammar_path)
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

grammar_decoders = []
pattern = re.compile('public <(.*?)> =')

with open(grammar_path, 'rt') as in_file:
    for linenum, line in enumerate(in_file):
        grammar_key = pattern.findall(line)
        if grammar_key != []:
            decoder = pocketsphinx.Decoder(config)
            ruleGrammar = jsgf.get_rule(('structure.' + grammar_key[0]).format(grammar_path))
            fsgNext = jsgf.build_fsg(ruleGrammar, decoder.get_logmath(), 7)
            decoder.set_fsg(grammar_key[0], fsgNext)
            decoder.set_search(grammar_key[0])
            grammar_decoders.append(decoder)

def evaluate(query):
    results = TextBlob(query)
    polarity = 'neutral'
    if results.sentiment.polarity >= 0.4:
      polarity = 'positive'
    elif results.sentiment.polarity <= -0.4:
      polarity = 'negative'
    perspective = 'neutral'
    if results.sentiment.subjectivity <= 0.33:
      perspective = 'objective'
    elif results.sentiment.subjectivity >= 0.66:
      perspective = 'subjective'
    return {
      'polarity': polarity,
      'perspective': perspective
    }

def parse(selfR, audio):
    try:

        raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
        decodedType = None
        decodedValue = None
        decodedSentiment = {'polarity': 'neutral', 'perspective': 'neutral'}
        decodedScore = 0
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

        if decodedValue == None:
            decodedType = 'complex'
            decodedScore = None
            decodedValue = str(r.recognize_google(audio))
        decodedSentiment = evaluate(decodedValue)

        data = {
            'type': decodedType,
            'score': decodedScore,
            'text': decodedValue,
            'sentiment': decodedSentiment
        }

        print(str(data))

    except sr.UnknownValueError:
        print("Sphinx could not understand audio")

    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


r.listen_in_background(source=sr.Microphone(), callback=parse, phrase_time_limit=2)

count = 0
while True:
    count += 1