import sys
sys.path.append('./DM/')
sys.path.append('./DM/models/')
from concurrent import futures
import time
import grpc
from protos.nlp.dm import dm_pb2
from protos.nlp.dm import dm_pb2_grpc
from DmClass import *

# 实现 proto 文件中定义的 DmServicer
class DmService(dm_pb2_grpc.DmServicer):
    
    def __init__(self):
        super(DmService, self).__init__()
        self.dm  = DmClass()
    
    # 实现 proto 文件中定义的 rpc 调用
    def GetDm(self, request, context):
        query = request.text
        history = request.history
        session_id = request.session_id
        robot_id = request.robot_id
        self.dm.load_data(query, history, session_id, robot_id)
        answer, history, emotion = self.dm.response()
        return dm_pb2.DmResponse(answer = answer, history = history, emotion = emotion)


def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dm_pb2_grpc.add_DmServicer_to_server(DmService(), server)
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port('0.0.0.0:50041')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) 
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()