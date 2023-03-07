import grpc
from protos.nlp.emotion import emotion_pb2, emotion_pb2_grpc
from grpc.beta import implementations
class Emotion_inference():
    def __init__(self):
        super(Emotion_inference, self).__init__()

    def emotion_answer(self, query):
        channel = grpc.insecure_channel('172.31.208.10:58999')
        emotion_client = emotion_pb2_grpc.EmotionStub(channel)
        res = emotion_client.GetEmotion(emotion_pb2.EmotionRequest(query=query, session_id='1', robot_id=2), timeout=1)
        return res
