from os import makedirs, path
from shutil import copyfile
import re

from .tools.yosys import call_yosys_script, parse_yosys_synth_stats
from .tools.utils import call_util_script
from .tools.openroad import do_openroad_step

from .flow_config import FlowConfig

def preprocess(config: FlowConfig):
	print("STARTING PREPROCESSING.")

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

	print("PREPROCESSING COMPLETED SUCCESFULLY.")

	return config

def synth(config: FlowConfig):
	print("STARTING SYNTHESIS.")

	makedirs(config.get('RESULTS_DIR'), exist_ok = True)
	makedirs(config.get('REPORTS_DIR'), exist_ok = True)
	makedirs(config.get('LOG_DIR'), exist_ok = True)

	SYNTH_OUTPUT_FILE = path.join(config.get('RESULTS_DIR'), '1_1_yosys.v')
	SYNTH_LOG_FILE = path.join(config.get('LOG_DIR'), '1_1_yosys.log')

	call_yosys_script(
		'synth',
		logfile=SYNTH_LOG_FILE,
		args=[],
		config=config
	)

	# Copy results
	copyfile(SYNTH_OUTPUT_FILE, path.join(config.get('RESULTS_DIR'), '1_synth.v'))
	copyfile(config.get('SDC_FILE'), path.join(config.get('RESULTS_DIR'), '1_synth.sdc'))

	print("SYNTHESIS COMPLETED SUCCESFULLY.")

	with open(path.join(config.get('REPORTS_DIR'), 'synth_stat.txt')) as statsfile:
		stats = parse_yosys_synth_stats(statsfile.read())

		return stats

def floorplan(config: FlowConfig):
	print("STARTING FLOORPLANNING.")

	makedirs(config.get('RESULTS_DIR'), exist_ok = True)
	makedirs(config.get('LOG_DIR'), exist_ok = True)

	# STEP 1: Translate verilog to odb
	do_openroad_step('2_1_floorplan', 'floorplan', config)
	# STEP 2: IO Placement (random)
	do_openroad_step('2_2_floorplan_io', 'io_placement_random', config)
	# STEP 3: Timing Driven Mixed Sized Placement
	do_openroad_step('2_3_floorplan_tdms', 'tdms_place', config)
	# STEP 4: Macro Placement
	do_openroad_step('2_4_floorplan_macro', 'macro_place', config)
	# STEP 5: Tapcell and Welltie insertion
	do_openroad_step('2_5_floorplan_tapcell', 'tapcell', config)
	# STEP 6: PDN generation
	do_openroad_step('2_6_floorplan_pdn', 'pdn', config)

	print("FLOORPLANNING COMPLETED SUCCESFULLY.")