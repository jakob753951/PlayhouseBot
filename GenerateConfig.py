import json

def generate_all(file_name: str):
	with open(file_name) as cfg_file:
		fields = json.loads(cfg_file.read())
		general = fields['general']
		server = fields['server']

	generate_general_cfg(general, server)
	generate_server_cfg(general, server)

def generate_general_cfg(general, server):
	with open('Configuration.py', 'w') as cfg_file:
		cfg_file.write(f"""\
import json
from ServerCfg import ServerCfg

class Configuration:
\tdef __init__(self, {', '.join([f"{field} = '{'.' if field == 'prefix' else ''}'" for field in general])}""")
		cfg_file.write(", servers = {}):\n")


		for field in general:
			cfg_file.write(f'\t\tself.{field} = {field}\n')

		cfg_file.write('\t\tself.servers = {}\n')

		cfg_file.write(f"""\t\tfor key, value in servers.items():
			fields = [{", ".join(["'" + f + "'" for f in server])}]
			args = [value[field] for field in fields]
			srv = ServerCfg(*args)
			self.servers[int(key)] = srv
""")

		sep = ',\n\t\t'
		cfg_file.write(f"""
def load_config(filename):
	with open(filename) as cfg_file:
		jsonfile = json.loads(cfg_file.read())

	args = (
		{sep.join([f"jsonfile['{field}']" for field in general])},
		jsonfile['servers']
	)

	conf = Configuration(*args)
	return conf
""")

def generate_server_cfg(general, server):
	sep = '\n\t\t'
	with open('ServerCfg.py', 'w') as cfg_file:
		cfg_file.write(f"""\
class ServerCfg:
	def __init__(self, {', '.join([f for f in server])}):
		{sep.join([f"self.{f} = {f}" for f in server])}
""")


if __name__ == '__main__':
    generate_all('fields.json')