from queue import Queue

from aiogram.dispatcher.router import Router
from aiogram.types import CallbackQuery
from magic_filter import F

from bot.analytics import NamedEventPre


async def cb_press_me(callback: CallbackQuery, objects_queue: Queue):
    """
    Хэндлер на нажатие кнопки с callback_data равной "press_me"

    :param callback: колбэк от Telegram
    :param objects_queue: очередь, из которой потом объекты улетают в InfluxDB
    """
    await callback.message.edit_text("Упс! Кнопка пропала!", reply_markup=None)
    await callback.answer()
    objects_queue.put(NamedEventPre(event="Нажатие кнопки 'нажми меня'"))


def register_callbacks(router: Router):
    router.callback_query.register(cb_press_me, F.data == "press_me")
