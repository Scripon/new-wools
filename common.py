import toml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def get_config():
    with open(str(Path(BASE_DIR / 'config.toml'))) as f:
        configs = toml.load(f)
    return configs
