import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from configuration import *
from server_cfg import *
import generate_config

generate_config.generate_all('fields.json')

cfg = load_config('config.json')

bot = commands.Bot(command_prefix=commands.when_mentioned_or(cfg.prefix), description=cfg.description, pm_help=True)

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

@bot.event
async def on_voice_state_update(member, before, after):
	#get owner of before.channel
	vc_owner = None
	for key, value in user_vc.items():
		if value[0] == before.channel:
			vc_owner = key
			break

	if vc_owner and len(before.channel.members) == 0:
		for chan in user_vc[vc_owner]:
			await chan.delete()
		user_vc.pop(vc_owner)

	if not after.channel:
		return

	if after.channel.guild.id not in cfg.servers:
		return

	guild_cfg = cfg.servers[after.channel.guild.id]

	if after.channel != await bot.fetch_channel(guild_cfg.chan_personal_vc):
		return

	server = after.channel.guild
	username = member.display_name
	role = await server.create_role(name=username)
	await member.add_roles(role)

	overwrites = {
		role: discord.PermissionOverwrite(
			manage_messages = True,
			manage_permissions = True,
			mute_members = True,
			deafen_members = True,
			manage_channels = True
		)
	}
	cat = await bot.fetch_channel(guild_cfg.cate_personal_vc)
	channel_name = f"{username}'s channel"
	vc = await cat.create_voice_channel(channel_name, overwrites = overwrites)
	await member.move_to(vc)

	tc = await cat.create_text_channel(channel_name, overwrites = overwrites)
	user_vc[member] = (vc, tc, role)

@bot.command(pass_ctx=True)
async def areyouonline(ctx):
	male = discord.utils.find(lambda r: r.name == 'Male', ctx.guild.roles)
	female = discord.utils.find(lambda r: r.name == 'Female', ctx.guild.roles)
	if male in ctx.author.roles:
		await ctx.send("Yea man.")
	elif female in ctx.author.roles:
		await ctx.send("Yea gurl.")
	else:
		await ctx.send("Yea.")

@bot.command(pass_ctx=True)
async def say(ctx, channel: discord.TextChannel, *, message):
	if len(ctx.message.embeds) > 0:
		await channel.send(message, embed=ctx.message.embeds[0], files=ctx.message.attachments)
	else:
		await channel.send(message, files=ctx.message.attachments)

bot.run(cfg.token)