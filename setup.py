from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
  name='nu',
  version='0.1.0',
  packages=['nu'],
  author='Nyan Of The Moon',
  author_email='nyanofthemoon@gmail.com',
  description='Framework for creating Cozmo skills using multiple sensory inputs.',
  long_description=long_description,
  url='https://hotchiwawa.com',
  license='MIT',
  entry_points={
      'console_scripts': [
          'nu = nu.__main__:main'
      ]
  },
  install_requires=[
      'argparse',
      'configparser',
      'redis',
      'hiredis',
      'sense-hat',
      'cozmo[camera]',
      'SpeechRecognition',
      'PyAudio',
      'PocketSphinx',
      'python-Levenshtein',
      'google-api-python-client',
      'textblob'
  ],
  zip_safe=False
)
