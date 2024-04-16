document.addEventListener('DOMContentLoaded', () => {
    const socket = io(); // 서버에 접속
    const startBtn = document.getElementById("startBtn");

    startBtn.addEventListener("click", () => {
		console.log("click")
        socket.emit("data", "start");
    });
});