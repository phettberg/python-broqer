import asyncio

import pytest

from broqer.op import MapAsync, Mode

from .helper import check_async_operator_coro, NONE

async def add1(v, i=1):
    return v+i

async def wait(v, duration=0.15):
    await asyncio.sleep(duration)
    return v

@pytest.mark.parametrize('map_coro, args, kwargs, mode, input_vector, output_vector', [
    (add1, (), {}, Mode.CONCURRENT, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (add1, (2,), {}, Mode.CONCURRENT, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 3), (0.1, 4), (0.2, 5))),
    (add1, (), {'i':3}, Mode.CONCURRENT, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 4), (0.1, 5), (0.2, 6))),
    (add1, (), {}, Mode.INTERRUPT, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (add1, (), {}, Mode.QUEUE, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (add1, (), {}, Mode.LAST, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (add1, (), {}, Mode.LAST_DISTINCT, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (add1, (), {}, Mode.SKIP, ((0, 1), (0.1, 2), (0.2, 3)), ((0.01, 2), (0.1, 3), (0.2, 4))),
    (wait, (), {}, Mode.CONCURRENT, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.15, 0), (0.2, 1), (0.25, 2), (0.35, 3))),
    (wait, (), {}, Mode.INTERRUPT, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.35, 3),)),
    (wait, (), {}, Mode.QUEUE, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.15, 0), (0.30, 1), (0.45, 2), (0.60, 3))),
    (wait, (), {}, Mode.LAST, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.15, 0), (0.3, 2), (0.45, 3))),
    (wait, (), {}, Mode.LAST_DISTINCT, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.15, 0), (0.3, 2), (0.45, 3))),
    (wait, (), {}, Mode.LAST_DISTINCT, ((0, 0), (0.05, 1), (0.1, 0), (0.2, 3)), ((0.15, 0), (0.35, 3))),
    (wait, (), {}, Mode.SKIP, ((0, 0), (0.05, 1), (0.1, 2), (0.2, 3)), ((0.15, 0), (0.35, 3))),
])
@pytest.mark.asyncio
async def test_with_publisher(map_coro, args, kwargs, mode, input_vector, output_vector, event_loop):
    await check_async_operator_coro(MapAsync, (map_coro, *args), {'mode':mode, **kwargs}, input_vector, output_vector, loop=event_loop)