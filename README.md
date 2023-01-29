- 开发者请移步开发指南[开发文档](https://github.com/Autumn-Rains-yan/airdrop-spider/blob/main/README.dev.md)
- 目前项目仅支持windows，理论上是可以跨平台的，后续会进行开发
---
### 环境配置
- HubStudio指纹浏览器(v2.19.0.1)
[64位下载](https://www.hubstudio.io/xxxlllyyy/123/2.19.0.1/64/HubstudioSetup-v2.19.0.1_x64.exe)
[32位下载](https://www.hubstudio.io/xxxlllyyy/123/2.19.0.1/32/HubstudioSetup-v2.19.0.1_x86.exe)
[帮助中心](https://support.hubstudio.cn/7cc7/4d9b)
- MetaMask钱包，请勿使用最新版本，请下载后手动导入指纹浏览器 [MateMask插件下载v10.23.3](https://github.com/MetaMask/metamask-extension/releases/download/v10.23.3/metamask-chrome-10.23.3.zip)
```html
配置详情:
1:在HubStudio中获取APP_ID，APP_SECRET，GROUP_CODE
2:手动下载MetaMask钱包，导入HubStudio
3:浏览器扩展程序页面获取扩展程序ID
4:配置填入应用根目录下constant.json
```
### 应用使用介绍
- 项目运行脚本时，请关闭杀毒软件(报毒是因为脚本会有模拟操作，非恶意程序)
- 在HubStudio手动创建的环境理论上和工具内创建的功能相同

##### 菜单介绍
- 菜单->关于
- 菜单->检索eth: `做的一个小玩具，没有实际作用，通过web3生成助记词，私钥和地址，去扫该地址下是否有eth，有则存入本地文件`
- 菜单->退出
- 工具->批量新建环境: `一次创建50个HubStudio环境`
- 工具->批量创建小狐狸账号: `一次性创建50个MetaMast账号，该账号为冷钱包账号，后续会增加断网启用工具的功能`
- 工具->清除HubStudio缓存

##### 功能
- 全选
- 删除环境: `选中想要删除的环境`
- 小狐狸绑定: `工具首次运行后，会在根目录下自动创建account.txt文件，使用批量创建小狐狸账号功能创建账号后，粘贴进该文件即可，该功能是在HubStudio浏览器上登录MetaMask`
- 启动: `目前预留的脚本启动功能，当前暂时无法使用`
