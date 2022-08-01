from pylceda import ScriptServer

ss=ScriptServer()

def script(api):
    result=api('getSource', {"type":'json'})
    print(result)
        
ss.bind_script("/py-plugin",script)#将脚本绑定在/py-plugin下
ss.mainloop()#启动服务