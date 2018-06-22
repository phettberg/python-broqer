"""
Combine the latest emit of multiple publishers and emit the combination

Usage:

>>> from broqer import Subject, op
>>> s1 = Subject()
>>> s2 = Subject()

>>> combination = s1 | op.combine_latest(s2)
>>> disposable = combination | op.sink(print)

CombineLatest is only emitting, when all values are collected:

>>> s1.emit(1)
>>> s2.emit(2)
1 2
>>> s2.emit(3)
1 3
>>> disposable.dispose()

Subscribing to a CombineLatest with all values available is emitting the values
immediatly on subscribtion:

>>> combination | op.sink(print, 'Second sink:')
Second sink: 1 3
<...>

"""
from typing import Any, Dict, MutableSequence, Sequence  # noqa: F401

from broqer import Publisher, Subscriber, SubscriptionDisposable

from ._operator import MultiOperator, build_operator


class CombineLatest(MultiOperator):
    def __init__(self, *publishers: Publisher, map=None) -> None:
        MultiOperator.__init__(self, *publishers)
        partial = [None for _ in publishers]  # type: MutableSequence[Any]
        self._partial_state = partial
        self._missing = set(publishers)
        self._index = \
            {p: i for i, p in enumerate(publishers)
             }  # type: Dict[Publisher, int]
        self._map = map
        self._state = None  # type: Sequence[Any]

    def subscribe(self, subscriber: Subscriber) -> SubscriptionDisposable:
        disposable = MultiOperator.subscribe(self, subscriber)
        if not self._missing:
            if self._map:
                self._state = (self._map(*self._partial_state),)
            else:
                self._state = self._partial_state
            self.notify(*self._state)
        return disposable

    def emit(self, *args: Any, who: Publisher) -> None:
        assert who in self._publishers, 'emit from non assigned publisher'
        if self._missing and who in self._missing:
            self._missing.remove(who)
        if len(args) == 1:
            args = args[0]
        self._partial_state[self._index[who]] = args
        if not self._missing:
            if self._map:
                self._state = (self._map(*self._partial_state),)
            else:
                self._state = self._partial_state
            self.notify(*self._state)

    @property
    def state_raw(self):
        return self._state


combine_latest = build_operator(CombineLatest)
