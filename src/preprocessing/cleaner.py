
# this is to clean up each comment since they will be noisy with timestamps, emojis, mentions etc
# or in case of stackoverflow - look into it
from langdetect import detect, LangDetectException
import html
import re

class Cleaner:

    def __init__(self, source, column_name, min_words):
        self.source = source
        self.column_name = column_name
        self.min_words = min_words
    
    def remove_duplicates(self, df):
        #drop duplicates function from pandas already have a hash set so the look up is pretty fast
        return df.drop_duplicates(subset=[self.column_name])
         
    def filter_length(self, df): 
        """
        what this basically does is takes each column, then str.split() splits the sentence in each sentence as
        words this creates a list apparently IDK HOW and then str.len checks if the list length is more than min words
        if it is then it returns True so only those rows get returned from the function 
        """
        return df[df[self.column_name].str.split().str.len() >= self.min_words]

    def filter_language(self, df): 
        """
        So first we check if the text is in ascii, this would mostly be english, and then if it is not in ascii we use
        langdetect. 

        Below code is ai helped code(i coudlnt understand what i was doing wrong) its basically using a helper function
        as in true or false, and then uses .apply to filter out which one is english and which one isnt
        """
        def is_english(text: str):
            if text.isascii():
                return True
            else: 
                try: 
                    detect(text) == 'en' 
                except LangDetectException: 
                    return False 

        mask = df[self.column_name].apply(is_english)
        return df[mask]

    def text_clean(self, df):
        """
        a bit of late knowlege, .apply function is kind of like a loop i knew it before but i realised it now.
        in this we basically remove all unwanted or noise, for example &amp; has to be changed into &, remove links, 
        mentions, emojis if any. the regex are ai idk regex bruha
        """
        df = df.copy() #this creates a safe copy for pandas to work w 
        df['text_clean'] = df[self.column_name]
        df['text_clean'] = df['text_clean'].apply(html.unescape)
        df['text_clean'] = df['text_clean'].str.replace(r'https?://\S+|www\.\S+', '', regex=True)  # to remove urls http or www
        df['text_clean'] = df['text_clean'].str.replace(r'@\w+', '', regex=True)  # to remove mentions
        df['text_clean'] = df['text_clean'].str.replace(r'[\u2028\u2029\u202f]', ' ', regex=True)  # to remove uni code
        df['text_clean'] = df['text_clean'].str.replace(r'\s+', ' ', regex=True).str.strip()  # to remove whitespace

        df['source'] = self.source
        df['word_count'] = df['text_clean'].str.split().str.len()
        return df
        
    def run(self, df):
        df_no_duplicates = self.remove_duplicates(df)
        df_length_filtered = self.filter_length(df_no_duplicates)
        df_lang_filtered = self.filter_language(df_length_filtered)
        df_clean_text = self.text_clean(df_lang_filtered)
        return df_clean_text;
