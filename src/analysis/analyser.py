from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from keybert import KeyBERT
import spacy
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
#MAIN THING THINK ABOUT WHERE I CAN HAVE DATA STRUCUTRE, BUT BEFORE IMPLEMENTING IT CHECK IF SOME FUNCTIONS HAVE 

class Analyser:

    def __init__(self, source, column_name):
        self.source = source
        self.column_name = column_name
        tqdm.pandas() #for progress_apply
        if self.source == "youtube":
            self.vader = SentimentIntensityAnalyzer()
        else:
            self.MODEL = f"Cloudy1225/stackoverflow-roberta-base-sentiment"
            self.roberta_pipeline = pipeline(task="sentiment-analysis", model=self.MODEL, truncation=True, max_length=512) #hard cut the model at 512 tokens, model is weird

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

        self.sentence_transformer_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.vectorizer = CountVectorizer(stop_words='english') #topic modelling was having too many the is to etc, so adding this would be better get topics
        self.cluster = HDBSCAN(metric='euclidean', cluster_selection_method='eom', min_cluster_size=100) #this is minimum documents need to form a topic.
        #verbose is for visualization, rest are self explanatory
        self.topic_model = BERTopic(language="english", embedding_model=self.sentence_transformer_model, calculate_probabilities=False, verbose=True, hdbscan_model=self.cluster, vectorizer_model=self.vectorizer)


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
                """
                each row in stackoverflow was extremely long so it took time to run(2hour+) and still it wasnt done, hence i chose the first 2000 characters in the row
                this would not really matter because the first 2000 characters would mostly give the sentiment behind it. i have used progress_apply instead of apply asw
                to see the progress of the model
                """
                result = self.roberta_pipeline(text[:2000])[0]
                return result['label'].lower()
            df['sentiment_label'] = df[self.column_name].progress_apply(roberta_base)
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
        """
        this is a straight forward process but took sm time, basically bertopic create topic clusters which
        can be later used to find using the topic label. below, topics return topic number or ids which categorize
        each topic into its own. meaning topic 1 - your_brother_your_sister etc, topic 5 - kfc_pizzahut etc. if a
        main topic id is -1 it means they cannot group it to anything basically because its meaningless
        idea is that it categorize depending on the topic on its own. topic_info variable is a dataframe. 
        topic_lookup is essentially creating a dataframe that is setting index as the Topic(which is the topic_id)
        and then getting only the Name(it removed all other columns). then this is saved in topic_label by
        looking throughou MY dataframe (topic_id) and using .map which auto matches in the topic_lookup. again
        another day, another surprise by what python is and its syntax  
        """
        batch = df[self.column_name].tolist()
        topics, _ = self.topic_model.fit_transform(batch) # 
        topic_info = self.topic_model.get_topic_info()
        df['topic_id'] = topics
        topic_lookup = topic_info.set_index("Topic")["Name"]
        df["topic_label"] = df["topic_id"].map(topic_lookup)
        return df
        
    def drop_nulls(self, df):
        return df.dropna(subset=['sentiment_label', 'keyword', 'entities', 'topic_label'])

    def run(self, df):
        sentiment = self.sentiment_analysis(df)
        print("Sentiment Analysis completed")
        keywords = self.keyword_extraction(sentiment)
        print("Keyword Extraction completed")
        entities = self.named_entity(keywords)
        print("Named Entities completed")
        topic_modelling = self.topic_modeling(entities)
        print("Topic Modeling completed")
        drop_null = self.drop_nulls(topic_modelling)
        print("Dropped nulls")
        return drop_null
