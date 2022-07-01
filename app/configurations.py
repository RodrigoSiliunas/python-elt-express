
class Config:
    pass


class DevelopmentConfig(Config):
    DATABASE_URI = 'mysql://root:@localhost/siliunas_testes'


class ProductionConfig(Config):
    pass
