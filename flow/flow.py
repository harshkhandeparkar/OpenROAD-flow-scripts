from os import path

from pyflow.config.config import FlowConfig
from pyflow.flow_steps import preprocess, synth, floorplan
from platforms.sky130hd.config import SKY130HD_PLATFORM_CONFIG

gcd_config = FlowConfig({
	'DESIGN_NAME': 'gcd',
	'PLATFORM': 'sky130hd',
	**SKY130HD_PLATFORM_CONFIG,
	'VERILOG_FILES': [path.join('designs', 'src', 'gcd', 'gcd.v')],
	'YOSYS_CMD': '/usr/bin/miniconda3/bin/yosys',
	'OPENROAD_CMD': '/usr/bin/miniconda3/bin/openroad',
	'KLAYOUT_CMD': 'klayout',
	# 'PRESERVE_CELLS': ['gcd', 'GcdUnitDpathRTL_0x4d0fc71ead8d3d9e', 'GcdUnitCtrlRTL_0x4d0fc71ead8d3d9e'],
	'CORE_UTILIZATION': 40
})

gcd_config = preprocess(gcd_config)
synth(gcd_config)
floorplan(gcd_config)