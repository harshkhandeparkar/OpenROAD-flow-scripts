from typing import TypedDict, Union

class __DesignCommonConfig(TypedDict):
	"""The common design configuration."""
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

class __DesignSynthConfig(TypedDict):
	"""The synthesis design configuration."""

class __DesignFloorplanConfig(TypedDict):
	"""The floorplan design configuration."""

_FlowDesignConfig = Union[__DesignCommonConfig, __DesignSynthConfig, __DesignFloorplanConfig]