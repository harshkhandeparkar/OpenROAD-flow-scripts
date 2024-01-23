from os import path
import re
from typing import TypedDict, Optional, Callable
from . import __call_tool

def __call_yosys(
	args: list[str],
	logfile: str,
	env: dict[str, str],
	yosys_cmd: str
):
	__call_tool(
		tool=yosys_cmd,
		args=['-v', '3', *args],
		env=env,
		logfile=logfile
	)

def call_yosys_script(
	script: str,
	args: list[str],
	logfile: str,
	scripts_dir: str,
	env: dict[str, str],
	yosys_cmd: str
):
	__call_yosys(["-c", path.join(scripts_dir, f'{script}.tcl'), *args], logfile, env, yosys_cmd)

class SynthStats(TypedDict):
	num_wires: int
	num_wire_bits: int
	num_public_wires: int
	num_memories: int
	num_memory_bits: int
	num_processes: int
	num_cells: int
	cell_counts: dict[str, int]
	module_area: float

def __find_yosys_synth_stats_value(stats_text: str, keyword: str, parser: Callable = int) -> Optional[str]:
	captures = re.findall(f"{keyword}\s*(\d+)", stats_text)
	if len(captures) > 0:
		try:
			return parser(captures[0])
		except:
			print(f'Error parsing the synthesis statistic: {keyword}')
			return None
	else:
		print(f'The synthesis statistic {keyword} not found.')
		return None

def parse_yosys_synth_stats(stats_text: str) -> SynthStats:
	stats: SynthStats = {}

	stats['num_wires'] = __find_yosys_synth_stats_value(stats_text, 'Number of wires:')
	stats['num_wire_bits'] = __find_yosys_synth_stats_value(stats_text, 'Number of wire bits:')
	stats['num_public_wires'] = __find_yosys_synth_stats_value(stats_text, 'Number of public wires:')
	stats['num_public_wire_bits'] = __find_yosys_synth_stats_value(stats_text, 'Number of public wire bits:')
	stats['num_memories'] = __find_yosys_synth_stats_value(stats_text, 'Number of memories:')
	stats['num_memory_bits'] = __find_yosys_synth_stats_value(stats_text, 'Number of memory bits:')
	stats['num_processes'] = __find_yosys_synth_stats_value(stats_text, 'Number of processes:')
	stats['num_cells'] = __find_yosys_synth_stats_value(stats_text, 'Number of cells:')

	# Finding module area
	for line in stats_text.splitlines():
		if line.lower().find("chip area for module ") != -1:
			stats['module_area'] = float(line.strip().split(':')[1].strip())

	# Finding module/cell wise chip area
	parse_cell_count = False
	stats['cell_counts'] = {}
	for line in stats_text.strip().splitlines():
		if parse_cell_count and (line.isspace() or len(line) == 0):
			parse_cell_count = False
			break
		elif parse_cell_count:
			parsed = line.strip().split()
			if len(parsed) > 1:
				stats['cell_counts'][parsed[0]] = int(parsed[1])
		elif line.lower().find("number of cells:") != -1:
			parse_cell_count = True

	return stats