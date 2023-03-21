from contextlib import contextmanager

from jina import Flow

from .helper import JINA_RESULTS, RESULT, parse_uses_with


@contextmanager
def StartFlow(protocol, uses, uses_with, port=12345):
    with Flow(port=port, protocol=protocol).add(
        uses=uses,
        uses_with=parse_uses_with(uses_with),
        env={'JINA_LOG_LEVEL': 'INFO'},
    ) as f:
        yield str(f.protocol).lower() + '://' + f.host + ':' + str(f.port)


def ServeGRPC(uses, uses_with, port=12345):
    return StartFlow('grpc', uses, uses_with, port)


def ServeHTTP(uses, uses_with, port=12345):
    return StartFlow('http', uses, uses_with, port)


def ServeWebSocket(uses, uses_with, port=12345):
    return StartFlow('websocket', uses, uses_with, port)


def Interact(host, inputs):
    from jina import Client

    r = Client(host=host).post(on='/run', parameters=inputs, return_responses=True)
    if r:
        results = r[0].parameters.get(JINA_RESULTS, None)
        if results:
            # TODO: handle replicas
            for v in results.values():
                if RESULT in v:
                    return v[RESULT]
    return None
