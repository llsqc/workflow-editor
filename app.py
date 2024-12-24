from flask import Flask
from flask_cors import CORS

from biz.controller import call
from biz.infra.config.mongo_config import mongo_init


def create_app():
    the_app = Flask(__name__)

    # 注册蓝图
    from biz.controller import agent
    the_app.register_blueprint(agent.bp)
    the_app.register_blueprint(call.bp)
    # 连接数据库MongoDB
    mongo_init()

    CORS(the_app)

    return the_app


if __name__ == '__main__':
    app = create_app()
    app.run()
