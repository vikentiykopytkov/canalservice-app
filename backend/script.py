from db.models import Order
from ggl import handler
import settings

from datetime import datetime
from tortoise import Tortoise
import httpx
import asyncio

async def db_init():
    await Tortoise.init(
        db_url=f'postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_CONTAINER_NAME}:5432/{settings.POSTGRES_DB}',
        modules={'models': ['db.models']}
    )

    await Tortoise.generate_schemas()


async def update_data():
    await asyncio.sleep(3) # Время на инициализацию базы данных

    while True:
        all_numbers = [obj.number for obj in await Order.all()] # Список с текущими номерами в базе данных (необходим для удаления элементов более не существующих в Google-таблицы)

        data = handler.get_handled_data()

        for row in data:
            if not await Order.filter(number=row [1]).first():
                order = Order(
                    google_id=row [0], 
                    number=row [1], 
                    price_usd=row [2], 
                    price_rub=row [3], 
                    date=row [4],
                    telegram_flag=False)
                await order.save()

                all_numbers.remove(row [1]) if row [1] in all_numbers else None
            else:
                order_obj = await Order.get(number=row [1])
                order = await Order.get(number=row [1]).update(
                    google_id=row[0],
                    price_usd=row [2], 
                    price_rub=row [3], 
                    date=row [4],
                    telegram_flag=False if order_obj.date != row [4] else order_obj.telegram_flag # Если дата поставки изменилась - выполнить оповещение в телеграме ещё раз
                )
                all_numbers.remove(row [1]) if row [1] in all_numbers else None
        
        [await Order.filter(number=number).delete() for number in all_numbers]

        await telegram_check()
        await asyncio.sleep(settings.UPDATE_RATE)


async def telegram_check():
    expired_objects = ['№' + str(obj.number) if datetime.now().date() >= obj.date else None for obj in await Order.filter(telegram_flag=False).all()]
    if expired_objects:
        async with httpx.AsyncClient() as client:
            await client.post(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT}/sendMessage', json={
                'chat_id': settings.ADMIN_CHAT_ID,
                'text': f"<b>Уведомление</b>\n\nСрок поставки заказа истёк:\n" + '\n'.join(expired_objects),
                'parse_mode': 'HTML'
            })
            await asyncio.sleep(1)
        [await Order.filter(number=number[1:]).update(telegram_flag=True) for number in expired_objects]
