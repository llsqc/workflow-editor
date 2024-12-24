import logging

from mongoengine import connect

from biz.infra.consts import database


def mongo_init():
    """
    初始化MongoDB数据库连接
    """
    try:
        connect(
            db=database.MONGO_DB,
            host=database.MONGO_HOST,
            port=database.MONGO_PORT,
            username=database.MONGO_USERNAME,
            password=database.MONGO_PASSWORD,
            authentication_source=database.MONGO_AUTHENTICATION_SOURCE,
        )
    except Exception as e:
        logging.error(f"MongoDB连接失败:{e}")
        exit(1)
    else:
        logging.info("MongoDB连接成功")
