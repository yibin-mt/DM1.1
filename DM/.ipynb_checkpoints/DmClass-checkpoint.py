import re
import sys
import os
import time
import pickle
import joblib
import logging
import fasttext
import jieba
from faq_infer import Faq_inference
from faq_chat import Faq_Chat_inference
from qr_infer import IUR_inference
from chat_infer import Chat_inference
from docqa_infer import DocQAInference
from emotion_infer import Emotion_inference
from skills.fund import *
from collections import defaultdict
from google.protobuf.json_format import MessageToJson

stop_words = ['你知道','的','了','吗','啊','拉','呢','知道','告诉','请问']

id_2_intent = {0:'Faq', 1:'Chat', 2:'DocQa', 3:'Mutil-Turn'}
intent_2_id = {'Faq':0, 'Chat':1, 'DocQa': 2, 'Mutil-Turn':3}

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
def get_logger(name, level=LOG_LEVEL, log_format=LOG_FORMAT):
    """
    :param name: looger 实例的名字
    :param level: logger 日志级别
    :param log_format: logger 的输出`格式
    :return:
    """
    # 强制要求传入 name
    logger = logging.getLogger(name)
    # 如果已经实例过一个相同名字的 logger，则不用再追加 handler
    if not logger.handlers:
        logger.setLevel(level=level)
        formatter = logging.Formatter(log_format)
        # fh = logging.FileHandler(name, "a")
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger


class DmClass(object):
    def __init__(self):
        super(DmClass, self).__init__()
        self.faq = Faq_inference()
        self.faq_chat = Faq_Chat_inference()
        self.qr = IUR_inference({})
        self.docqa = DocQAInference({})
        self.chat = Chat_inference()
        self.emotion = Emotion_inference()
        self.chat_thres = 0.8
        self.qr_thres = 0.8
        self.faq_thres = 0.75
        self.docqa_thres = 0.73
        # self.vectorizer = pickle.load(open('DM/models/tfidftransformer.pkl', "rb"))
        # self.model = joblib.load('DM/models/logisitic_model.pkl')
        self.model  = fasttext.load_model(r"DM/models/model.bin")
        self.DEFAULT_ANSWER = '不好意思，我目前还无法回答您这个问题'
        self.FAQ_DEFAULT_ANSWER = '不好意思，我不大明白你的意思。您想问的是不是：'
        self.DOCQA_DEFAULT_ANSWER = '不好意思，我目前还不知这个问题的答案，我会继续学习的！'
        self.DOCQA_DEFAULT_ANSWER_2 = '您想问的是不是：有关《'

    def load_data(self, query, history, session_id, robot_id):
        self.query = query
        # self.conversation = history.conversation
        self.history = history
        try:
            self.conversation = history.conversation
            # self.conversation = history['conversation']
        except:
            self.conversation = []
        # self.intent = history.intent
        try:
            self.intent = history.intent
            # self.intent = history['intent']
        except:
            self.intent = []
        self.session_id = session_id
        self.robot_id = robot_id
        
    def word_segment(self, text):
        seg_list = jieba.cut(text)
        word_list = []
        for word in seg_list:
            if word not in stop_words:
                word_list.append(word)
        line = " ".join(word_list)
        return line
        
        
    def strategy_2(self, query):
        #先过Faq
        answer, faq, score, match = self.faq_chat.chat_answer(query, self.robot_id)
        if score>0.9:
            return answer, score, 1
        
        pred_class = int(self.model.predict(self.word_segment(query))[0][0][-1])
        #Faq
        if pred_class==0:
            answer, faq, score, match = self.faq.faq_answer(query, self.robot_id)
            if score<self.faq_thres:
                return self.FAQ_DEFAULT_ANSWER+faq, 1.0, pred_class 
            else:
                return answer, score, pred_class
        #闲聊
        elif pred_class==1:
            answer, faq, score, match = self.faq_chat.chat_answer(query, self.robot_id)
            if score < self.chat_thres:
                res = self.chat.response([self.history], query)
                answer = res[0]
                score = res[1]
            # else:
            #     pass
            return answer, score, pred_class
        #文档问答
        else:
            docqa_rst = self.docqa.docqa_answer('wiki', query)
            res = eval(MessageToJson(docqa_rst, ensure_ascii=False, indent=2))
            if res=={}:
                return self.DOCQA_DEFAULT_ANSWER, 1.0, pred_class
            elif res['result'][0]['score']<self.docqa_thres:
                sources=[]
                for i in range(5):
                    sources.append(res['result'][i]['sourceId'])
                common_source = max(sources,key=sources.count)
                ans = self.DOCQA_DEFAULT_ANSWER_2+common_source+'》的问题，可以尝试换个问法哦～'
                return ans, res['result'][0]['score'], pred_class
            else:
                temp_ans = []
                for i in range(5):
                    try:
                        start = int(res['result'][i]['start'])
                        end = int(res['result'][i]['end'])
                        ans = res['result'][i]['context'][start:end]
                        temp_ans.append(ans)
                    except:
                        continue
                first_ans = temp_ans[0]
                #去重
                # temp_ans = sorted(set(temp_ans), key=temp_ans.index)
                # temp_ans.remove(first_ans)
                # for text in temp_ans:
                #     if first_ans in text:
                #         temp_ans.remove(text)
                # self.history['entities'].extend(temp_ans)
                return first_ans, res['result'][0]['score'], pred_class
            
    
    def policy(self,slot, query):
        if slot!='end':
            leg, match = check(query, slot)
        else:
            leg=True
            match = []
        return leg, match
    
    #改写
    def query_write_strategy(self, query, conversation):
        if len(conversation)==2:
            return query
        new_query_1, qr_score_1 = self.qr.iur(conversation[:2], self.query)
        new_query_2, qr_score_2 = self.qr.iur(conversation[2:], self.query)
        new_query, qr_score = new_query_1, qr_score_1
        if qr_score_1 <qr_score_2:
            new_query = new_query_2
            qr_score = qr_score_2
        print(new_query, qr_score)
        if qr_score>self.qr_thres and new_query!=self.query:
            return new_query
        return query
    
    def get_emotion(self, text):
        return self.emotion.emotion_answer(text)
    
    def response(self):        
        #方式二
        logger = get_logger('log.log')
        logger.info('query input:{}'.format(self.query))
        if self.query == '':
            answer = '不好意思，我没听清你在说啥'
            score = 1.0
            intent = ''
            emotion = self.get_emotion(answer)
        else:
            if self.conversation == []:
                self.conversation.insert(0,'')
                self.conversation.insert(1,'')
            new_query = self.query_write_strategy(self.query, self.conversation)
            self.query = new_query
            logger.info('query rewrite output:{}'.format(self.query))

            answer, score, pred_class = self.strategy_2(self.query)
            emotion = self.get_emotion(answer)
            intent = id_2_intent[int(pred_class)]
        logger.info('predict class:{}'.format(intent))
        logger.info('score:{}'.format(score))
        logger.info('dm response :{} \n'.format(answer))
        #更新history
        if len(self.conversation)==4:
            self.conversation.pop(0)
            self.conversation.pop(0)
        self.conversation.insert(2, self.query)
        self.conversation.insert(3, answer)
        if intent!='Mutil-Turn' or self.intent==[]:
            self.intent.append(intent)
        history = {'conversation':self.conversation,'intent':self.intent}
        return answer, history, emotion.answer
                
    
