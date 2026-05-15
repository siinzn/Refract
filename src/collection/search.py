from ..collection.youtube import youtube 
from itertools import batched
from googleapiclient.errors import HttpError
import json
from pathlib import Path 

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
    try:
        request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=10,
        relevanceLanguage="en",
        videoDuration="any",
        order="relevance"
        ).execute()
        return request
    except HttpError as e:
        print(f"Googel API Error for {query} : {e}")
    except Exception as e:
        print(f"Unexpected error : {e}")

video_ids = []

for query in search_queries:
    #basically go into the result of get_yt_vids list and grab only items from that list 
    #(the whole result of the function return multiple details but we only want items) and then
    #in that item from the result of function, go into id -> then into videoId (there are multple ids but we want videoId)
    results = get_yt_vids(query)
    if results:
        video_ids += [item['id']['videoId'] for item in results['items']]

def get_video_stats(video_ids):
    stats = []
    #batched lets me batch 70 ids into 50 so the api doesnt crash. 50 is the limit
    for chunk in batched(video_ids, 50):
        try:
            response = youtube.videos().list(
            #snippet has title, desc, channelId, channelTitle, categoryId etc
            #statistics has viewCount, likeCount, commentCount, favoriteCount
            part="snippet,statistics",
            id=",".join(chunk)
            ).execute()
            #extend adds elements individually rather than append which adds all at once
            stats.extend(response.get('items', []))
        except HttpError as e:
            print(f"Googel API Error : {e}")
        except Exception as e:
            print(f"Unexpected error : {e}")
    return stats

# to prevent duplicate ids so we dont search same video and waste token
video_ids = list(set(video_ids))
filtered_vids = []

for vid in get_video_stats(video_ids):
    stats = vid.get('statistics', {})
    comment_count = int(stats.get('commentCount', 0))
    view_count = int(stats.get('viewCount', 0))
    if comment_count >= 200 and view_count >= 10000:
        filtered_vids.append(vid) 

filtered_vids.sort(key=lambda item: int(item.get("statistics", {}).get("commentCount", 0)), reverse=True)
top20_vids = filtered_vids[:20]


videos = []
for vid in top20_vids:
    video_entry = {
        "video_id": vid['id'],
        "title": vid['snippet']['title'],
        "channel_name": vid['snippet']['channelTitle'],
        "view_count": vid['statistics']['viewCount'],
        "comment_count": vid['statistics']["commentCount"],
        "video_url": f"https://youtube.com/watch?v={vid['id']}"
    }
    videos.append(video_entry)


script_dir = Path(__file__).parent
root_dir = script_dir.parent.parent
output_file_path = root_dir / "data" / "raw" / "videos.json"

with open(output_file_path, "w") as f:
    json.dump(videos, f, indent=2)

print(f"Added {len(videos)} vids")