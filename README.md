# workflow-editor

## 应用启动方式i

### 基于docker

基于docker启动步骤如下
- 在docker环境下，进入`/scripts`目录，执行`make`命令即可

### 手动部署

手动部署需要如下步骤
- 在本地部署一个mongoDB
- 并将`/biz/infra/consts/database.py`文件下相应的配置修改为本地配置
- 通过python命令运行`app.py`文件