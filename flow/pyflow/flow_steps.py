from os import makedirs, path
import re

from .call_tool import call_yosys_script, call_util_script
from .config import FlowConfig

def preprocess(config: FlowConfig):
	# Mark libraries as dont use
	makedirs(path.join(config.get('OBJECTS_DIR'), 'lib'), exist_ok = True)
	dont_use_libs = []

	for libfile in config.get('LIB_FILES'):
		output_file = path.join(config.get('OBJECTS_DIR'), 'lib', path.basename(libfile))
		call_util_script(
			'markDontUse.py',
			config,
			[
				'-p', ' '.join(config.get('DONT_USE_CELLS')),
				'-i', libfile,
				'-o', output_file
			]
		)

		dont_use_libs.append(output_file)

	config.set('DONT_USE_LIBS', dont_use_libs)
	config.set('DONT_USE_SC_LIB', config.get('DONT_USE_LIBS'))

	# Set yosys-abc clock period to first "clk_period" value or "-period" value found in sdc file
	with open(config.get('SDC_FILE')) as sdc_file:
		# Match for set clk_period or -period statements
		clk_period_matches = re.search(pattern="^set\s+clk_period\s+(\S+).*|.*-period\s+(\S+).*", flags=re.MULTILINE, string=sdc_file.read())

		if len(clk_period_matches.groups()) > 0:
			config.set('ABC_CLOCK_PERIOD_IN_PS', float(clk_period_matches.group(1)))

	return config

def synth(config: FlowConfig):
	makedirs(config.get('RESULTS_DIR'), exist_ok = True)
	makedirs(config.get('REPORTS_DIR'), exist_ok = True)
	makedirs(config.get('LOG_DIR'), exist_ok = True)

	call_yosys_script(
		'synth',
		logfile='test.log',
		args=[],
		config=config
	)