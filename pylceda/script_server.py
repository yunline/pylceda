import pywss
from pylceda.interface import JLCInterface
from typing import Callable

class ScriptServer:
    def __init__(self):
        self.binding={}

    def mainloop(self):
        app = pywss.App()
        for route in self.binding:
            app.get(route,self.handler_factory(self.binding[route]))
        app.run(port=3579)

    def handler_factory(self,script):
        def _websocket(ctx: pywss.Context):
            # 升级 WebSocket
            err = pywss.WebsocketContextWrap(ctx)
            if err:
                ctx.log.error(err)
                ctx.set_status_code(pywss.StatusBadRequest)
                return
            # 轮询获取消息，阻塞式

            interface=JLCInterface(ctx.ws_read,ctx.ws_write)

            interface.script_start(script)
            interface.ws_loop()

        return _websocket

    def bind_script(self,route:str,script:Callable):
        self.binding[route]=script
    