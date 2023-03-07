import grpc
import sys
from protos.nlp.rewrite import rewrite_pb2
from protos.nlp.rewrite import rewrite_pb2_grpc

import requests
import base64

from grpc.beta import implementations

class IUR_inference(object):
    def __init__(self, config):
        self.host = config.get('faq_host', "192.168.68.26")
        self.port = config.get('faq_port', 60005)
        self.timeout = config.get('timeout', 60)

    def iur(self, history_utts, query):
        conn = implementations.insecure_channel(self.host, self.port)
        client = rewrite_pb2_grpc.ReWriteStub(channel=conn._channel)
        res = client.GetReWrite(rewrite_pb2.ReWriteRequest(history=history_utts, query=query, session_id='1', robot_id=1), timeout=self.timeout)
        new_query = res.new_query
        score = res.score
        return new_query, score

if __name__ == "__main__":
    # history_utts = ["", "", "北京可以办理工作居住证么？", "可以，根据政府政策规定，入职满一年后满足条件的可办理。"]
    # query = "多久能下来？"
    # history_utts = ["", "", "有松下的吹风机吗", "没有哦亲"]
    # query = "那有戴森的吗"
    # history_utts = ["", "", "帮我放周杰伦的歌", "好的，正在播放周杰伦的稻香"]
    # query = "算了，不要放他的，放张学友的"
    history_utts = ['你好', '你好呀，我可以帮你做点啥嘛', '什么时候发工资', " 每月 10 日，发放上月工资，遇节假日顺延 。"]
    query="我为什么没收到"
    tt = IUR_inference({})
    new_query, score = tt.iur(history_utts, query)
    print(new_query, score)
#     history_utts_list = [history_utts]*1
#     query_list = [query]*1
    
#     max_ctx_len = 80
#     max_src_len = 50
#     tt = IUR_inference({})
#     tt.iur(history_utts_list[0], query_list[0])

#     import numpy as np
#     import time
#     history_lens, query_lens = [], []
#     latency_list = []
#     for history_utts, query in zip(history_utts_list, query_list):
#         start_time = time.time()    
#         print(f"history_utts={history_utts}")
#         print(f"query={query}")
#         iur_rst = tt.iur(history_utts, query)
#         print(f"rewrite={iur_rst[0]}")
#         time_cost = time.time() - start_time
#         latency_list.append(time_cost*1000)
#         history_len = len("".join(history_utts))
#         query_len = len(query)
#         history_lens.append(min(max_ctx_len, history_len))
#         query_lens.append(min(max_src_len, query_len))
    
#     print(f"num of examples is {len(history_utts_list)}")
#     print(f"mean of history utt len is {np.mean(history_lens)}")
#     print(f"mean of query len is {np.mean(query_lens)}")
#     print(f"mean of latency is {np.mean(latency_list)}ms")
#     print(f"0.95 of latency is {np.quantile(latency_list, 0.95)}ms")
#     print(f"0.99 of latency is {np.quantile(latency_list, 0.99)}ms")

    


