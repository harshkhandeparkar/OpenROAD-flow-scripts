from os import path

from pyflow.flow_config import FlowConfig
from pyflow.flow_runner import FlowRunner
from pyflow.flow_steps import preprocess, synth, floorplan
from platforms.sky130hd.config import SKY130HD_PLATFORM_CONFIG

gcd_runner = FlowRunner(
	{
		'DESIGN_NAME': 'gcd',
		'PLATFORM': 'sky130hd',
		**SKY130HD_PLATFORM_CONFIG,
		'VERILOG_FILES': [path.join('designs', 'src', 'gcd', 'gcd.v')],
		'YOSYS_CMD': '/usr/bin/miniconda3/bin/yosys',
		'OPENROAD_CMD': '/usr/bin/miniconda3/bin/openroad',
		'KLAYOUT_CMD': 'klayout',
		'PRESERVE_CELLS': ['gcd', 'GcdUnitDpathRTL_0x4d0fc71ead8d3d9e', 'GcdUnitCtrlRTL_0x4d0fc71ead8d3d9e'],
		'CORE_UTILIZATION': 40
	},
	[]
)

gcd_runner.run_flow()