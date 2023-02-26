## 开发环境
- python 3.10
- MetaMask 版本 10.23.3(请勿使用chrome商店安装，不同版本会导致ui无法使用) [MateMask插件下载](https://github.com/MetaMask/metamask-extension/releases/download/v10.23.3/metamask-chrome-10.23.3.zip) `assets项目目录下自取也可`
***

## 开发配置相关

- windows配合指纹浏览器(hubstudio使用)
- settings/ProjectSettings.py里配置hubstudio的`APP_ID `,`APP_SECRET`,`GROUP_CODE`

- debug环境中手动执行cmd命令行开启hubstudio本地服务，打包后**不需要**了手动运行命令，会在启动时监听终端信息，hubstudio启动完毕**自动加载**ui界面
- `app_id` `group_code`与上边的配置是一样的，debug模式手动开启服务是为了不用每次开启调试都要先等待服务启动


**启动hubstudio命令(开发模式手动启用)**
```html
cd E:\Hubstudio\2.19.0.1&E:&hubstudio_connector.exe --server_mode=http --http_port=6873 --app_id={appId} --group_code={groupCode} --app_secret={appSecret}
```
***
## 打包相关
多文件打包，脚本会自动将需要的依赖文件复制到打包好的项目中
```html
pyinstaller -D main.py & xcopy assets\eth_account dist\main\eth_account\ /s & echo f| xcopy constant.json dist\main
```
***
## hubstudio配置相关
- 偏好设置里启动环境时改成仅检测页
***
