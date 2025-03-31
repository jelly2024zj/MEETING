import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # 从环境变量读取
    SQLALCHEMY_TRACK_MODIFICATIONS = False