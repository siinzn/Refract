from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from keybert import KeyBERT
import spacy
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
        for spacy, i used en_core_web_md to meet at the middle, en_core_web_sm was not good for my dataset, and larger 
        models were not needed, so i stuck with this. i had to add custom entities(claude recommended) since
        the model may not be know certain words, also note for self, these models are heavy and if defined in the function
        they would be run on every iteration, thatd slowed down the whole process.
        """
        self.nlp = spacy.load('en_core_web_md')
        self.ruler = self.nlp.add_pipe("entity_ruler", before="ner")
        TECH_ENTITIES = [
        "C++", "C", "Rust", "Python", "Go", "Assembly", "Fortran",
        "LLVM", "GCC", "Clang", "MSVC", "ICC",
        "Linux", "Windows", "macOS", "Unix", "POSIX",
        "RAII", "vtable", "syscall", "mmap", "malloc", "free",
        "OpenMP", "pthreads", "MPI",
        "CMake", "Make", "Ninja",
        "valgrind", "sanitizer", "gdb", "perf",
        "STL", "Boost", "libc", "glibc",
        "x86", "ARM", "RISC-V",
        "Docker", "Git",
        "undefined behavior", "memory leak", "dangling pointer",
        "smart pointer", "borrow checker", "garbage collection",
        "stack overflow", "heap allocation", "cache miss"
        ]
        patterns = [{"label": "TECH", "pattern": entity} for entity in TECH_ENTITIES]
        self.ruler.add_patterns(patterns)

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
        """
        the same as keywords, batching is more efficient than passing row by row. spacy gives a weird output tbh, 
        im not 100% about the var entities, i know what it does but dont really get the syntax. essentially,
        nlp.pipe(bacth) returns [Doc1, Doc2, Doc3...] this list is looped through -> doc, and then inside each doc ->
        loop through the entities, inside each entities extract the ent.text. hella weird syntax but this is apparently
        the best way to get the best performance. there is ai involvment in that line of code :(
        """
        batch = df[self.column_name].tolist()
        entities = [[ent.text for ent in doc.ents] for doc in self.nlp.pipe(batch)]
        df['entities'] = entities
        return df

    def topic_modeling(self, df):
        pass

    def drop_nulls(self, df):
        pass

    def run(self, df):
        sentiment = self.sentiment_analysis(df)
        keywords = self.keyword_extraction(sentiment)
        entities = self.named_entity(keywords)
