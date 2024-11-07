const express = require('express');
const net = require('net');
const http = require('http');
const {Server} = require("socket.io");
const {spawn} = require('child_process');

const app = express();
const server = http.createServer(app);
const io = new Server(server);


const process = spawn('python3', ['./python/yolo.py']);

process.stdout.on('data', function (data) {
    console.log(data.toString("utf8"));
    // io.emit('img', data.toString("utf8"));
});
process.stderr.on('data', function (data) {
    console.log("error")
    console.log(data.toString("utf8"));
});

io.on("connection", (socket) => {

    socket.on('data', (data) => {
        console.log('클라이언트로부터 받은 데이터', data);
		process.stdin.write(data + "\n");
	});
    socket.on('disconnect', () => {
        console.log('클라이언트 접속 해제', socket.id);
        clearInterval(socket.interval);
    });
    socket.on('error', (error) => {
        console.error(error);
    });
});


app.set("view engine", "pug");
app.set("views", __dirname + "/views");
app.use("/public", express.static(__dirname + "/public"));
app.get("/", (_, res) => res.render("index"));
app.get("/*", (_, res) => res.redirect("/"));

const PORT = 8888;
server.listen(PORT,() => {
    console.log(`listening on *:${PORT}`);
});
