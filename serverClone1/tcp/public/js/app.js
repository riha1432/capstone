function textarea_add(textareaElement, str) {
    textareaElement.innerHTML += (str);
    textareaElement.scrollTop = textareaElement.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // 서버에 접속
    const videoItem = document.getElementById("video-item"); // video-item 태그
    const startBtn = document.getElementById("startBtn");
    const stopBtn = document.getElementById("stopBtn");
    const resetBtn = document.getElementById("resetBtn");
    const log = document.getElementById("log");
    // const container = document.getElementById("map");

	const status_name = document.getElementById("status_name");
	const status_speed = document.getElementById("status_speed");
	const status_rotateX = document.getElementById("status_rotateX");
	const status_rotateY = document.getElementById("status_rotateY");
	const status_rotateZ = document.getElementById("status_rotateZ");
	const status_gpsX = document.getElementById("status_gpsX");
	const status_gpsY = document.getElementById("status_gpsY");
	const status_gpsZ = document.getElementById("status_gpsZ");
	const status_battery = document.getElementById("status_battery");
	const status_mode = document.getElementById("status_mode");


    // let options = { //지도를 생성할 때 필요한 기본 옵션
    //     center: new kakao.maps.LatLng(35.9084, 128.8018), //지도의 중심좌표.
    //     level: 6, //지도의 레벨(확대, 축소 정도)
    //     disableDoubleClick: false, //더블 클릭 이벤트 및 더블 클릭 확대가능여부
    // };
    // let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
    // var marker = new kakao.maps.Marker({
    //     map: map,
    //     position: new kakao.maps.LatLng(35.9084, 128.8018)
    // });
    // marker.setMap(map);

    startBtn.addEventListener("click", () => {
        socket.emit("data",`USER-${socket.id} to server: "start"\n`);
        textarea_add(log, `USER: ${socket.id} to server: "start"\n`);
    });
    stopBtn.addEventListener("click", () => {
        socket.emit("data",`USER-${socket.id} to server: "stop"\n`);
        textarea_add(log, `USER: ${socket.id} to server: "stop"\n`);
    });
    resetBtn.addEventListener("click", () => {
        socket.emit("data",`USER-${socket.id} to server: "reset"\n`);
        textarea_add(log, `USER: ${socket.id} to server: "reset"\n`);
    });

    socket.on("img", (data) => {
        videoItem.src = `data:image/jpg;base64,${data}`;
        videoItem.onerror = () => {
            textarea_add(log,"CLIENT: Image loading failed\n");
        };
    });
	socket.on('status', (data) => {
		if(data === null) return;
		status_name.innerHTML = data.name;
		status_speed.innerHTML = data.speed;
		status_rotateX.innerHTML = data.rotateX;
		status_rotateY.innerHTML = data.rotateY;
		status_rotateZ.innerHTML = data.rotateZ;
		status_gpsX.innerHTML = data.gpsX;
		status_gpsY.innerHTML = data.gpsY;
		status_gpsZ.innerHTML = data.gpsZ;
		status_battery.innerHTML = data.battery;
		status_mode.innerHTML = data.mode;
		// marker.setPosition(new kakao.maps.LatLng(data.gpsX, data.gpsY));
	});
    socket.on("client_data", function (data) {
        textarea_add(log, data);
    });
});