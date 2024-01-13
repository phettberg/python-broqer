from typing import Any, Union

from broqer.publisher import Publisher


class ListPublisher(Publisher):
    def __init__(self, init: Any = None) -> None:
        Publisher.__init__(self)
        self._state = []
        if init is not None:
            if isinstance(init, list):
                self._state[:] = init
            elif isinstance(init, ListPublisher):
                self._state[:] = init._state[:]
            else:
                self._state = list(init)

    def __iter__(self):
        return iter(self._state)

    def __setitem__(self, index: int, item: Any):
        self._state[index] = item
        Publisher.notify(self, self._state)

    def insert(self, index: int, item: Any):
        self._state.insert(index, item)
        Publisher.notify(self, self._state)

    def append(self, item: Any):
        self._state += item,
        Publisher.notify(self, self._state)

    def remove(self, item: Any):
        self._state.remove(item)
        Publisher.notify(self, self._state)

    def extend(self, other: Union[list, 'ListPublisher']):
        if isinstance(other, ListPublisher):
            self._state.extend(other._state)
        else:
            self._state.extend(other)
        Publisher.notify(self, self._state)

    def clear(self):
        self._state.clear()
        Publisher.notify(self, self._state)

    def reverse(self):
        self._state.reverse()
        Publisher.notify(self, self._state)

    def count(self, item: Any):
        return self._state.count(item)

    def sort(self, /, *args, **kwds):
        self._state.sort(*args, **kwds)
