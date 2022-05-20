
class Config:
    pass


class DevelopmentConfig(Config):
    DATABASE_URI = 'mysql://root:@localhost/teste_mysql'


class ProductionConfig(Config):
    pass
