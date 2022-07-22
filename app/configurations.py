from sqlalchemy import engine


class Config:
    pass


class DevelopmentConfig(Config):
    DATABASE_URI = 'mysql://root:@localhost/pythonetlexpress'


class ProductionConfig(Config):
    DATABASE_URI = engine.URL.create(
        drivername="mysql",
        username="root",
        password="@tkx31Na9",
        host="192.168.1.205",
        database="teste_mysql"
    )
