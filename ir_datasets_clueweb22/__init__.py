from ir_datasets import main_cli as irds_main_cli
from ir_datasets_clueweb22.clueweb22 import register as register_clueweb22


def register() -> None:
    register_clueweb22()


def main_cli() -> None:
    register()
    irds_main_cli()
