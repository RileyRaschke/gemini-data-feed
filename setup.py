
from distutils.core import setup

requires = [
'websocket_client',
'PyYAML',
]

setup(
    name='GeminiDataService',
    version='0.1.0',
    author='Riley Raschke',
    author_email='riley@rrappsdev.com',
    packages=['geminidata.service','geminidata.feed'],
    scripts=['bin/geminidata-service.py'],
    url='',
    license='LICENSE',
    description='Merge/Massage Gemini Data feeds, as a service',
    long_description='Massage gemini websocket feeds while broadcasting to unix socket',
    install_requires=requires
)

