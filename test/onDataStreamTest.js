#!/usr/bin/env node

const NetcatClient = require('netcat/client')
const stream = require('stream')

var chunkCount = 1;

var dataStream = new stream.Writable({
  write: function( chunk, encoding, next ){
    console.log( chunk.toString() );
    console.log('ChunkCount: ' + chunkCount)
    ++chunkCount
    next();
  }
});

var ncc = new NetcatClient()
ncc.enc('utf8').unixSocket('/tmp/gemini-feed.sock').connect().pipe( dataStream )

//ncc.addr('127.0.0.1').port(2595 + testSize - testStartSize).connect().pipe( new Base64Encode() ).pipe( dataStream )
