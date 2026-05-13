from ..collection.youtube import youtube 

search_queries = [
    "Modern C++",
    "Operating Systems",
    "C++ systems programming",
    "memory management C++",
    "multithreading C++ concurrency",
    "performance optimization C++",
    "operating systems low level programming"
]

def get_yt_vids(query):
    request = youtube.search().list(
    part="snippet",
    q=query,
    type="video",
    maxResults=10,
    relevanceLanguage="en",
    videoDuration="any",
    order="relevance"
    )
    return request.execute()
    
    
for query in search_queries:
    get_yt_vids(query)



