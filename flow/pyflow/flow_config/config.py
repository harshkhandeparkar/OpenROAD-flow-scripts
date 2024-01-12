from typing import Union

from .common_config import FlowCommonConfigDict, FlowCommonConfig
from .platform_config import FlowPlatformConfigDict, FlowPlatformConfig
from .design_config import FlowDesignConfigDict, FlowDesignConfig

FlowConfigDict = Union[FlowCommonConfigDict, FlowPlatformConfigDict, FlowDesignConfigDict]

class FlowConfig(FlowCommonConfig, FlowPlatformConfig, FlowDesignConfig):
	configopts: Union[FlowConfigDict, dict]
	config: FlowConfigDict

	def __init__(self, configopts: Union[FlowConfigDict, dict]):
		self.configopts = configopts.copy()
		self.config = configopts.copy()

		FlowCommonConfig.__init__(self)
		FlowPlatformConfig.__init__(self)
		FlowDesignConfig.__init__(self)

	def get(self, key: str):
		if key in self.config:
			return self.config[key]
		else:
			return None

	def set(self, key, value):
		self.config[key] = value

		self.calculate_dirs()

	def get_env(self):
		"""Returns the corresponding environment variables for the given configuration."""

		return FlowDesignConfig.get_env(
			self,
			FlowPlatformConfig.get_env(
				self,
				FlowCommonConfig.get_env(self, self.config)
			)
		)
