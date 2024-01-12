import subprocess
from os import path
from .flow_config import FlowConfig

def _call_tool(tool: str, args: list[str], env: dict | None, logfile: str | None):
	for key in env:
		if type(env[key]) != str:
			print(key, env[key])

	if logfile:
		with open(logfile, 'w') as f:
			subprocess.run([tool, *args], env=env, stdout=f, stderr=f)
	else:
		subprocess.run([tool, *args], env=env)

def _call_yosys(args: list[str], logfile: str, config: FlowConfig):
	_call_tool(
		tool=config.get('YOSYS_CMD'),
		args=['-v', '3', *args],
		env=config.get_env(),
		logfile=logfile
	)

def call_yosys_script(script: str, args: list[str], logfile: str, config: FlowConfig):
	_call_yosys(["-c", path.join(config.get('SCRIPTS_DIR'), f'{script}.tcl'), *args], logfile, config=config)

def call_util_script(script: str, config: FlowConfig, args: list[str]):
	_call_tool(
		path.join(config.get('UTILS_DIR'), script),
		args,
		config.get_env(),
		None
	)

def _call_openroad(args: list[str], logfile: str, config: FlowConfig):
	_call_tool(
		tool=config.get('OPENROAD_CMD'),
		args=['-exit', '-no_init', *args],
		env=config.get_env(),
		logfile=logfile
	)

def do_openroad_step(name: str, script: str, config: FlowConfig):
	script_path = path.join(config.get('SCRIPTS_DIR'), f'{script}.tcl')
	metricsfile_path = path.join(config.get('LOG_DIR'), f'{name}.json')
	logfile_path = path.join(config.get('LOG_DIR'), f'{name}.log')

	_call_openroad([script_path, "-metrics", metricsfile_path], logfile_path, config)
