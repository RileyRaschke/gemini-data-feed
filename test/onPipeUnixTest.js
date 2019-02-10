#!/usr/bin/env node

const NetcatClient = require('netcat/client');

const { spawn } = require('child_process')

var bashDataFeedServer = `
  for i in {1..100}
  do
    cat /dev/urandom | base64 | dd bs=100 count=10
    sleep 0.1
  done | nc -l -q 1 -U /tmp/test.sock
`
spawn('bash', ['-c', bashDataFeedServer])

var nc = new NetcatClient()

nc.enc('utf8').unixSocket('/tmp/test.sock').connect().pipe(process.stdout)
