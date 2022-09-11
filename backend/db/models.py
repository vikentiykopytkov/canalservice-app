import numbers
from tortoise.models import Model
from tortoise import fields


class Order(Model):
    id = fields.IntField(pk=True)
    #: ID из Google-таблицы
    google_id = fields.IntField()
    #: Номер заказа
    number = fields.IntField()
    #: Стоимость в долларах
    price_usd = fields.IntField()
    #: Стоимость в рублях
    price_rub = fields.IntField()
    #: Дата поставки
    date = fields.DateField()
    #: Отправлено ли уведомление в телеграме
    telegram_flag = fields.BooleanField()