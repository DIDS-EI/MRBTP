
import os
import hydra
from hydra import utils
from omegaconf import DictConfig
from omegaconf import OmegaConf
from hydra.core.config_store import ConfigStore
from test_cfg.pycfg import AppConfig
import logging

logger=logging.getLogger(__name__)
hydra.initialize(config_path=None)

cfg = OmegaConf.structured((AppConfig))
logger.info(os.getcwd())
# logger.warning(utils.get_original_cwd())
# print(cfg.pretty())