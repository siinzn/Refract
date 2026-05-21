from src.collection.youtube import youtube 
import pandas as pd
import json
from pathlib import Path 
from googleapiclient.errors import HttpError

def getcomments(video):
    response = youtube.commentThreads().list(
      part="snippet",
      videoId=video,
      order="time",
      maxResults=100
    ).execute()

    comments = []
    #comment_count = 0

    for item in response['items']:
        #if(comment_count >= 500):
            #break
        #comment_count += 1
        #similar to video, comments are nested. it has an item -> snipper, which has a top level and inside that is another snippet of actual text strings
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['likeCount'],
            comment['textOriginal'],
            comment['videoId'],
      ])

    print("step 1")
    while(True):
        try:
            nextPageToken = response['nextPageToken']
        except KeyError:
            break
        
        response = youtube.commentThreads().list(
            part="snippet",
            videoId = video,
            order="time",
            maxResults = 100,
            pageToken = nextPageToken
        ).execute()

        for item in response ['items']:
            #if(comment_count >= 500):
                #break
            #comment_count += 1
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textOriginal'],
                comment['videoId'],
            ])    
    print("step 2")
    df = pd.DataFrame(
        comments,
        columns=[
            'author', 
            'updated_at', 
            'like_count', 
            'text',
            'video_id',
        ]
    )
    print("step 3")
    return df;       

script_dir = Path(__file__).parent
root_dir = script_dir.parent.parent
input_file_path = root_dir / "data" / "videoIds" / "videos_final.json"
#my final data is called comments_final.csv. this is purely to save phases of data
output_file_path = root_dir / "data" / "raw" / "comments.csv"

with open(input_file_path, "r", encoding="utf-8") as vd:
    videoIds = json.load(vd)

dfs = []

for video in videoIds:
    videoId = video.get('video_id')
    try:
        comment_df = getcomments(videoId)
        print(f"Comments extracted for : {videoId}")
        dfs.append(comment_df)
    except HttpError as e:
        print(f"Googel API Error : {e}")
    except Exception as e:
        print(f"Unexpected error : {e}")

    
if dfs:
    main_df = pd.concat(dfs, ignore_index=True)
    main_df.to_csv(output_file_path, index=False, encoding="utf-8")
    print(f"Got comments({len(main_df)})")




