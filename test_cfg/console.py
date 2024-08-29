
import os
import hydra
from hydra import utils
from omegaconf import DictConfig
from hydra.core.config_store import ConfigStore
from test_cfg.pycfg import AppConfig
import logging

logger=logging.getLogger(__name__)

# 注册配置
cs = ConfigStore.instance()
cs.store(name="config", node=AppConfig)

def a():
    logger.info(os.getcwd())


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: DictConfig):
    print(f"Database host: {cfg.db.host}")
    print(f"Database port: {cfg.db.port}")
    print(f"Debug mode: {cfg.debug}")
    logger.info(os.getcwd())
    logger.warning(utils.get_original_cwd())
    a()

if __name__ == "__main__":
    # hydra.initialize(config_path=None)
    # hydra.compose(overrides=["hydra.run.dir=null"])
    my_app()
