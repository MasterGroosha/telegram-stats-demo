from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Тестовая команда №1"),
        BotCommand(command="help", description="Тестовая команда №2"),
        BotCommand(command="button", description="Тестовая команда №3"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
