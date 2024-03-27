const http = require('http');
const express = require('express');
const cors = require('cors')
var socketio=require('socket.io');
const net = require('net');

const app = express();
const router = express.Router();

const port = 4000;

app.use(cors());
app.use(express.static('public'));
app.use(router)

const server = http.createServer(app);
server.listen(port, function(){
    console.log("서버 실행 중 : http://localhost:" + port);
});

var io = socketio(server);
let img = null;

let tcp = net.createServer(function (socket) {
    socket.setEncoding('utf8')

    socket.on('connect', function(data){
        console.log("연결됨")
    })

    socket.on('data', function (data) {
        console.log("------------")
        data = String(data);
        console.log(data.length)

        if(data.lastIndexOf("끝") !== -1) {
            data = data.split("끝");
            
            lat = data[1][0].charCodeAt(0)<<28 | data[1][1].charCodeAt(0)<<21 | data[1][2].charCodeAt(0)<<14 | data[1][3].charCodeAt(0)<<7 | data[1][4].charCodeAt(0)
            lon = data[1][5].charCodeAt(0)<<28 | data[1][6].charCodeAt(0)<<21 | data[1][7].charCodeAt(0)<<14 | data[1][8].charCodeAt(0)<<7 | data[1][9].charCodeAt(0)
            // console.log(data[0][0].charCodeAt(0)<<28 | data[0][1].charCodeAt(0)<<21)
            // console.log(data[0][0].charCodeAt(0).toString(2))
            // console.log(data[0][1].charCodeAt(0).toString(2))
            // console.log(data[0][2].charCodeAt(0).toString(2))
            // console.log(data[0][3].charCodeAt(0).toString(2))
            // console.log(data[0][4].charCodeAt(0).toString(2))
            // console.log(lat.toString(2))
            // console.log(lat.toString(16))
            console.log(lat)
            // console.log(lat.toString(2))
            console.log(lon)
            // console.log(lon.toString(2))
            // console.log("끝")
            io.emit('img', img+data[0]);
            img = data[1]
        }
        else {
            if(img !== null) img += data;
        }
    });
    socket.on('close', function () {
        console.log(`${socket.address()}client disconnected`);
    });
});

tcp.on('error', (err) => {
    console.log(err.code);
});
tcp.listen(8000, '192.168.137.1', () => {
    console.log('server listen', tcp.address());
});