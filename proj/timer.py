import logging
from datetime import datetime

def timed(message):
  def decorator(wrapped):
    def wrapper(*args, **kwargs):
      try:
        start = datetime.now()
        name = wrapped.__name__
        return wrapped(*args, **kwargs)
      finally:
        end = datetime.now()
        logging.debug(f'{message or name} took {(end - start).seconds} secs')

    return wrapper

  if hasattr(message, '__call__'):
    return decorator(message)

  return decorator
