from os import path
from . import __call_tool
from pyflow.flow_config import FlowConfig

def _call_openroad(args: list[str], logfile: str, config: FlowConfig):
	__call_tool(
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
