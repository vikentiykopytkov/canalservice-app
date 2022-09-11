from flask import Flask
from flask_cors import CORS

from db.models import Order

app = Flask(__name__)
CORS(app)

@app.get('/orders')
async def get_orders():
    orders = await Order.all().order_by('google_id')
    return {
        'total': sum([obj.price_usd for obj in orders]),
        'orders': [{
            'google_id': obj.google_id,
            'number': obj.number,
            'price_usd': obj.price_usd,
            'price_rub': obj.price_rub,
            'date': obj.date.strftime('%d.%m.%Y'),
        } for obj in orders]
    }


@app.get('/orders_sum')
async def get_orders_sum():
    orders = await Order.all()
    data = {}
    for order in orders:
        data [order.date.strftime('%d.%m.%Y')] = sum([obj.price_usd for obj in await Order.filter(date=order.date).all()])
    return [{'date': date, 'price_usd': data [date]} for date in data.keys()]