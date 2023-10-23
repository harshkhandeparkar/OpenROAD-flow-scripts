from typing import TypedDict, Union

class __PlatformCommonConfig(TypedDict):
	"""The common platform configuration."""
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

class __PlatformSynthConfig(TypedDict):
	"""The synthesis platform configuration."""

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

class __PlatformFloorplanConfig(TypedDict):
	"""The floorplan platform configuration."""
	PLACE_SITE: str
	"""Placement site for core cells. This can be found in the technology lef"""
	IO_PLACER_H: str
	"""The metal layer on which to place the I/O pins horizontally (top and bottom of the die)."""
	IO_PLACER_V: str
	"""The metal layer on which to place the I/O pins vertically (sides of the die)."""
	PDN_TCL: str
	"""File path which has a set of power grid policies used by `pdn` to be applied to the design, such as layers to use, stripe width and spacing to generate the actual metal straps. Default: `[platform_dir]/pdn.tcl`"""
	TAPCELL_TCL: str
	"""Path to Endcap and Welltie cells file. Default: `[platform_dir]/tapcell.tcl`"""
	MACRO_PLACE_HALO: tuple[float, float]
	"""Horizontal/vertical halo around macros (microns). Used by automatic macro placement."""
	MACRO_PLACE_CHANNEL: tuple[float, float]
	"""Horizontal/vertical channel width between macros (microns). Used by automatic macro placement when `RTLMP_FLOW` is disabled."""

_FlowPlatformConfig = Union[__PlatformCommonConfig, __PlatformSynthConfig, __PlatformFloorplanConfig]