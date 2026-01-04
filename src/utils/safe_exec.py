from contextlib import asynccontextmanager
from logging import Logger
from typing import Type

ErrMappingType = dict[Type[Exception], str]
@asynccontextmanager
async def safe_exec(
    err_mapping: ErrMappingType,
    logger: Logger,
    throw: bool
):
    
    """
    A context manager to safely execute a block of code.

    Parameters
    ----------
    err_mapping : dict[Type[Exception], str]
        A dictionary mapping exception types to error messages.
    logger : Logger
        A logger to log errors.
    throw : bool
        Whether to rethrow the exception or not.

    Yields
    -------
    None

    Raises
    ------
    Exception
        If throw is True, the exception is rethrown.
    """
    try:
        yield
    except Exception as e:
        # Get an error message for giving err
        msg: str = err_mapping.get(
            type(e),
            f"Error occured: {e}"
        )
        
        logger.error(msg, exc_info=True)
        
        if throw:
            raise e
        else:
            pass
        