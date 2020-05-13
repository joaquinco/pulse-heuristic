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
        ms = (end - start).microseconds
        unit = 'ms'
        if ms > 1e5:
          ms = ms / 1e6
          unit = 's'

        logging.debug(f'{message or name} took {ms}{unit}')

    return wrapper

  if hasattr(message, '__call__'):
    return decorator(message)

  return decorator
