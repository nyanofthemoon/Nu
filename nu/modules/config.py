# Config Reader

import configparser

def lmemory_config():
    return _readConfig('./nu/configs/lmemory.ini')

def nu_config():
    return _readConfig('./nu/configs/nu.ini')

def query_config():
    return _readConfig('./nu/configs/query.ini')

def runner_config():
    return _readConfig('./nu/configs/runner.ini')

def sense_config():
    return _readConfig('./nu/configs/sense.ini')

def skill_config():
    return _readConfig('./nu/configs/skill.ini')

def smemory_config():
    return _readConfig('./nu/configs/smemory.ini')

def _readConfig(path):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(path)
    return config