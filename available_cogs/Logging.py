import discord
from discord.ext import commands
from Configuration import Configuration, load_config

class Logging(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cfg = load_config('config.json')

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if after.author.bot or not after.guild:
			return

		log_channel = await self.get_msglog_channel(after.guild)
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

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.author.bot or not message.guild:
			return

		log_channel = await self.get_msglog_channel(message.guild)
		sender = message.author
		msg_channel = message.channel

		await log_channel.send(f'Message was deleted in {msg_channel.mention}: "{sender.name}#{sender.discriminator}: {message.content}"')

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		log_channel = self.get_membrlog_channel(guild.id)
		await log_channel.send(f'User was banned:\n"Username: "{user.name}#{user.discriminator}"\n{"/Nickname: " + user.nick if user.nick else ""}\nID: {user.id}')


	async def get_msglog_channel(self, guild: discord.Guild):
		channel_id = self.cfg.servers[guild.guild.id].chan_message_log
		channel = await self.bot.fetch_channel(channel_id)
		return channel

	async def get_membrlog_channel(self, guild: discord.Guild):
		channel_id = self.cfg.servers[guild.id].chan_member_log
		channel = await self.bot.fetch_channel(channel_id)
		return channel



def setup(bot):
    bot.add_cog(Logging(bot))