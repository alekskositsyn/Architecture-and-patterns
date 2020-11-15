import copy


class PrototypeMixin:
    """ Прототип - копирует обьект """

    def clone(self):
        return copy.deepcopy(self)
