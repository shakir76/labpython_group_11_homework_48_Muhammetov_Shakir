from django.core.management.base import BaseCommand
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging

from telegram.utils.request import Request

from e_shop.settings import TELEGRAM_BOT_API_KEY
from shop.models import Order, OrderProduct


def start(update: Update, context: CallbackContext):
    print(update.effective_chat)
    print(update.effective_user)
    orders = Order.objects.all()
    len_order = orders.count()

    update.message.reply_text(f"""У вас {len_order} заказов
Чтобы Просмотреть их введите команду /list""")


def list_orders(update: Update, context: CallbackContext):
    orders = Order.objects.all()
    for order in orders:
        user_order = f"""Новый заказ:
Имя:{order.name} Тел: {order.phone} Адрес: {order.address}
Заказ:
"""
        products = order.products.all()
        for product in products:
            user_order += f"{product.name} количество: {product.balance}\n"
        update.message.reply_text(user_order)


class Command(BaseCommand):
    help = "tg bot"

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1.0, )
        bot = Bot(request=request, token=TELEGRAM_BOT_API_KEY)
        print(bot.get_me())

        updater = Updater(bot=bot, use_context=True,)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("list", list_orders))
        updater.start_polling()
        updater.idle()
