class Config(object):
    SECRET_KEY = 'msqaidyq1314'
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/car_home"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True

class ProductConfig(Config):
    pass


config_map = {
    'develop':DevelopmentConfig,
    'product':ProductConfig
}