var express = require('express');
var fs = require("fs");

var PORT = 3000;

var DATA_DIR = '/data';
var OUT_DIR = '/out';

var app = express();

var counter = 0;

/**
*/
app.get('/', function (req, res) {
	var message = {
		message: 'File cache server is running...'
	}
    res.send(message)
});

/**
For streaming data from file
*/
app.get('/test', function (req, res) {
	var stream = fs.createReadStream(__dirname + DATA_DIR + '/test.txt');
    stream.pipe(res);
});

app.get('/data/:id', function (req, res) {
	var fileId = req.params.id;
	var stream = fs.createReadStream(__dirname + DATA_DIR + '/test_' + fileId + '.json');
    stream.pipe(res);
});

/**
For streaming POST request doby into file
*/
app.post('/data', function(req, res) {
	var writeStream = fs.createWriteStream(__dirname + DATA_DIR + '/test_' + (counter++) + '.json');

  	// This pipes the POST data to the file
  	req.pipe(writeStream);
  	req.on('end', function () {
	  	var message = {
	  		message: 'success'
	  	}
	  	res.send(message);
  	});

});



var server = app.listen(PORT, function () {

  var host = server.address().address;
  var port = server.address().port;
  console.log(server.address())
  console.log("File Server is listening at http://%s:%s", host, port);

});