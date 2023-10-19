from os import path

from flow.pyflow.config import FlowConfig
from pyflow.flow_steps import preprocess, synth

gcd_config = FlowConfig({
	'DESIGN_NAME': 'gcd',
	'PLATFORM': 'sky130hd',
	'VERILOG_FILES': [path.join('designs', 'src', 'gcd', 'gcd.v')],
	'YOSYS_CMD': '/usr/bin/miniconda3/bin/yosys',
	'OPENROAD_CMD': 'openroad',
	'KLAYOUT_CMD': 'klayout',
	'PROCESS': 130,
	'TECH_LEF': path.join('platforms', 'sky130hd', 'lef', 'sky130_fd_sc_hd.tlef'),
	'SC_LEF': path.join('platforms', 'sky130hd', 'lef', 'sky130_fd_sc_hd_merged.lef'),
	'LIB_FILES': [path.join('platforms', 'sky130hd', 'lib', 'sky130_fd_sc_hd__tt_025C_1v80.lib')],
	'GDS_FILES': [path.join('platforms', 'sky130hd', 'gds', 'sky130_fd_sc_hd.gds')],
	'DONT_USE_CELLS': ['sky130_fd_sc_hd__probe_p_8', 'sky130_fd_sc_hd__probec_p_8', 'sky130_fd_sc_hd__lpflow_bleeder_1', 'sky130_fd_sc_hd__lpflow_clkbufkapwr_1', 'sky130_fd_sc_hd__lpflow_clkbufkapwr_16', 'sky130_fd_sc_hd__lpflow_clkbufkapwr_2', 'sky130_fd_sc_hd__lpflow_clkbufkapwr_4', 'sky130_fd_sc_hd__lpflow_clkbufkapwr_8', 'sky130_fd_sc_hd__lpflow_clkinvkapwr_1', 'sky130_fd_sc_hd__lpflow_clkinvkapwr_16', 'sky130_fd_sc_hd__lpflow_clkinvkapwr_2', 'sky130_fd_sc_hd__lpflow_clkinvkapwr_4', 'sky130_fd_sc_hd__lpflow_clkinvkapwr_8', 'sky130_fd_sc_hd__lpflow_decapkapwr_12', 'sky130_fd_sc_hd__lpflow_decapkapwr_3', 'sky130_fd_sc_hd__lpflow_decapkapwr_4', 'sky130_fd_sc_hd__lpflow_decapkapwr_6', 'sky130_fd_sc_hd__lpflow_decapkapwr_8', 'sky130_fd_sc_hd__lpflow_inputiso0n_1', 'sky130_fd_sc_hd__lpflow_inputiso0p_1', 'sky130_fd_sc_hd__lpflow_inputiso1n_1', 'sky130_fd_sc_hd__lpflow_inputiso1p_1', 'sky130_fd_sc_hd__lpflow_inputisolatch_1', 'sky130_fd_sc_hd__lpflow_isobufsrc_1', 'sky130_fd_sc_hd__lpflow_isobufsrc_16', 'sky130_fd_sc_hd__lpflow_isobufsrc_2', 'sky130_fd_sc_hd__lpflow_isobufsrc_4', 'sky130_fd_sc_hd__lpflow_isobufsrc_8', 'sky130_fd_sc_hd__lpflow_isobufsrckapwr_16', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_1', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_2', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_4', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_4', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_1', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_2', 'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4'],
	'FILL_CELLS': ['sky130_fd_sc_hd__fill_1 sky130_fd_sc_hd__fill_2', 'sky130_fd_sc_hd__fill_4', 'sky130_fd_sc_hd__fill_8'],
	'LATCH_MAP_FILE': path.join('platforms', 'sky130hd', 'cells_latch_hd.v'),
	'ADDER_MAP_FILE': '',
	'CLKGATE_MAP_FILE': path.join('platforms', 'sky130hd', 'cells_clkgate_hd.v'),
	'TAPCELL_TCL': path.join('platforms', 'sky130hd', 'tapcell.tcl'),
	'CDL_FILE': path.join('platforms', 'sky130hd', 'cdl', 'sky130hd.cdl'),
	'KLAYOUT_LVS_FILE': path.join('platforms', 'sky130hd', 'lvs', 'sky130hd.lylvs'),
	'ABC_DRIVER_CELL': 'sky130_fd_sc_hd__buf_1',
	'ABC_LOAD_IN_FF': 5,
	'TIEHI_CELL_AND_PORT': ('sky130_fd_sc_hd__conb_1', 'HI'),
	'TIELO_CELL_AND_PORT': ('sky130_fd_sc_hd__conb_1', 'LO'),
	'MIN_BUF_CELL_AND_PORTS': ('sky130_fd_sc_hd__buf_4', 'A', 'X')
})

gcd_config = preprocess(gcd_config)
synth(gcd_config)