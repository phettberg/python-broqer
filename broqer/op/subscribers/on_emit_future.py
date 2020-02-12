"""
Build a future able to await for

Usage:

>>> import asyncio
>>> from broqer import Value, op
>>> s = Value()

>>> _ = asyncio.get_event_loop().call_later(0.05, s.emit, 1)

>>> asyncio.get_event_loop().run_until_complete(op.OnEmitFuture(s) )
1

#>>> _ = asyncio.get_event_loop().call_later(0.05, s.emit, (1, 2))
#>>> asyncio.get_event_loop().run_until_complete(s)
(1, 2)
"""
import asyncio
from typing import Any, Optional, Union

from broqer.publisher import Publisher
from broqer.subscriber import Subscriber
from broqer.disposable import SubscriptionDisposable


class OnEmitFuture(Subscriber, asyncio.Future):
    """ Build a future able to await for.
    :param publisher: source publisher
    :param timeout: timeout in seconds
    :param loop: asyncio loop to be used
    """
    def __init__(self, publisher: Publisher, timeout=None, omit_first_emit=False, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()

        asyncio.Future.__init__(self, loop=loop)
        self.add_done_callback(self._cleanup)

        self._publisher = publisher

        self._omit_first_emit = omit_first_emit
        publisher.subscribe(self)

        if timeout is not None:
            self._timeout_handle = loop.call_later(
                timeout, self.set_exception, asyncio.TimeoutError)
        else:
            self._timeout_handle = None

    def _cleanup(self, _future):
        self._publisher.unsubscribe(self)

        if self._timeout_handle is not None:
            self._timeout_handle.cancel()
            self._timeout_handle = None

    def emit(self, value: Any, who: Optional[Publisher] = None) -> None:
        if who is not self._publisher:
            raise ValueError('Emit from non assigned publisher')

        if self._omit_first_emit:
            self._omit_first_emit = False
            return

        if not self.done():
            self.set_result(value)
