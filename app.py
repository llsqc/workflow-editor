from flask import Flask
from mongoengine import connect

from const import database


def create_app():
    the_app = Flask(__name__)

    # 注册蓝图
    # from api import train, forecast, manage
    # the_app.register_blueprint(train.bp, url_prefix='/train')  # 导入训练接口蓝图
    # the_app.register_blueprint(forecast.bp, url_prefix='/forecast')  # 导入预测接口蓝图
    # the_app.register_blueprint(manage.bp, url_prefix='/manage')  # 导入管理接口蓝图

    # 连接数据库MongoDB
    try:
        connect(
            db=database.db,
            host=database.host,
            port=database.port,
            username=database.username,
            password=database.password,
            authentication_source=database.authentication_source,
        )
    except ConnectionError as e:
        print(f"数据库连接失败:{e}")
    else:
        print("数据库连接成功")

    return the_app


if __name__ == '__main__':
    app = create_app()
    app.run()
