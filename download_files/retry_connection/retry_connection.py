import asyncio
import logging

from functools import wraps

log = logging.getLogger(__name__)

def retry(*exceptions, retries=3, cooldown=1, verbose=True):
    """Decorate an async function to execute it a few times before giving up.
    Args:
        exceptions (Tuple[Exception]) : The exceptions expected during function execution
        retries (int): Number of retries of function execution.
        cooldown (int): Seconds to wait before retry.
        verbose (bool): Specifies if we should log about not successful attempts.
    """

    def wrap(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            retries_count = 0
            while True:
                try:
                    result = await func(*args, **kwargs)
                except exceptions as err:
                    retries_count += 1
                    message = (
                        f"Exception during {func} execution: "
                        f"{retries_count} of {retries} retries attempted"
                    )

                    if retries_count > retries:
                        verbose and log.exception(message)
                        raise ValueError(
                            f"ERROR! There was a problem trying to download the image, {err}"
                        )
                    else:
                        verbose and log.warning(message)

                    if cooldown:
                        await asyncio.sleep(cooldown)
                else:
                    return result
        return inner
    return wrap