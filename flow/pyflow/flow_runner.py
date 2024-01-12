from typing import TypedDict, Union, Any
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

class FlowRunner:
	global_flow_config: FlowConfig
	modules: list[Module]
	work_home: str

	def __init__(self, global_flow_config: FlowConfigDict, modules: list[Module]):
		self.global_flow_config = FlowConfig(global_flow_config)
		self.modules = modules

		if 'WORK_HOME' not in global_flow_config:
			self.work_home = path.abspath(path.join('.', 'runs', global_flow_config['DESIGN_NAME']))
			self.global_flow_config.set('WORK_HOME', self.work_home)

	def run_flow(self):
		self.global_flow_config = preprocess(self.global_flow_config)
		synth(self.global_flow_config)
		floorplan(self.global_flow_config)

	def clean_runs(self):
		rmtree(self.global_flow_config.get('WORK_HOME'))