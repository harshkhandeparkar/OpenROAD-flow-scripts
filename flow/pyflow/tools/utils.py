from os import path
from pyflow.flow_config import FlowConfig
from . import __call_tool

def call_util_script(script: str, config: FlowConfig, args: list[str]):
	__call_tool(
		path.join(config.get('UTILS_DIR'), script),
		args,
		config.get_env(),
		None
	)