from typing import TypedDict, Union, Any, Optional
from os import path
from shutil import rmtree

from .flow_config import FlowConfig, FlowConfigDict
from .flow_steps import preprocess, synth, floorplan

class ParameterSweepDict(TypedDict):
	start: float
	end: float
	step: float

class Module(TypedDict):
	name: str
	parameters: dict[str, Union[ParameterSweepDict, list[Any], Any]]
	flow_config: dict[str, Union[ParameterSweepDict, list[Any], Any]]

class PPARunner:
	design_name: str
	global_flow_config: FlowConfigDict
	modules: list[Module]
	work_home: str

	def __init__(self, design_name: str, global_flow_config: FlowConfigDict, modules: list[Module], work_home: Optional[str] = None):
		self.design_name = design_name
		self.global_flow_config = global_flow_config
		self.modules = modules
		self.work_home = work_home if work_home != None else path.abspath(path.join('.', 'runs', design_name))

	def run_ppa_analysis(self):
		for module in self.modules:
			print(f"Running flow for module {module['name']}")

			module_work_home = path.join(self.work_home, module['name'])
			module_config: FlowConfig = FlowConfig({
				**self.global_flow_config,
				'DESIGN_NAME': module['name'],
				'WORK_HOME': module_work_home
			})

			if path.exists(module_work_home):
				rmtree(module_work_home)

			module_config = preprocess(module_config)
			stats = synth(module_config)

			print(stats)

	def clean_runs(self):
		rmtree(self.global_flow_config.get('WORK_HOME'))