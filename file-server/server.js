var express = require('express');
var fs = require("fs");
var uuid = require('node-uuid');
var redis = require('redis');

var PORT = 3000;

var DATA_DIR = '/data/';
var OUT_DIR = '/out';

var app = express();

// Connect to redis
var redisClient = redis.createClient(6379, 'redis', {});

var counter = 0;

// Parse command-line arguments

process.argv.forEach(function(val, index, array) {
	console.log(index + ': ' + val);
});

/**
 */
app.get('/', function(req, res) {
	var message = {
		message: 'File cache server is running...'
	}
	res.send(message)
});

/**
For streaming data from file
*/
app.get('/data/:id', function(req, res) {
	var fileId = req.params.id;
	var stream = fs.createReadStream(__dirname + DATA_DIR + fileId + '.json');
	stream.pipe(res);
});


app.get('/data/:id', function(req, res) {
	var fileId = req.params.id;
	var stream = fs.createReadStream(__dirname + DATA_DIR + fileId + '.json');
	stream.pipe(res);
});

/**
	For streaming POST request doby into file
*/
app.post('/data', function(req, res) {
	var fileId = uuid.v1();

	var writeStream = fs.createWriteStream(__dirname + DATA_DIR + fileId + '.json');

	// This pipes the POST data to the file
	req.pipe(writeStream);
	req.on('end', function() {
		var message = {
			fileId: fileId
		};
		res.send(message);
	});

});


var server = app.listen(PORT, function() {
	var host = server.address().address;
	var port = server.address().port;

	console.log(server.address())
});