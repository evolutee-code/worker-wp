from logging import INFO, Formatter, getLogger, StreamHandler


def _set_handler(logger, handler):
    handler.setLevel(INFO)
    handler.setFormatter(Formatter(
        '%(name)s: %(funcName)s '
        '[%(levelname)s]: %(message)s'))
    logger.addHandler(handler)
    return logger


logger = getLogger(__name__)
logger = _set_handler(logger, StreamHandler())
logger.setLevel(INFO)
logger.propagate = False
