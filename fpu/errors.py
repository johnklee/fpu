"""Module to hold errors related to FPU."""


class FPUError(Exception):
  pass


class UOException(FPUError):
  """Unsupported Operation Exception."""
  def __init__(self, message, errors=None):
    super(FPUError, self).__init__(message)
    self.errors = errors
