from ai.engine import engine
from ai.prompts import CUSTOMER_SERVICE


class CustomerServiceBot:
    def __init__(self):
        self.conversations = {}

    def get_response(self, question: str, customer_name: str = "亲", conversation_id: str = None) -> str:
        prompt = f"Customer name: {customer_name}\nCustomer question: {question}"
        conv_history = ""
        if conversation_id and conversation_id in self.conversations:
            conv_history = "\n对话历史：\n" + "\n".join(self.conversations[conversation_id][-5:])
            prompt += conv_history

        system_prompt = CUSTOMER_SERVICE.format(question=question)
        reply = engine.chat(system_prompt, f"请回复以下客户咨询：\n{prompt}", temperature=0.7)

        if conversation_id:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            self.conversations[conversation_id].append(f"客户: {question}")
            self.conversations[conversation_id].append(f"客服: {reply}")

        return reply

    def analyze_sentiment(self, message: str) -> str:
        prompt = f"""分析以下客户消息的情感倾向，只回复一个词：positive（正面）, negative（负面）, neutral（中性）。

消息：{message}"""
        return engine.chat("你是一个情感分析助手，只输出一个词。", prompt, temperature=0.1)
