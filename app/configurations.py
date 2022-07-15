from sqlalchemy import engine


class Config:
    pass


class DevelopmentConfig(Config):
    DATABASE_URI = 'mysql://root:@localhost/pythonetlexpress'


class ProductionConfig(Config):
    DATABASE_URI = engine.URL.create(
        drivername="mysql",
        username="root",
        password="",
        host="localhost",
        database="teste_mysql"
    )
