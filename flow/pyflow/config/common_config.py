from typing import TypedDict, Union

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

FlowCommonConfig = Union[__FlowConfigDirectories, __FlowConfigTools]