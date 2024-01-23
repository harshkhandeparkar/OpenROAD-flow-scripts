from typing import TypedDict, Union, Any, Optional
from os import path
from shutil import rmtree

from .flow import FlowRunner, FlowConfigDict
from .tools.yosys import SynthStats

class ParameterSweepDict(TypedDict):
	start: float
	end: float
	step: float

class ModuleConfig(TypedDict):
	name: str
	parameters: dict[str, Union[ParameterSweepDict, list[Any], Any]]
	flow_config: dict[str, Union[ParameterSweepDict, list[Any], Any]]

class ModuleRun(TypedDict):
	run_dir: str
	synth_stats: SynthStats

class PPARunner:
	design_name: str
	global_flow_config: FlowConfigDict
	modules: list[ModuleConfig]
	runs: dict[str, list[ModuleRun]] = {}
	work_home: str

	def __init__(
		self,
		design_name: str,
		global_flow_config: FlowConfigDict,
		modules: list[ModuleConfig],
		work_home: Optional[str] = None
	):
		self.design_name = design_name
		self.global_flow_config = global_flow_config
		self.modules = modules
		self.work_home = work_home if work_home != None else path.abspath(path.join('.', 'runs', design_name))

		for module in modules:
			self.runs[module['name']] = []

	def run_ppa_analysis(self):
		for module in self.modules:
			print(f"Running flow for module {module['name']}")

			module_work_home = path.join(self.work_home, module['name'])
			module_runner: FlowRunner = FlowRunner({
				**self.global_flow_config,
				'DESIGN_NAME': module['name'],
				'WORK_HOME': module_work_home
			})

			if path.exists(module_work_home):
				rmtree(module_work_home)

			module_runner.preprocess()
			synth_stats = module_runner.synthesis()

			self.runs[module['name']].append({
				'run_dir': module_work_home,
				'synth_stats': synth_stats
			})

	def clean_runs(self):
		rmtree(self.global_flow_config.get('WORK_HOME'))

	def print_stats(self):
		for module_name in self.runs:
			module_runs = self.runs[module_name]
			print(f"---Module {module_name}---")

			for (i, run) in enumerate(module_runs):
				print(f"	Run #{i + 1}:")

				for stat in run['synth_stats']:
					if stat == 'cell_counts':
						formatted_cell_counts = []

						for cell in run['synth_stats']['cell_counts']:
							formatted_cell_counts.append(f"{cell} ({run['synth_stats']['cell_counts'][cell]})")

						print(f"		{stat}: {', '.join(formatted_cell_counts)}")
					else:
						print(f"		{stat}: {run['synth_stats'][stat]}")