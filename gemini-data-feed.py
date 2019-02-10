#!/usr/bin/env python3
###
# Author: Riley Raschke <rileyATrrappsdevDOTcom>
# © 2019 rrappsdev.com
##

import sys
import os
import argparse
from pprint import pprint
from yaml import load

from main import Main

yourCwd = os.path.realpath('.')
myself  = os.path.basename(__file__)

CONFIG_SEARCH_PATHS = [f"~/etc/{myself}.yaml", f"./etc/{myself}.yaml", f"/etc/{myself}.yaml"]

FEED_URI_PREFIX='wss://api.gemini.com/v1/marketdata/'
DEFAULT_SOCKET='/tmp/gemini-feed.sock'
DEFAULT_TICKER_SYMBOL='btcusd'
DEPTH_PERCENT_DEFAULT=0.01

opts = argparse.ArgumentParser(
    description="Massage/Merge raw gemini websocket feeds and rebroadcast on local network interfaces."
)
opts.add_argument('-c', '--config', type=str, metavar=f"~/etc/{myself}.yaml", help='Use config file <CONFIG>')

opts.add_argument('-t', '--tickers',
    type=str, nargs='+', metavar=DEFAULT_TICKER_SYMBOL, default='',
    help='Ticker string and optional depth percent. ex: btcusd ethbtc:0.02 bchusd:05 '
)
opts.add_argument('-p', '--socket', '--port',
    type=str, metavar=DEFAULT_SOCKET, default='',
    help='Server interface, port or socket; path to socket must exists'
)
opts.add_argument('-d', '--depthPercent',
    type=float, metavar=DEPTH_PERCENT_DEFAULT, default=0.0,
    help='Orderbook depth as percent display of last price or best bid/offer as a float where 1.0 == 100%%'
)
opts.add_argument('-f', '--feedUri',
    type=str, metavar=FEED_URI_PREFIX, default='',
    help='Gemini wss:// feed URI'
)

args = opts.parse_args()

# If you provided a config, try it first, if it exists
if args.config:
    if not os.access(args.config, os.R_OK ):
        sys.stderr.write(f"Unable to read config at: {args.config}\n")
        sys.exit(1);
    else:
        CONFIG_SEARCH_PATHS.insert(0, args.config)

conf={}
for maybeConfig in CONFIG_SEARCH_PATHS:
    if len(conf.keys()) == 0:
        try:
            with open( maybeConfig, 'r') as stream:
                #log.debug("Trying to load: " + maybeConfig)
                conf = load( stream )
                args.config = maybeConfig
        except Exception as e:
            #sys.stderr.write(f"Tried: {maybeConfig} got: {e}\n")
            pass

if not args.depthPercent and 'defaultDepthPercent' in conf.keys():
       args.depthPercent = conf['defaultDepthPercent']
if not args.depthPercent: args.depthPercent = DEPTH_PERCENT_DEFAULT

cmdTickers = args.tickers
args.tickers = {}
for ticker in cmdTickers:
    try:
      (t,d) = ticker.split(':')
      args.tickers[t] = float(d)
    except Exception as e:
      args.tickers[ticker] = args.depthPercent

if not args.tickers and 'tickers' in conf.keys():
       args.tickers = conf['tickers']
if not args.tickers:
       args.tickers = {DEFAULT_TICKER_SYMBOL:DEPTH_PERCENT_DEFAULT}
if not args.socket  and 'serverFeedSocket' in conf.keys():
       args.socket  = conf['serverFeedSocket']
if not args.socket:
       args.socket  = DEFAULT_SOCKET
if not args.feedUri and 'sourceFeedUri' in conf.keys():
       args.feedUri = conf['sourceFeedUri']
if not args.feedUri:
       args.feedUri = FEED_URI_PREFIX

#print( "You are in:", yourCwd )
#print( "Program is file:", myself )
#print( "Config search paths:", CONFIG_SEARCH_PATHS )
#print( "Program is in path:", __file__ )
#print( args )
print( "Resolved conf:" )
pprint( args.__dict__ )

# Create program with opts
svc = Main.Main( args.feedUri, args.tickers, args.socket)

# Run program
sys.exit( svc.run() )

