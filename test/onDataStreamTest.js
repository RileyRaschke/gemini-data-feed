#!/usr/bin/env node

const NetcatClient = require('netcat/client')
const stream = require('stream')

const socketPath = '/tmp/gemini-feed.sock'

var chunkCount = 1
var connected = false;

var dataStream = new stream.Writable({
  write: function( chunk, encoding, next ){
    console.log( chunk.toString() );
    console.log('ChunkCount: ' + chunkCount)
    ++chunkCount
    next();
  },
});

dataStream.on( 'close', () => { console.log( 'Connection closed.. was it listening?' ) } )
dataStream.on( 'error', () => { console.log( 'Connection closed.. was it listening?' ) } )
dataStream.on( 'finish', () => { console.log( 'Connection closed.. was it listening?' ) } )

setConnected = () => {
  connected = true
  console.log( 'connected' )
}

var ncc = new NetcatClient()
ncc.enc('utf8').unixSocket(socketPath).connect(setConnected).pipe(dataStream)

setTimeout( () => {
  if( ! connected ){
    console.log( 'Failed to connect to: ' + socketPath + ' -Is the server running?' )
  }
}, 1000)
