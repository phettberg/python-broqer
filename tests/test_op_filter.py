import pytest

from broqer import op, NONE
from broqer.op.operator import Operator
from tests.helper_single import check_get_method, check_subscription, check_dependencies


test_vector = [
    # o, args, kwargs, input_vector, output_vector
    (op.Filter, (lambda v: v == 0,), {},
        (1, 2, 0, 0.0, None),
        (NONE, NONE, 0, 0.0, NONE)),
    (op.Filter, (lambda a, b: a == b, 2), {},
        (0, 2, 2.0, 1),
        (NONE, 2, 2.0, NONE)),
    (op.Filter, (lambda a, b, c: a + b == c, 2), {'unpack': True},
        ((0, 2), (0, 3), (-1.0, 1.0)),
        ((0, 2), NONE, (-1.0, 1.0))),
    (op.Filter, (lambda a, b, c: a + b == c,), {'unpack': True, 'c': 2},
        ((0, 2), (0, 3), (-1.0, 3.0)),
        ((0, 2), NONE, (-1.0, 3.0))),
    (op.build_filter(lambda v: v == 0), (), {},
        (1, 2, 0, 0.0, None),
        (NONE, NONE, 0, 0.0, NONE)),
    (op.build_filter(lambda a, b, c: a + b == c, unpack=True), (2,), {},
        ((0, 2), (0, 3), (-1.0, 1.0)),
        ((0, 2), NONE, (-1.0, 1.0))),
    (lambda v: op.build_filter(unpack=True)(lambda a, b, c: a + b == c)(v), (2,), {},
        ((0, 2), (0, 3), (-1.0, 1.0)),
        ((0, 2), NONE, (-1.0, 1.0))),
    (op.True_, (), {},
        (1, 2, 0, 0.0, None, False, [1]),
        (1, 2, NONE, NONE, NONE, NONE, [1])),
    (op.True_, (), {},
        (0, ),
        (NONE, )),
    (op.False_, (), {},
        (1, 2, 0, 0.0, None, False, [1]),
        (NONE, NONE, 0, 0.0, None, False, NONE)),
    (op.False_, (), {},
        (0, ),
        (0, )),
]


@pytest.mark.parametrize('method', [check_get_method, check_subscription, check_dependencies])
@pytest.mark.parametrize('o,args,kwargs,input_vector,output_vector', test_vector)
def test_operator(method, o, args, kwargs, input_vector, output_vector):
    operator = o(*args, **kwargs)

    method(operator, input_vector, output_vector)
