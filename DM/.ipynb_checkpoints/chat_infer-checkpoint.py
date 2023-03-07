from protos.nlp.chat import chat_pb2
from protos.nlp.chat import chat_pb2_grpc
from grpc.beta import implementations


class Chat_inference(object):
    def __init__(self):
        super(Chat_inference, self).__init__()

    def response(self, history_utts, query):
        conn = implementations.insecure_channel("172.31.208.9", 60005)
        client = chat_pb2_grpc.ChatStub(channel=conn._channel)
        res = client.GetChat(chat_pb2.ChatRequest(history=history_utts, query=query, session_id='1', robot_id=1), timeout=60)
        answer = res.answer
        score = res.score
        query = res.query
        sessionid = res.session_id
        return answer, score, query, sessionid