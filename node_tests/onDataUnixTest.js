#!/usr/bin/env node

console.log("This is broken, see: https://github.com/roccomuso/netcat/issues/11");
console.log("Use the stream implementation instead, see: test/onDataStreamTest.js");
return;

const NetcatClient = require('netcat/client');

const { spawn } = require('child_process')

var CHUNK_COUNT = 100 // Breaks around chunk 34
// var CHUNK_COUNT = 10 // SUCCESSFUL

var bashDataFeedServer = `
  for i in {1..${CHUNK_COUNT}}
  do
    cat /dev/urandom | base64 | dd bs=100 count=10
    sleep 0.1
  done | nc -l -q 1 -U /tmp/test.sock
`
// var child = spawn('bash', ['-c', bashDataFeedServer])
spawn('bash', ['-c', bashDataFeedServer])

var nc = new NetcatClient()

var chunkCount = 0
// nc.enc('utf8').retry(1).interval(1).unixSocket('/tmp/gemini-feed.sock').connect()
//nc.enc('utf8').unixSocket('/tmp/gemini-feed.sock').connect()
nc.enc('utf8').unixSocket('/tmp/test.sock').connect()
  .on('data', (chunk) => {
    ++chunkCount
    process.stdout.write(`Chunkcount: ${chunkCount} - chunkSize: ${chunk.length} \n`)
  })
