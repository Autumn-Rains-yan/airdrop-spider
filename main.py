from time import sleep

from gui.GuiMain import initGui

from settings import ProjectSettings
from settings.ProjectSettings import BASE_DIR
from settings.UserSettings import HubStudioPath, BasePath

import subprocess

if __name__ == '__main__':
    # 初始化创建account.txt
    file = open(BASE_DIR + '/account.txt', 'a')
    file.close()
    if not ProjectSettings.DEBUG:
        print('正在启动HubStudio服务...')
        # 服务启动线程
        res = subprocess.Popen(f"cd {HubStudioPath}&{BasePath}&{ProjectSettings.CMD_HUB}",
                               shell=True, stdout=subprocess.PIPE)
        serverType = ''
        runTimes = 0
        while serverType == '':
            for i in res.stdout.readlines(100):
                if 'starting' in str(i):
                    serverType = 'success'
                elif 'started' in str(i):
                    serverType = 'alreadySuccess'
            runTimes = runTimes + 1
            if runTimes > 200:
                break
        if serverType == 'success':
            print('HubStudio服务启动完成')
            initGui()
        elif serverType == 'alreadySuccess':
            print('有正在运行的HubStudio服务')
            initGui()
        print('未知错误，60秒后窗口将自动关闭，请将完整错误信息截图并发送给开发人员调试')
        sleep(60)
    else:
        initGui()



