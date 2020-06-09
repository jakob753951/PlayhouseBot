import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from Configuration import *
from ServerCfg import *
import GenerateConfig

GenerateConfig.generate_all('fields.json')

cfg = load_config('config.json')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(cfg.prefix), description=cfg.description, pm_help=True)

if __name__ == '__main__':
    for extension in cfg.initial_cogs:
        bot.load_extension(f'cogs.{extension}')

user_vc = {}

def log(message):
	print(f'{str(datetime.now())[:-7]}: {message}', flush=True)

async def get_msglog_channel(message: discord.Message):
	channel_id = cfg.servers[message.guild.id].chan_message_log
	channel = await bot.fetch_channel(channel_id)
	return channel

async def get_membrlog_channel(message: discord.Message):
	channel_id = cfg.servers[message.guild.id].chan_member_log
	channel = await bot.fetch_channel(channel_id)
	return channel

@bot.event
async def on_ready():
	log('Connected!')
	log(f'Username: {bot.user.name}')
	log(f'ID: {bot.user.id}')

@bot.event
async def on_message(message):
	if not message.author.bot and message.guild and message.guild.id in cfg.servers:
		log_channel = await get_msglog_channel(message)
		sender = message.author
		msg_channel = message.channel
		await log_channel.send(f'"{sender.name}#{sender.discriminator}" ({sender.id}) sent a message in {msg_channel.mention}: "{message.content}"')

	await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
	if not after.author.bot and after.guild:
		log_channel = await get_msglog_channel(after)
		sender = after.author
		msg_channel = after.channel

		male = discord.utils.find(lambda r: r.name == 'Male', after.guild.roles)
		female = discord.utils.find(lambda r: r.name == 'Female', after.guild.roles)
		if male in sender.roles:
			pronoun = 'his'
		elif female in sender.roles:
			pronoun = 'her'
		else:
			pronoun = 'their'

		await log_channel.send(f'"{sender.name}#{sender.discriminator}" ({sender.id}) edited {pronoun} message in {msg_channel.mention}: "{before.content}" --> "{after.content}"')

@bot.event
async def on_message_delete(message):
	if not message.author.bot and message.guild:
		log_channel = await get_msglog_channel(message)
		sender = message.author
		msg_channel = message.channel
		await log_channel.send(f'Message was deleted in {msg_channel.mention}: "{sender.name}#{sender.discriminator}: {message.content}"')

@bot.event
async def on_member_ban(guild, user):
	log_channel = get_membrlog_channel(guild.id)
	await log_channel.send(f'User was banned:\n"Username: "{user.name}#{user.discriminator}"\n{"/Nickname: " + user.nick if user.nick else ""}\nID: {user.id}')


bot.run(cfg.token)