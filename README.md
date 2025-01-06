# workflow-editor

## 应用启动方式

### 基于docker

基于docker启动步骤如下

- 在有docker的linux环境下，进入`/scripts`目录，执行`make`命令即可
- windows系统推荐使用wsl

### 手动部署

手动部署需要如下步骤

- 在本地部署一个mongoDB
- 并将`/biz/infra/consts/database.py`文件下相应的配置修改为本地配置
- 通过python命令运行`app.py`文件
- 运行`/scripts/case.py`生成样例

## 说明

后端项目运行在5000端口处
前端项目预选在3000端口处