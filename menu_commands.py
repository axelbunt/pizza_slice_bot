import json

import requests
from aiogram.types.bot_command import BotCommand

from constants import BOT_TOKEN


class BotCommandWithJSONSerializer(BotCommand):
    def __init__(self, command: str = None, description: str = None) -> None:
        super().__init__(command, description)

    def toJSON(self):
        return {"command": self.command, "description": self.description}


class HelpBotCommand(BotCommandWithJSONSerializer):
    def __init__(self) -> None:
        super().__init__()
        self.command = "help"
        self.description = "get description of bot commands"


class LocationBotCommand(BotCommandWithJSONSerializer):
    def __init__(self) -> None:
        super().__init__()
        self.command = "location"
        self.description = "get location of nearest pizzeria"


class HoursBotCommand(BotCommandWithJSONSerializer):
    def __init__(self) -> None:
        super().__init__()
        self.command = "hours"
        self.description = "get pizzeria working hours"


class MenuBotCommand(BotCommandWithJSONSerializer):
    def __init__(self) -> None:
        super().__init__()
        self.command = "menu"
        self.description = "get pizzeria menu"


COMMANDS = [
    HelpBotCommand(),
    LocationBotCommand(),
    HoursBotCommand(),
    MenuBotCommand(),
]


async def add_commands_to_bot_menu() -> requests.Response:
    url = (
        'https://api.telegram.org/bot' + BOT_TOKEN + '/SetMyCommands?commands='
    )
    url += json.dumps([command.toJSON() for command in COMMANDS])
    response = requests.get(url)
    return response
