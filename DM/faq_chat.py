#robot——id值为0时使用客服FAQ库；值为1使用数字人FAQ库；值为2时使用闲聊FAQ库
import grpc
from protos.nlp.faq import faq_pb2 as pb2
from protos.nlp.faq import faq_pb2_grpc as pb2_grpc
from grpc.beta import implementations
class Faq_Chat_inference():
    def __init__(self):
        super(Faq_Chat_inference, self).__init__()

    def chat_answer(self, query, robot_id):
        # conn = grpc.insecure_channel('192.168.4.29:60009')
        # conn = grpc.insecure_channel(self.ip+':'+self.port)
        conn = grpc.insecure_channel('172.31.208.10:58999')
        client = pb2_grpc.FaqStub(conn)
        res = client.GetFaq(pb2.FaqRequest(query=query, robot_id=1), timeout=1)
        answer = res.answer #faq对应的答案
        match = res.match   #匹配到的相似问句
        faq = res.faq       #对应的标准问句
        score = res.score   #匹配模型匹配的分数，可以视为置信度
        return answer, faq, score, match

# if __name__ == "__main__":
#     query = "怎么连接打印机"
#     tt = Faq_inference()
#     print(tt.faq_answer(query))