from os import path

from pyflow.flow_runner import FlowRunner
from platforms.sky130hd.config import SKY130HD_PLATFORM_CONFIG

gcd_runner = FlowRunner(
	global_flow_config={
		**SKY130HD_PLATFORM_CONFIG,
		'DESIGN_NAME': 'gcd',
		'PLATFORM': 'sky130hd',
		'VERILOG_FILES': [path.join('designs', 'src', 'gcd', 'gcd.v')],
		'YOSYS_CMD': '/usr/bin/miniconda3/bin/yosys',
		'OPENROAD_CMD': '/usr/bin/miniconda3/bin/openroad',
		'KLAYOUT_CMD': 'klayout',
		'CORE_UTILIZATION': 40
	},
	modules=[
		{
			'name': 'gcd',
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
		}
	]
)

gcd_runner.run_flow()