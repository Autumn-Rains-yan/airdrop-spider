# TODO: 感觉写的不好看，以后看看有没有别的办法
filename = "constant.json"
contents = open(filename).read()
config = eval(contents)


HubStudioPath = config['HubStudioPath']
BasePath = config['BasePath']
MetaMaskId = config['MetaMaskId']
APP_ID = config['APP_ID']
APP_SECRET = config['APP_SECRET']
GROUP_CODE = config['GROUP_CODE']
