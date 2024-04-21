const express = require('express');
const net = require('net');
const http = require('http');
// const https = require('https');
const {Server} = require("socket.io");

const {spawn} = require('child_process');


// let options = require("./.config/pem_config").options;

const app = express();
const server = http.createServer(app);
// const server = https.createServer(options, app);
const io = new Server(server);
const ipaddr = "0.0.0.0";
// const ipaddr = "172.23.246.241";



let py_data = "";
const python = spawn('python3', ['/python/dino.py']);
python.stdout.setEncoding("utf8");

python.stdout.on('data', function (data) {
	if(data.lastIndexOf("_E_") !== -1)
	{
		data = data.split("_E_");
		py_data += data[0];

		io.emit('img', py_data);
		py_data = data[1];
	}
	else
		py_data += data;
});
python.stderr.on('data', function (data) {
    console.log("error")
    console.log(data.toString("utf8"));
});


let process_data = "";
let status = {};
let tcp = net.createServer(function (socket) {
    socket.setEncoding('utf8')

    socket.on('data', function (data) {
        if(data.lastIndexOf("_E_") !== -1)
		{
			// console.log(data);
            data = data.split("_E_");
			process_data += data[0];
			process_data = process_data.split("_D_");
			img = process_data[0];
			

			{
			lat = process_data[1][0].charCodeAt(0)<<28 | process_data[1][1].charCodeAt(0)<<21 | process_data[1][2].charCodeAt(0)<<14 | process_data[1][3].charCodeAt(0)<<7 | process_data[1][4].charCodeAt(0)
            lon = process_data[1][5].charCodeAt(0)<<28 | process_data[1][6].charCodeAt(0)<<21 | process_data[1][7].charCodeAt(0)<<14 | process_data[1][8].charCodeAt(0)<<7 | process_data[1][9].charCodeAt(0)
            alt = process_data[1][10].charCodeAt(0)<<7 | process_data[1][11].charCodeAt(0)
			speed = process_data[1][14].charCodeAt(0)<<7 | process_data[1][15].charCodeAt(0)
            battery = process_data[1][12].charCodeAt(0)<<7 | process_data[1][13].charCodeAt(0)
			
			status['name'] = "test_name";
			status['speed'] = speed;
			status['rotateX'] = 10;
			status['rotateY'] = 10;
			status['rotateZ'] = 10;
			status['gpsX'] = lat/10000000.0;
			status['gpsY'] = lon/10000000.0;
			status['gpsZ'] = alt;
			status['battery'] = battery/10;
			status['mode'] = 1;
			}

			io.emit('status', status);
			python.stdin.write(img + "\n");
            process_data = data[1]
			socket.write('sat');
        }
		else 
        	process_data += data;
    });

    socket.on('close', function () {
		for (key in status){
			if (key != 'name')
				status[key] = "None"
			else 
				status[key] = 'disconnect';
		}

		io.emit('status', status);
        console.log(`${socket.address()}client disconnected`);
    });
});
tcp.on('error', (err) => {
    console.log(err.code);
});
tcp.listen(8484, ipaddr, () => {
    console.log('server listen', tcp.address());
});


io.on("connection", (socket) => {
    console.log(`클라이언트 접속 ${socket.id}`);
    io.emit('client_data', `USER: ${socket.id} Enter\n`)

    socket.on('data', (data) => {
        console.log('클라이언트로부터 받은 데이터', data);
        io.emit(data)
        tcp.emit(data)
    });
    socket.on('client_data', (data) => {
        console.log('클라이언트간 전송 데이터', data);
        io.emit(data)
    })
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

const PORT = process.env.PORT || 8888;
server.listen(PORT,() => {
    console.log(`listening on *:${PORT}`);
});
