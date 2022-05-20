from sqlalchemy import Column, Integer, String, DateTime
from app.database.models import DeclarativeBase


class Coleta(DeclarativeBase.Model):
    __tablename__ = 'coletas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    esl_id = Column(Integer, nullable=False)
    invoices_mapping = Column(String(255), nullable=False)
    sequence_code = Column(Integer)
    delivery_prediction = Column(DateTime)
    foe_reciver = Column(String(255))
    foe_ore_description = Column(String(255))
    lce_ore_description = Column(String(255))
    fis_id = Column(Integer, nullable=False)
    ioe_order_number = Column(String(255))
    ioe_pin_number = Column(String(255))

    def to_json(self):
        return dict(name=self.name, slug=self.slug, count=self.count)
