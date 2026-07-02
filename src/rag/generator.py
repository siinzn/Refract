from src.retrieval.retrieval import Retrieval
from collections import Counter
import mlflow
from langchain_ollama import ChatOllama

mlflow.set_experiment("Refract")
mlflow.langchain.autolog()

class RAG:
    def __init__(self, query: str, threshold, limit=5):
        self.query = query
        self.threshold = threshold
        self.limit = limit
        self.retrieval = Retrieval(query_text=self.query) 
        self.results = self.retrieval.hybrid_retrieval()
        self.results = self.retrieval.reranker(self.results)
        self.total_score: float = 0.0
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0)

    def summarize_evidence(self):
        if not self.results:
            return "No evidence available to summarize."
        context = "\n".join([res[0]['text_clean'] for res in self.results])
        prompt = f"Summarize the main themes, common opinions, and any notable disagreements in these developer discussions in 2-3 sentences:\n\n{context}"
        response = self.llm.invoke(prompt)
        return response.content
    
    def compute_score(self):
        """
        okay so to get the score i need to combine and get a score between 0-1
        - total no. result / threshold 
        - avg score which is already given
        - sentiment coinsistency - for this if positive is more then sentiment consistency is good
        - topic similarity consistency - if topics are similar then its good

        i used dict for sentiment since i know the keys are going to be the same for all ouputs, but for 
        topic label it wont be. 
        """
        hybrid_score = 0
        sentiment_label = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
        topic_label = []
        if len(self.results) == 0:
            return self.total_score
        
        result_count = len(self.results) / self.limit

        for res, h_score in self.results:
            #sentiment consistency
            if res['sentiment_label'] == 'positive':
                sentiment_label["positive"] += 1
            elif res['sentiment_label'] == 'negative':
                sentiment_label["negative"] += 1
            else:
                sentiment_label["neutral"] += 1
            #topic similarity
            topic_label.append(res['topic_label'])
            #hyrbid score
            hybrid_score += h_score
        
        #topic_label_consistency = Counter(topic_label).most_common(1)[0][1] / len(self.results)  #Counter adds frequency to each element, most_common(1) gets the most count, [0][1] gets the first element's count
        hybrid_score = hybrid_score/ len(self.results)
        #sentiment_label_consistency = max(sentiment_label.values()) / len(self.results) #max gets the maximum value in the dict pairs
        self.total_score = (result_count + hybrid_score) / 2 #this is to get a score between 0-1

    def routing(self):
        self.compute_score()
        if self.total_score < self.threshold:
            fallback_prompt = f"You are a helpful assistant. Answer the following question clearly and concisely: {self.query}"
            response = self.llm.invoke(fallback_prompt)
            return {
                "answer": f"I could not find a link to your question with systems programming but here is the answer for your question anyways.\n\n{response.content}",
                "source": "Ollama fallback",
                "confidence": self.total_score,
                "evidence": []
            }
            
        #use ollama
        context = "" 
        for idx, (res, score) in enumerate(self.results, start=1):
            context += (
                f"[{idx}] Source: {res['source']} | Sentiment: {res['sentiment_label']} | Topic: {res['topic_label']}\n"
                f"Text: \"{res['text_clean']}\"\n"
                f"Author: {res['author']} | Likes: {res['like_count']}\n"
            )
        sources_used = list(set(res['source'] for res, score in self.results))
        prompt = (
            f"You are an expert analyst of developer discussions about systems programming. Based ONLY on the following real developer comments and answers, answer the question below."
            f"Do not add any information not present in the context. If the context is insufficient, say so."
            f"Question: {self.query}"
            f"Context: {context}"
            f"Answer: "
        )
        response = self.llm.invoke(prompt)
        summary = self.summarize_evidence()

        return {
            "answer": response.content,
            "source": sources_used,
            "confidence": self.total_score,
            "evidence": self.results,
            "summary": summary
        }
    
    def close(self):
        self.retrieval.close()
        
        

         
    


