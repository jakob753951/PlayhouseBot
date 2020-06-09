import json
from ServerCfg import ServerCfg

class Configuration:
	def __init__(self, token = '', prefix = '.', description = '', name = '', initial_cogs = '', servers = {}):
		self.token = token
		self.prefix = prefix
		self.description = description
		self.name = name
		self.initial_cogs = initial_cogs
		self.servers = {}
		for key, value in servers.items():
			fields = ['cate_personal_vc', 'chan_personal_vc', 'chan_message_log', 'chan_member_log']
			args = [value[field] for field in fields]
			srv = ServerCfg(*args)
			self.servers[int(key)] = srv

def load_config(filename):
	with open(filename) as cfg_file:
		jsonfile = json.loads(cfg_file.read())

	args = (
		jsonfile['token'],
		jsonfile['prefix'],
		jsonfile['description'],
		jsonfile['name'],
		jsonfile['initial_cogs'],
		jsonfile['servers']
	)

	conf = Configuration(*args)
	return conf
