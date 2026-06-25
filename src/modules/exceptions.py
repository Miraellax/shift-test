class ItemNotFoundException(Exception):
    """
    Exception raised when item is not found in DB
    """
    pass

class DuplicateItemValueException(Exception):
    """
    Exception raised when item cannot be created/changed with current values due to duplicate values
    """
    pass