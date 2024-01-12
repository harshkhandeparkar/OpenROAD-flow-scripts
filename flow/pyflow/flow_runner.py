from typing import TypedDict

from .flow_config import FlowConfig

class Module(TypedDict):
	name: str
	parameters: list[dict]
	flow_config: list[dict]

class FlowRunner:
	global_flow_config: FlowConfig
	modules: list[Module]