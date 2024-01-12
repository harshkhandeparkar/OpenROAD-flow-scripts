from typing import TypedDict, Union, Optional
from os import path

class __FlowConfigDirectories(TypedDict):
	"""The flow directories."""
	FLOW_HOME: str
	"""The home directory for the flow scripts. Default: `.`"""
	DESIGN_HOME: str
	"""The directory in which all design files are stored. Default: `[flow_home]/designs/`"""
	DESIGN_DIR: str
	"""The directory in which the design files for the used design are stored. Default: `[design_home]/[platform]/[design_name]/"""
	UTILS_DIR: str
	"""The directory in which util functions are stored. Default: `[flow_home]/util/`"""
	SCRIPTS_DIR: str
	"""The directory in which the scripts are stored. Default: `[flow_home]/scripts/`"""
	PLATFORM_HOME: str
	"""The directory in which all platform configurations are stored. Default: `[flow_home]/platforms/`"""
	PLATFORM_DIR: str
	"""The directory in which the configuration for the used platform configurations are stored. Default: `[platform_home]/[platform]`"""
	RESULTS_DIR: str
	"""The directory in which all flow results will be generated. Default: `[flow_home]/results/[platform]/[design_name]/`"""
	LOG_DIR: str
	"""The directory in which all log files will be generated. Default: `[flow_home]/logs/[platform]/[design_name]/`"""
	REPORTS_DIR: str
	"""The directory in which all reports will be generated. Default: `[flow_home]/reports/[platform]/[design_name]/`"""
	OBJECTS_DIR: str
	"""The directory in which all objects will be generated. Default: `[flow_home]/objects/[platform]/[design_name]/`"""

class __FlowConfigTools(TypedDict):
	"""The tool configurations."""
	# TOOL COMMANDS
	YOSYS_CMD: str
	"""Path to the the Yosys executable. Default: `/usr/bin/yosys`"""
	OPENROAD_EXE: str
	"""Path to the OpenROAD executable. Default: `/usr/bin/openroad`"""
	KLAYOUT_CMD: str
	"""Path to the Klayout executable. Default: `/usr/bin/klayout`"""

	# SYNTHESIS CONFIG
	SYNTH_ARGS: str
	SYNTH_HIERARCHICAL: str
	"""Optional synthesis variables for Yosys."""

FlowCommonConfigDict = Union[__FlowConfigDirectories, __FlowConfigTools]

FLOW_COMMON_CONFIG_DEFAULTS: FlowCommonConfigDict = {
	'FLOW_HOME': path.abspath('.'),
	'YOSYS_CMD': '/usr/bin/yosys',
	'OPENROAD_EXE': '/usr/bin/openroad',
	'KLAYOUT_CMD': '/usr/bin/klayout',
	'SYNTH_ARGS': '-flatten'
}

class FlowCommonConfig:
	config: FlowCommonConfigDict

	def __init__(self, configopts: Union[FlowCommonConfigDict, dict]):
		self.config = {**FLOW_COMMON_CONFIG_DEFAULTS, **configopts}

		# Set defaults for directories (interdependent)
		self.config['DESIGN_HOME'] = self.config.get('DESIGN_HOME', path.join(self.config['FLOW_HOME'], 'designs'))
		self.config['DESIGN_DIR'] = self.config.get('DESIGN_DIR', path.join(self.config['DESIGN_HOME'], self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['UTILS_DIR'] = self.config.get('UTILS_DIR', path.join(self.config['FLOW_HOME'], 'util'))
		self.config['SCRIPTS_DIR'] = self.config.get('SCRIPTS_DIR', path.join(self.config['FLOW_HOME'], 'scripts'))
		self.config['PLATFORM_HOME'] = self.config.get('PLATFORM_HOME', path.join(self.config['FLOW_HOME'], 'platforms'))
		self.config['PLATFORM_DIR'] = self.config.get('PLATFORM_DIR', path.join(self.config['PLATFORM_HOME'], self.config['PLATFORM']))
		self.config['RESULTS_DIR'] = self.config.get('RESULTS_DIR', path.join(self.config['FLOW_HOME'], 'results', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['LOG_DIR'] = self.config.get('LOG_DIR', path.join(self.config['FLOW_HOME'], 'logs', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['REPORTS_DIR'] = self.config.get('REPORTS_DIR', path.join(self.config['FLOW_HOME'], 'reports', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['OBJECTS_DIR'] = self.config.get('OBJECTS_DIR', path.join(self.config['FLOW_HOME'], 'objects', self.config['PLATFORM'], self.config['DESIGN_NAME']))

	def get_env(self, init_env: Optional[dict]):
		env = {**init_env} if init_env is not None else {**self.config}
