from os import path

from pyflow import PPARunner
from platforms.sky130hd.config import SKY130HD_PLATFORM_CONFIG

gcd_runner = PPARunner(
	design_name="gcd",
	global_flow_config={
		**SKY130HD_PLATFORM_CONFIG,
		'PLATFORM': 'sky130hd',
		'VERILOG_FILES': [path.join('designs', 'src', 'gcd', 'gcd.v')],
		'DESIGN_DIR': path.join('designs', 'sky130hd', 'gcd'),
		'YOSYS_CMD': '/usr/bin/miniconda3/bin/yosys',
		'OPENROAD_CMD': '/usr/bin/miniconda3/bin/openroad',
		'KLAYOUT_CMD': 'klayout',
		'CORE_UTILIZATION': 40
	},
	modules=[
		{
			'name': 'GcdUnitCtrlRTL_0x4d0fc71ead8d3d9e',
			'flow_config': {
				'CORE_UTILIZATION': {
					'start': 10,
					'end': 100,
					'step': 10
				}
			},
			'parameters': {
				'header_type': ['A', 'B'],
				'array_size': [10, 20, 30],
				'temp': {'start': 1, 'end': 50, 'step': 2}
			}
		},
		{
			'name': 'RegRst_0x9f365fdf6c8998a',
			'flow_config': {},
			'parameters': {}
		}
	]
)

gcd_runner.run_ppa_analysis()
gcd_runner.print_stats()