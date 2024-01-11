from typing import Union
from os import path

from .platform_config import FlowPlatformConfig
from .design_config import FlowDesignConfig
from .common_config import FlowCommonConfig

_FlowConfigDict = Union[FlowCommonConfig, FlowPlatformConfig, FlowDesignConfig]

class FlowConfig():
	config: _FlowConfigDict

	def __init__(self, configopts: Union[_FlowConfigDict, dict]):
		# Set defaults for independent variables
		self.config = {
			**configopts,
			# Directories
			'FLOW_HOME': path.abspath(configopts.get('FLOW_HOME', '.')),

			# Tool commands
			'YOSYS_CMD': configopts.get('YOSYS_CMD', '/usr/bin/yosys'),
			'OPENROAD_EXE': configopts.get('OPENROAD_EXE', '/usr/bin/openroad'),
			'KLAYOUT_CMD': configopts.get('KLAYOUT_CMD', '/usr/bin/klayout'),

			# Platform config
			'ABC_AREA': configopts.get('ABC_AREA', False),
			'ABC_CLOCK_PERIOD_IN_PS': configopts.get('ABC_CLOCK_PERIOD_IN_PS', 0),
			'DONT_USE_CELLS': configopts.get('DONT_USE_CELLS', []),
			'DONT_USE_LIBS': configopts.get('DONT_USE_LIBS', []),
			'DONT_USE_SC_LIB': configopts.get('DONT_USE_SC_LIB', []),
			'FILL_CELLS': configopts.get('FILL_CELLS', []),

			# Synthesis config
			'SYNTH_ARGS': configopts.get('SYNTH_ARGS', '-flatten'),
			'PRESERVE_CELLS': configopts.get('PRESERVE_CELLS', []),

			# Floorplan config
			'DIE_AREA': configopts.get('DIE_AREA', []),
			'CORE_AREA': configopts.get('CORE_AREA', []),
			'CORE_ASPECT_RATIO': configopts.get('CORE_ASPECT_RATIO', 0),
			'CORE_MARGIN': configopts.get('CORE_MARGIN', 0),
		}

		# Set defaults for directories (interdependent)
		self.config['DESIGN_HOME'] = configopts.get('DESIGN_HOME', path.join(self.config['FLOW_HOME'], 'designs'))
		self.config['DESIGN_DIR'] = configopts.get('DESIGN_DIR', path.join(self.config['DESIGN_HOME'], self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['UTILS_DIR'] = configopts.get('UTILS_DIR', path.join(self.config['FLOW_HOME'], 'util'))
		self.config['SCRIPTS_DIR'] = configopts.get('SCRIPTS_DIR', path.join(self.config['FLOW_HOME'], 'scripts'))
		self.config['PLATFORM_HOME'] = configopts.get('PLATFORM_HOME', path.join(self.config['FLOW_HOME'], 'platforms'))
		self.config['PLATFORM_DIR'] = configopts.get('PLATFORM_DIR', path.join(self.config['PLATFORM_HOME'], self.config['PLATFORM']))
		self.config['RESULTS_DIR'] = configopts.get('RESULTS_DIR', path.join(self.config['FLOW_HOME'], 'results', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['LOG_DIR'] = configopts.get('LOG_DIR', path.join(self.config['FLOW_HOME'], 'logs', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['REPORTS_DIR'] = configopts.get('REPORTS_DIR', path.join(self.config['FLOW_HOME'], 'reports', self.config['PLATFORM'], self.config['DESIGN_NAME']))
		self.config['OBJECTS_DIR'] = configopts.get('OBJECTS_DIR', path.join(self.config['FLOW_HOME'], 'objects', self.config['PLATFORM'], self.config['DESIGN_NAME']))

		# Set platform config default file paths (depend on directories)
		self.config['PDN_TCL'] = configopts.get('PDN_TCL', path.join(self.config['PLATFORM_DIR'], 'pdn.tcl'))
		self.config['TAPCELL_TCL'] = configopts.get('TAPCELL_TCL', path.join(self.config['PLATFORM_DIR'], 'tapcell.tcl'))

		# Set design config file paths (depend on directories)
		self.config['SDC_FILE'] = configopts.get('SDC_FILE', path.join(self.config['DESIGN_DIR'], 'constraint.sdc'))

	def get(self, key):
		return self.config[key]

	def set(self, key, value):
		self.config[key] = value

	def get_env(self):
		"""Returns the corresponding environment variables for the given configuration."""

		# Import default string variables
		env_vars = {**self.config}

		# Convert others to string
		env_vars['PROCESS'] = str(self.config['PROCESS'])
		env_vars['LIB_FILES'] = ' '.join(self.config['LIB_FILES'])
		env_vars['GDS_FILES'] = ' '.join(self.config['GDS_FILES'])
		env_vars['DONT_USE_CELLS'] = ' '.join(self.config['DONT_USE_CELLS'])
		env_vars['DONT_USE_LIBS'] = ' '.join(self.config['DONT_USE_LIBS'])
		env_vars['DONT_USE_SC_LIB'] = ' '.join(self.config['DONT_USE_SC_LIB'])
		env_vars['FILL_CELLS'] = ' '.join(self.config['FILL_CELLS'])

		env_vars['ABC_LOAD_IN_FF'] = str(self.config['ABC_LOAD_IN_FF'])
		env_vars['TIEHI_CELL_AND_PORT'] = ' '.join(self.config['TIEHI_CELL_AND_PORT'])
		env_vars['TIELO_CELL_AND_PORT'] = ' '.join(self.config['TIELO_CELL_AND_PORT'])
		env_vars['MIN_BUF_CELL_AND_PORTS'] = ' '.join(self.config['MIN_BUF_CELL_AND_PORTS'])
		env_vars['VERILOG_FILES'] = ' '.join(self.config['VERILOG_FILES'])
		env_vars['PRESERVE_CELLS'] = ' '.join(self.config['PRESERVE_CELLS'])
		env_vars['ABC_AREA'] = str(int(self.config['ABC_AREA']))
		env_vars['ABC_CLOCK_PERIOD_IN_PS'] = str(self.config['ABC_CLOCK_PERIOD_IN_PS'])
		env_vars['IO_PLACER_H'] = self.config['IO_PLACER_H']
		env_vars['IO_PLACER_V'] = self.config['IO_PLACER_V']
		env_vars['MACRO_PLACE_HALO'] = f"{self.config['MACRO_PLACE_HALO'][0]} {self.config['MACRO_PLACE_HALO'][1]}"
		env_vars['MACRO_PLACE_CHANNEL'] = f"{self.config['MACRO_PLACE_CHANNEL'][0]} {self.config['MACRO_PLACE_CHANNEL'][1]}"

		env_vars['DIE_AREA'] = ' '.join(self.config.get('DIE_AREA'))
		env_vars['CORE_AREA'] = ' '.join(self.config.get('CORE_AREA'))
		env_vars['CORE_UTILIZATION'] = str(self.config['CORE_UTILIZATION'])
		env_vars['CORE_ASPECT_RATIO'] = str(self.config['CORE_ASPECT_RATIO'])
		env_vars['CORE_MARGIN'] = str(self.config['CORE_MARGIN'])

		return env_vars
