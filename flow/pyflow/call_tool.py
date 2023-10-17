import subprocess
from os import path
from .config.config import FlowConfig

def _call_tool(tool: str, args: list[str], env: dict | None):
	subprocess.run([tool, *args], env=env)

def _call_yosys(args: list[str], logfile: str, config: FlowConfig):
	print(config.get_env())
	_call_tool(
		config.get('YOSYS_CMD'),
		['-v', '3', *args],
		config.get_env()
	)

def call_yosys_script(script: str, args: list[str], logfile: str, config: FlowConfig):
	_call_yosys(["-c", path.join(config.get('SCRIPTS_DIR'), f'{script}.tcl'), *args], logfile, config=config)

def call_util_script(script: str, config: FlowConfig, args: list[str]):
	_call_tool(
		path.join(config.get('UTILS_DIR'), script),
		args,
		config.get_env()
	)