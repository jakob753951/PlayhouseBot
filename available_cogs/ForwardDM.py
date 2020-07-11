import discord
from discord.ext import commands
from Configuration import Configuration, load_config

class ForwardDM(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cfg = load_config('config.json')

	@commands.Cog.listener()
	async def on_message(self, message):
		# Make sure it's a user sending a message in a DM to the bot
		if message.author.bot or message.guild:
			return
		
		forward_channel = await self.get_forward_channel()
		await forward_channel.send(f'{message.author.name}: "{message.content}"')
		if message.attachments:
			await forward_channel.send(f'with the following attachment{"s" if len(message.attachments) > 1 else ""}:')
			await forward_channel.send('\n'.join([att.url for att in message.attachments]))

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		# Make sure it's a user editing a message in a DM with the bot
		if after.author.bot or after.guild:
			return
		
		forward_channel = await self.get_forward_channel()
		await forward_channel.send(f'{after.author.name} edited their message: "{before.content}" --> "{after.content}"')

	async def get_forward_channel(self):
		return await self.bot.fetch_channel(self.cfg.chan_forward_dm)

	@commands.command(name='send_dm')
	async def send_dm(self, ctx, recipient: discord.User, *, message):
		await recipient.send(message)



def setup(bot):
	bot.add_cog(ForwardDM(bot))