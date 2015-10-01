//
// Very simple file server built on top of express.js
//

var express = require('express');
var fs = require("fs");
var uuid = require('node-uuid');
var glob = require("glob");

var PORT = 3000;

var DATA_DIR = '/data/';

// Create a server instance
var app = express();

// Parse command-line arguments
process.argv.forEach(function (val, index, array) {
    console.log(index + ': ' + val);
});

////////////// API Definitions ///////////////////////

/**
 * GET status of the server.
 */
app.get('/', function (req, res) {
    var message = {
        version: '0.1.0',
        message: 'Node.js file cache server is running...'
    };

    res.send(message)
});


/**
 * GET data from a file
 */
app.get('/data/:id', function (req, res) {
    var fileId = req.params.id;
    console.log('Opening input data file: ' + fileId);

    var stream = fs.createReadStream(__dirname + DATA_DIR + fileId + '.json');
    stream.pipe(res);
});


/**
 * GET list of all files in the server
 */
app.get('/data', function (req, res) {
    var fileList = [];

    glob("data/*.json", function (er, files) {
        files.forEach(function(path){
            var parts = path.split('/');
            fileList.push(parts[1]);
        });
        res.send(fileList);
    });
});


/**
 * POST request body into a file
 */
app.post('/data', function (req, res) {
    // Generate file ID
    var fileId = uuid.v1();

    var writeStream = fs.createWriteStream(__dirname + DATA_DIR + fileId + '.json');
    req.pipe(writeStream);
    req.on('end', function () {
        var message = {
            fileId: fileId
        };
        res.send(message);
    });
});

app.delete('/data', function(req, res) {
    glob("data/*.json", function (er, files) {
        files.forEach(function(path){
            fs.unlinkSync(path);
        });
        var message = {
            message: 'Success deleting all data files.'
        };
        res.send(message);
    });
});


app.delete('/data/:id', function (req, res) {
    var fileId = req.params.id;
    fs.unlinkSync(__dirname + DATA_DIR + fileId + '.json');
    var message = {
        message: 'Success deleting a data file: ' + fileId
    };
    res.send(message);
});


// Start listening...
var server = app.listen(PORT, function () {
    console.log(server.address())
});