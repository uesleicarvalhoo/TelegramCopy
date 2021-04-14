from functools import wraps
from typing import Any, Callable

from src.utils.logger import logger


def error_handler(*exceptions, re_raise: bool = True) -> Callable:
    def handler(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return fn(*args, **kwargs)

            except exceptions as err:
                logger.error("Error on function %s, description: %s" % (fn.__name__, str(err)))
                if re_raise:
                    raise err

        return wrapper

    return handler


def error_handler_context(*exceptions, context=None) -> None:
    try:
        yield

    except exceptions as err:
        if context:
            logger.error("Error, on context %s, description: %s" % (context, err))
        else:
            logger.error("Description: %s" % err)
