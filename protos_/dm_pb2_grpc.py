# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import dm_pb2 as dm__pb2


class DmStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetDm = channel.unary_unary(
                '/nlp.dm.Dm/GetDm',
                request_serializer=dm__pb2.DmRequest.SerializeToString,
                response_deserializer=dm__pb2.DmResponse.FromString,
                )


class DmServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetDm(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DmServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetDm': grpc.unary_unary_rpc_method_handler(
                    servicer.GetDm,
                    request_deserializer=dm__pb2.DmRequest.FromString,
                    response_serializer=dm__pb2.DmResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nlp.dm.Dm', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Dm(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetDm(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/nlp.dm.Dm/GetDm',
            dm__pb2.DmRequest.SerializeToString,
            dm__pb2.DmResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)