from typing import TypedDict
from typing import Union
from os import path

class _FlowConfigDict(TypedDict):
	"""The flow configuration."""

	# DIRECTORIES
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

	# TOOL COMMANDS
	YOSYS_CMD: str
	"""Path to the the Yosys executable. Default: `/usr/bin/yosys`"""
	OPENROAD_EXE: str
	"""Path to the OpenROAD executable. Default: `/usr/bin/openroad`"""
	KLAYOUT_CMD: str
	"""Path to the Klayout executable. Default: `/usr/bin/klayout`"""

	# PLATFORM CONFIG
	PROCESS: int
	"""The process node."""
	TECH_LEF: str
	"""Path to a technology LEF file of the PDK that includes all relevant information regarding metal layers, vias, and spacing requirements."""
	SC_LEF: str
	"""Path to technology standard cell LEF."""
	LIB_FILES: list[str]
	"""Paths to Liberty files of the standard cell library with PVT characterization, input and output characteristics, timing and power definitions for each cell."""
	GDS_FILES: list[str]
	"""Paths to platform GDS files."""
	DONT_USE_CELLS: list[str]
	"""List of cells marked as dont use. Dont use cells eases pin access in detailed routing."""
	DONT_USE_LIBS: list[str]
	"""Liberty files marked as dont use."""
	DONT_USE_SC_LIB: list[str]
	"""Standard cell Liberty files marked as dont use."""
	FILL_CELLS: list[str]
	"""List of fill cells. Fill cells are used to fill empty sites."""
	CDL_FILE: str
	"""Path to the platform CDL file. """
	KLAYOUT_LVS_FILE: str
	"""Path to the platform LVS file used in Klayout."""

	### SYNTHESIS ###
	ABC_DRIVER_CELL: str
	"""Default driver cell used during ABC synthesis."""
	ABC_LOAD_IN_FF: float
	"""The `set_load` value used during synthesis."""
	TIEHI_CELL_AND_PORT: tuple[str, str]
	"""Tie high cells used in Yosys synthesis to replace a logical 1 in the Netlist."""
	TIELO_CELL_AND_PORT: tuple[str, str]
	"""Tie low cells used in Yosys synthesis to replace a logical 0 in the Netlist."""
	MIN_BUF_CELL_AND_PORTS: tuple[str, str, str]
	"""Used to insert a buffer cell to pass through wires. Used in synthesis."""
	LATCH_MAP_FILE: str
	"""The path to a Verilog file with a list of latches treated as a black box by Yosys."""
	CLKGATE_MAP_FILE: str
	"""The path to a Verilog file with a list of cells for gating clock treated as a black box by Yosys."""
	ADDER_MAP_FILE: str
	"""The path to a Verilog file with a list of adders treated as a black box by Yosys."""
	### /SYNTHESIS ###

	### FLOORPLAN ###
	PLACE_SITE: str
	"""Placement site for core cells. This can be found in the technology lef"""
	IO_PLACER_H: str
	"""IO Placer pin layers."""
	IO_PLACER_V: str
	"""IO Placer pin layers."""
	PDN_TCL: str
	"""File path which has a set of power grid policies used by `pdn` to be applied to the design, such as layers to use, stripe width and spacing to generate the actual metal straps. Default: `[platform_dir]/pdn.tcl`"""
	TAPCELL_TCL: str
	"""Path to Endcap and Welltie cells file. Default: `[platform_dir]/tapcell.tcl`"""
	MACRO_PLACE_HALO: tuple[float, float]
	MACRO_PLACE_CHANNEL: tuple[float, float]
	### /FLOORPLAN ###

	# DESIGN CONFIG
	DESIGN_NAME: str
	"""The name of the design."""
	PLATFORM: str
	"""The process design kit to be used."""
	VERILOG_FILES: list[str]
	"""The paths to the design Verilog files."""
	SDC_FILE: str
	"""The path to design constraint (SDC) file. Default: `[design_dir]/constraint.sdc"""
	ABC_AREA: bool
	"""Whether to use `ABC_AREA` strategy for Yosys synthesis. Setting it to false will use `ABC_SPEED` strategy. Default: `False`"""
	ABC_CLOCK_PERIOD_IN_PS: float
	"""Clock period to be used by STA during synthesis. Default value read from `constraint.sdc`."""

	# SYNTHESIS CONFIG
	SYNTH_ARGS: str
	"""Optional synthesis variables for Yosys."""

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
		env_vars['ABC_AREA'] = str(int(self.config['ABC_AREA']))
		env_vars['ABC_CLOCK_PERIOD_IN_PS'] = str(self.config['ABC_CLOCK_PERIOD_IN_PS'])
		env_vars['IO_PLACER_H'] = self.config['IO_PLACER_H']
		env_vars['IO_PLACER_V'] = self.config['IO_PLACER_V']
		env_vars['MACRO_PLACE_HALO'] = f"{self.config['MACRO_PLACE_HALO'][0]} {self.config['MACRO_PLACE_HALO'][1]}"
		env_vars['MACRO_PLACE_CHANNEL'] = f"{self.config['MACRO_PLACE_CHANNEL'][0]} {self.config['MACRO_PLACE_CHANNEL'][1]}"

		return env_vars
