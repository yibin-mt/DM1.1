import grpc
from protos.nlp.dm import dm_pb2
from protos.nlp.dm import dm_pb2_grpc

def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:50051')
    # 调用 rpc 服务
    stub = dm_pb2_grpc.DmStub(channel)
    
    #第一轮
    text = '你知道碧昂斯吗'
    print('text:',text)
    response = stub.GetDm(dm_pb2.DmRequest(text=text, history={}, session_id='1', robot_id = -1))
    print("Dm client received: " + response.answer,'\n')
    history = response.history
    
    #第二轮
    text = '他的第一张专辑叫什么'
    print('text:',text)
    response = stub.GetDm(dm_pb2.DmRequest(text=text, history=history, session_id='1', robot_id = -1))
    print("Dm client received: " + response.answer)
    print(response.history.conversation)
    history = response.history
if __name__ == '__main__':
    run()