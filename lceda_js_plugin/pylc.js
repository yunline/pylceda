class PythonInterface {
    constructor(addr = "ws://127.0.0.1:3579") {
        var route = prompt("请输入插件路径", "/py-plugin")
        this.ws = new WebSocket(addr + route);
        this.ws.onmessage = function (event) {
            var data = JSON.parse(event.data);

            var cmd = data["cmd"];
            var _json = data["json"];

            //console.log("cmd:", cmd, "  json:", _json);

            var result = api(cmd, _json)//勇敢牛牛，不怕注入
            if(result==undefined){
                result="undefined";
            }

            //console.log("return:",result)

            this.send(JSON.stringify(result))
        }
        this.ws.onclose = function (event) {
            console.log('Connect Closed');
        }
        this.ws.onopen = function () {
            if (this.readyState === WebSocket.OPEN) {
                console.log('Connected');
            }
        }
    }
    send(data) {
        this.ws.send(data);
    }
    close() {
        this.ws.close();
    }
}

var pi = new PythonInterface();