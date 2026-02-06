import io from "socket.io-client";

const socket = io("http://10.0.0.1:9000");

socket.on("connect", () => {
	console.log("Conectado");
	socket.emit("data", { mensaje: "Hola servidor" });
});

socket.on("response", (msg) => {
	console.log("Respuesta:", msg);
});