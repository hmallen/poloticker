from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='poloticker',
    version='0.1dev',
    author='Hunter M. Allen',
    author_email='allenhm@gmail.com',
    license='MIT',
    #packages=find_packages(),
    packages=['poloticker'],
    #scripts=['bin/heartbeatmonitor.py'],
    install_requires=['poloniex',
                      'pymongo',
                      'slackclient',
                      'websocket'],
    description='MongoDB-based OHLC ticker for Poloniex markets with Slack integration, using websockets as data feed.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hmallen/poloticker',
    keywords=['poloniex', 'ticker', 'slack'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
