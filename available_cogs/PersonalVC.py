import discord
from discord.ext import commands
from Configuration import *

class PersonalVC(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.cfg = load_config('config.json')
		self.user_vc = {}

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		#if the left channel was a personal VC
		if before.channel and before.channel.id in self.user_vc:
			#and it is now empty
			if len(before.channel.members) == 0:
				#delete the channels and roles
				for chan in self.user_vc[before.channel.id]:
					await chan.delete()
				await before.channel.delete()
				#remove from dict
				self.user_vc.pop(before.channel.id)

		if not after.channel:
			return
		if after.channel != await self.bot.fetch_channel(self.cfg.servers[member.guild.id].chan_personal_vc):
			return

		#shorthand for later use
		server = member.guild
		username = member.display_name

		#create role and add it to the user
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

		#get cate_personal_vc for the server
		cat = await self.bot.fetch_channel(self.cfg.servers[member.guild.id].cate_personal_vc)

		channel_name = f"{username}'s channel"
		vc = await cat.create_voice_channel(channel_name, overwrites = overwrites)
		await member.move_to(vc)

		tc = await cat.create_text_channel(channel_name, overwrites = overwrites)
		#add the vc as a key to user_vc, while setting the value to a tuple with tc and role
		self.user_vc[vc.id] = (tc, role)



def setup(bot):
	bot.add_cog(PersonalVC(bot))