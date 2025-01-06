from flask import Flask
from flask_cors import CORS

from biz.controller import call, agent, scene
from biz.infra.config.log_config import log_init
from biz.infra.config.mongo_config import mongo_init


def create_app():
    """
    创建并配置 Flask 应用程序。

    Returns:
        Flask: 配置后的 Flask 应用程序实例。
    """
    # 创建 Flask 应用实例
    the_app = Flask(__name__)

    # 注册蓝图
    the_app.register_blueprint(agent.bp)  # 从 biz.controller.agent 导入蓝图并注册
    the_app.register_blueprint(scene.bp)  # 从 biz.controller.scene 导入蓝图并注册
    the_app.register_blueprint(call.bp)  # 从 biz.controller.call 导入蓝图并注册

    # 初始化日志配置
    log_init()

    # 初始化 MongoDB 配置
    mongo_init()

    # 初始化跨域策略配置
    CORS(the_app)

    return the_app


if __name__ == '__main__':
    """
    应用程序入口点。
    """
    # 创建并配置 Flask 应用
    app = create_app()
    # 运行 Flask 应用
    app.run("0.0.0.0", port=5000)
