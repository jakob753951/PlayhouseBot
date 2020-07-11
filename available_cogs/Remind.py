import discord
from discord.ext import tasks, commands
from Configuration import Configuration, load_config
import asyncio

class Remind(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.cfg = load_config('config.json')
		self.remind_bump.start()

	def cog_unload(self):
		self.remind_bump.cancel()

	@tasks.loop(hours=2)
	async def remind_bump(self):
		await asyncio.sleep(10)
		chan = await self.bot.fetch_channel(self.cfg.chan_remind)
		guild = await self.bot.fetch_guild(self.cfg.guild_remind)
		role = guild.get_role(self.cfg.role_remind)
		await chan.send(f'{role.mention} Time to bump!\n`!d bump`')


def setup(bot):
	bot.add_cog(Remind(bot))