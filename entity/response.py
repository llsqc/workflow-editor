from abc import abstractmethod, ABC

"""
An abstract class as stand,
to ensure that all returned values can be serialised
"""


class Response:
    def to_dict(self):
        raise NotImplementedError
