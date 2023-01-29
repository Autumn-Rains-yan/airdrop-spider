import json
import requests

from settings import ProjectSettings


class Api:

    def __init__(self):
        pass

    def apiPostIntercept(self, url, data):
        response = requests.post(url=url, data=json.dumps(data))
        if response.status_code == 200 and json.loads(response.text)['code'] == 0:
            return json.loads(response.text)['data']
        else:
            if response.status_code != 200:
                print('网络错误，服务暂未开启，请联系开发者')
            else:
                print(json.loads(response.text)['msg'])

    def apiGetIntercept(self, url, params):
        response = requests.get(url=url, params=params)
        if response.status_code == 200 and json.loads(response.text)['code'] == 0:
            return json.loads(response.text)['data']
        else:
            if response.status_code != 200:
                print('网络错误，服务暂未开启，请联系开发者')
            else:
                print(json.loads(response.text)['msg'])

    # 创建环境
    def createEnv(self):
        url = ProjectSettings.HTTP_BASE + '/api/v1/env/create'
        name = '自动创建环境a'
        data = {
            'containerName': name,
            'asDynamicType': 1,
            'proxyTypeName': '不使用代理',
        }
        for i in range(0, 50):
            print('正在创建第' + str(i) + '个环境')
            data['containerName'] = name + str(i)
            self.apiPostIntercept(url=url, data=data)
            print('第' + str(i) + '个环境创建成功')

    # 获取环境列表
    def getEnvList(self):
        print('正在获取环境列表...')
        data = {
            'size': 200
        }
        url = ProjectSettings.HTTP_BASE + '/api/v1/env/list'
        print('获取环境列表成功!')
        return self.apiPostIntercept(url=url, data=data)

    # 打开环境
    def openEnv(self, containerCode):
        print('正在打开环境' + str(containerCode) + '...')
        url = ProjectSettings.HTTP_BASE + '/api/v1/browser/start'
        data = {
            'containerCode': containerCode,
            'isWebDriverReadOnlyMode': True,
            "args": [
                # "--disable-extensions",
                "--blink-settings=imagesEnabled=false"
            ]
        }
        res = self.apiPostIntercept(url=url, data=data)
        print('打开环境成功')
        return res

    # 关闭环境
    def closeEnv(self, containerCode):
        print('正在关闭环境' + str(containerCode) + '...')
        url = ProjectSettings.HTTP_BASE + '/api/v1/browser/stop'
        params = {
            'containerCode': containerCode,
        }
        res = self.apiGetIntercept(url=url, params=params)
        print('关闭环境成功')
        return res

    # 删除环境
    def deleteEnv(self, containerCodes):
        print('正在删除环境' + str(containerCodes) + '...')
        url = ProjectSettings.HTTP_BASE + '/api/v1/env/del'
        data = {
            'containerCodes': containerCodes,
        }
        res = self.apiPostIntercept(url=url, data=data)
        return res

    # 清除环境缓存,打开环境时返回的browserID，参数不传则删除所有环境的本地缓存
    def clearEnvCache(self, browserID=''):
        print('正在清除缓存')
        if browserID != '':
            data = {
                'browserOauths': browserID
            }
        else:
            data = {}
        url = ProjectSettings.HTTP_BASE + '/api/v1/cache/clear'
        res = self.apiPostIntercept(url=url, data=data)
        print('清除缓存成功')
        return res