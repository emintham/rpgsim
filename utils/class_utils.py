class Borg(object):
    """Borg Pattern"""

    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
