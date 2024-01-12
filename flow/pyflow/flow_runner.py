from typing import TypedDict
from os import path

from .flow_config import FlowConfig, FlowConfigDict
from .flow_steps import preprocess, synth, floorplan

class Module(TypedDict):
	name: str
	parameters: list[dict]
	flow_config: list[dict]

class FlowRunner:
	global_flow_config: FlowConfig
	modules: list[Module]
	work_home: str

	def __init__(self, global_flow_config: FlowConfigDict, modules: list[Module]):
		if 'WORK_HOME' not in global_flow_config:
			global_flow_config['WORK_HOME'] = self.work_home = path.abspath(path.join('.', 'runs', global_flow_config['DESIGN_NAME']))

		self.global_flow_config = FlowConfig(global_flow_config)
		self.modules = modules

	def run_flow(self):
		self.global_flow_config = preprocess(self.global_flow_config)
		synth(self.global_flow_config)
		floorplan(self.global_flow_config)