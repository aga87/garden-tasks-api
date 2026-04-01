import logging
import os


def setup_logging() -> None:
    debug = os.getenv("GARDEN_APP_DEBUG") == "1"
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(name)s: %(message)s",
        force=True,  # ensures config is applied even if already set
    )
