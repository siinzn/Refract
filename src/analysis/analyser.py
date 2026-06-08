from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from keybert import KeyBERT
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
        
        self.kw_model = KeyBERT()

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
        """
        when i apply keybert i get a list of tuples, and thats sorted by score. i take the top 5 using top_n=5, but how do i save it? the column keywords is going to be a list
        but till now i didnt save anything in a list for columns using df[keywords], okay so whatever the fucntion returns is stored in keyword column, basically i just return 
        a list from keybert and then a list will be stored in the column, but if keybert function returns a string, string will be stored in the column, HELLA WEIRD LANGUAGE
        """
        batch = df[self.column_name].tolist()
        keywords = self.kw_model.extract_keywords(batch, keyphrase_ngram_range=(1,2), stop_words="english",top_n=5)
        keywords_extracted = [[item[0] for item in kw_list] for kw_list in keywords]
        df['keyword'] = keywords_extracted
        return df
        
    def named_entity(self, df):
        pass

    def topic_modeling(self, df):
        pass

    def drop_nulls(self, df):
        pass

    def run(self, df):
        sentiment = self.sentiment_analysis(df)
        keywords = self.keyword_extraction(sentiment)
