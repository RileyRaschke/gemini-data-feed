#!/bin/bash

ncat -l -U /tmp/gemini-btcusd.out -k --send-only < /tmp/gemini-btcusd.in

