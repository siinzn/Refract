from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import pandas as pd
#MAIN THING THINK ABOUT WHERE I CAN HAVE DATA STRUCUTRE, BUT BEFORE IMPLEMENTING IT CHECK IF SOME FUNCTIONS HAVE 

class Analyser:

    def __init__(self, source, column_name):
        self.source = source
        self.column_name = column_name
        if self.source == "youtube":
            self.vader = SentimentIntensityAnalyzer()
        else:
            self.MODEL = f"Cloudy1225/stackoverflow-roberta-base-sentiment"
            self.roberta_pipeline = pipeline(task="sentiment-analysis", model=self.MODEL, truncation=True)


    """
    for youtube comments dataset, i will be using VADER, vader works best for short in terms of word count.
    for stackoverflow dataset, i will use cardiffnlp/twitter-roberta-base-sentiment using transformers since 
    stackoverflow comments/answer could be longer in terms of word count
    """

    def sentiment_analysis(self, df):
        df = df.copy() #creates same df for pandas to work
        if self.source == "youtube":
            def vader_analysis(text: str):
                return self.vader.polarity_scores(text)['compound']
            
            df['sentiment_score'] = df[self.column_name].apply(vader_analysis)
            df['sentiment_label'] = df['sentiment_score'].apply(
                lambda x: 
                'positive' if x > 0.05 else ('negative' if x <= -0.05 else 'neutral') #didnt know this was a syntax
            )
            print("VADER sentiment applied!")

        else:       
            def roberta_base(text: str):
                result = self.roberta_pipeline(text)[0]
                return result['label'].lower()
            df['sentiment_label'] = df[self.column_name].apply(roberta_base)
            print("Roberta base sentiment applied!")

        return df

    def keyword_extraction(self, df):
        pass

    def named_entity(self, df):
        pass

    def topic_modeling(self, df):
        pass

    def drop_nulls(self, df):
        pass

    def run(self, df):
        pass