if __name__ == '__main__':
    dm = DmClass()
    history = defaultdict(list)
    history['conversation'].insert(0,'')
    history['conversation'].insert(1,'')
    while True:
        print('用户：', end=' ')        
        query = input()
        start_time = time.time()
        session_id = 1
        robot_id = 1
        dm.load_data(query, history, session_id, robot_id)
        answer, score, intent, slot, entity, task_id, emotion = dm.response()
        end_time = time.time()
        print('*' * 20 + '回复完成!用时{:.2f}s'.format(end_time - start_time) + '*' * 20)
        print("机器人：: " + answer)
        print('score' + str(score))
        print('intent', intent)
        if len(history['conversation'])==4:
            history['conversation'].pop(0)
            history['conversation'].pop(0)
        history['conversation'].insert(2,query)
        history['conversation'].insert(3,answer)
        #多轮对话内的意图id与task id，不重复加入
        if intent!='Mutil-Turn' or history['intent']==[] or (intent == 'Mutil-Turn' and history['intent'][-1]!='Mutil-Turn'):
            history['intent'].append(intent)
            history['task_id'].extend(task_id)
        if slot == ['end'] or (history['intent']!=[] and history['intent'] in ['Faq', 'Chat']):
            history['slots'].clear()
            history['entities'].clear()
            history['task_id'].clear()
        else:
            history['slots'].extend(slot)
            history['entities'].extend(entity)
        print('历史', history)