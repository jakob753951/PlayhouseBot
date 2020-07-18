import discord
from discord.ext import commands
from Configuration import Configuration, load_config

class Warning(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cfg = load_config('config.json')

	@commands.command(name='warn')
	async def warn(self, ctx, user: discord.User, *, reason = '[no reason given]'):
		await user.send(f"You have been warned in {ctx.guild.name} for the following reason:\n{reason}")
		member_log = await self.bot.fetch_channel(self.cfg.servers[ctx.guild.id].chan_member_log)
		await member_log.send(f"{user.name}(id: {user.id}) was warned for '{reason}'")


def setup(bot):
	bot.add_cog(Warning(bot))