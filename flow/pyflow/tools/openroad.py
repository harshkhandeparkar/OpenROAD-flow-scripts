from os import path
from . import __call_tool

def _call_openroad(args: list[str], logfile: str, openroad_cmd: str, env: dict[str, str]):
	__call_tool(
		tool=openroad_cmd,
		args=['-exit', '-no_init', *args],
		env=env,
		logfile=logfile
	)

def do_openroad_step(
	name: str,
	script: str,
	scripts_dir: str,
	log_dir: str,
	openroad_cmd: str,
	env: dict[str, str]
):
	script_path = path.join(scripts_dir, f'{script}.tcl')
	metricsfile_path = path.join(log_dir, f'{name}.json')
	logfile_path = path.join(log_dir, f'{name}.log')

	_call_openroad([script_path, "-metrics", metricsfile_path], logfile_path, openroad_cmd, env)
