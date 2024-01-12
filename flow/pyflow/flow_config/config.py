from typing import Union

from .common_config import FlowCommonConfigDict, FlowCommonConfig
from .platform_config import FlowPlatformConfigDict, FlowPlatformConfig
from .design_config import FlowDesignConfigDict, FlowDesignConfig

_FlowConfigDict = Union[FlowCommonConfigDict, FlowPlatformConfigDict, FlowDesignConfigDict]

class FlowConfig():
	config: _FlowConfigDict

	def __init__(self, configopts: Union[_FlowConfigDict, dict]):
		self.config = configopts

		FlowCommonConfig.__init__(self, self.config)
		FlowPlatformConfig.__init__(self, self.config)
		FlowDesignConfig.__init__(self, self.config)

	def get(self, key):
		return self.config[key]

	def set(self, key, value):
		self.config[key] = value

	def get_env(self):
		"""Returns the corresponding environment variables for the given configuration."""

		return FlowDesignConfig.get_env(
			self,
			FlowPlatformConfig.get_env(
				self,
				FlowCommonConfig.get_env(self, self.config)
			)
		)
