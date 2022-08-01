import threading
import json
from typing import Callable
import queue

#主线程跑pywss（ws_loop()）
#脚本线程用于跑脚本

#脚本→api()→arg_queue→ws_loop()→_api()→return_queue→api()→脚本

class _StopConnection:pass

class JLCInterface:
    def __init__(self,ws_read:Callable,ws_write:Callable):
        self.ws_read=ws_read
        self.ws_write=ws_write

        self.arg_queue=queue.Queue()
        self.return_queue=queue.Queue()
    
    def script_start(self,_script):
        script=self.script_factory(_script)
        threading.Thread(target=script,args=(self.api,)).start()

    def script_factory(self,script):
        def _script(api):
            try:
                script(api)
            finally:
                self.arg_queue.put((_StopConnection(),{}))
        return _script


    def api(self,cmd,json_data):#脚本线程调用
        self.arg_queue.put((cmd,json_data))
        raw_data=self.return_queue.get()#阻塞
        return_data=json.loads(raw_data.decode("utf8"))#由json转字典
        return return_data

    def _api(self,cmd,json_data):#ws线程调用
        json_str=json.dumps({"cmd":cmd,"json":json_data},ensure_ascii=False)#转json
        self.ws_write(json_str.encode("utf8"))
        #阻塞，等待返回值
        return self.ws_read()

    def ws_loop(self):
        while 1:
            cmd,json_data=self.arg_queue.get()#阻塞
            
            if type(cmd)==_StopConnection:
                break
            else:
                return_data=self._api(cmd, json_data)#接收返回值
                self.return_queue.put(return_data)