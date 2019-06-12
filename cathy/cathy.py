"""
Cathy AI Discord Chat Bot

Written in Python 3 using AIML chat library.
"""
import asyncio
import os
import random

import discord
import pkg_resources
import requests
from discord.ext import commands
from slugify import slugify

import aiml

STARTUP_FILE = "std-startup.xml"
BOT_PREFIX = ('?', '!')


class ChattyCathy:
    """
    Class that contains all of the bot logic
    """

    def __init__(self, channel_name, bot_token):
        """
        Initialize the bot using the Discord token and channel name to chat in.

        :param channel_name: Only chats in this channel. No hashtag included.
        :param bot_token: Full secret bot token
        """
        self.channel_name = channel_name
        self.token = bot_token

        # Load AIML kernel
        self.aiml_kernel = aiml.Kernel()
        initial_dir = os.getcwd()
        os.chdir(pkg_resources.resource_filename(
            __name__, ''))  # Change directories to load AIML files properly
        startup_filename = pkg_resources.resource_filename(
            __name__, STARTUP_FILE)
        self.aiml_kernel.learn(startup_filename)
        self.aiml_kernel.respond("LOAD AIML B")
        os.chdir(initial_dir)

        # Set up Discord client
        self.discord_client = commands.Bot(command_prefix=BOT_PREFIX)
        self.setup()

    def get_translation(self, word):
        url = "https://dict.phundrak.fr/word/FRA/MTR/FRA-" + slugify(word)
        try:
            r = requests.head(url)
            if r.status_code != 404:
                return "It works o/"
        except requests.ConnectionError:
            return "Could not connect to the translation service."

    def setup(self):
        @self.discord_client.event
        @asyncio.coroutine
        def on_ready():
            print("Bot Online!")
            print("Name: {}".format(self.discord_client.user.name))
            print("ID: {}".format(self.discord_client.user.id))
            yield from self.discord_client.change_presence(game=discord.Game(
                name='Guiding you through Einlant'))

        @self.discord_client.event
        @asyncio.coroutine
        def on_message(message):
            if message.author.bot or str(message.channel) != self.channel_name:
                return

            if message.content is None:
                print("Empty message received.")
                return

            print("Message: " + str(message.content))

            if message.content.startswith(BOT_PREFIX):
                # Pass on to rest of the client commands
                yield from self.discord_client.process_commands(message)
            else:
                print("Getting answer")
                aiml_response = self.aiml_kernel.respond(message.content)
                print("Got answer: \"%s\"" % (aiml_response))
                yield from self.discord_client.send_typing(message.channel)
                yield from asyncio.sleep(random.randint(1, 3))
                if aiml_response != "":
                    if aiml_response.startswith("TRANS"):
                        word = aiml_response.split()[1]
                        trans = self.get_translation(word)
                        yield from self.discord_client.send_message(
                            message.channel, "translation: " + trans)
                    else:
                        yield from self.discord_client.send_message(
                            message.channel, aiml_response)
                else:
                    yield from self.discord_client.send_message(
                        message.channel, "Sorry, I do not understand.")

    def run(self):
        self.discord_client.run(self.token)
