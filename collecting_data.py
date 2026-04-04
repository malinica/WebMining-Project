from googleapiclient.discovery import build
import pandas as pd
import time
import re
from langdetect import detect
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=api_key)

recent_videos = [
    "[GOING SEVENTEEN SPECIAL] 2026 고잉 긴급 회의 (Agenda: GOING SEVENTEEN 2026)",
    "[GOING SEVENTEEN] EP.149 마피아불 #2 (Mafiapoly #2)",
    "[GOING SEVENTEEN] EP.148 마피아불 #1 (Mafiapoly #1)",
    "[GOING SEVENTEEN] EP.147 Chat, Chat #2",
    "[GOING SEVENTEEN] EP.146 Chat, Chat #1",
    "[GOING SEVENTEEN] EP.145 빠퇴 #2 (Let’s Go Home #2)",
    "[GOING SEVENTEEN] EP.144 빠퇴 #1 (Let’s Go Home #1)",
    "[GOING SEVENTEEN] EP.143 무죄 추정 #2 (Innocent Until Proven Guilty #2)",
    "[GOING SEVENTEEN] EP.142 무죄 추정 #1 (Innocent Until Proven Guilty #1)",
    "[GOING SEVENTEEN] EP.139 GOOD OFFER 2 #2"
]

popular_videos = [
    "[GOING SEVENTEEN 2020] EP.27 술래잡기 #1 (The Tag #1)",
    "[GOING SEVENTEEN] EP.32 순응특집 단짝 #2 (Best Friends #2)",
    "[GOING SEVENTEEN 2020] EP.44 TTT #1 (Hyperrealism Ver.)",
    "[GOING SEVENTEEN] EP.31 순응특집 단짝 #1 (Best Friends #1)",
    "[GOING SEVENTEEN 2020] EP.45 TTT #2 (Hyperrealism Ver.)",
    "[GOING SEVENTEEN] EP.18 TTT에 빠지다 #1 (Dive into TTT #1)",
    "[GOING SEVENTEEN] EP.24 부족오락관 #2 (Tribal Games #2)",
    "[GOING SEVENTEEN 2020] EP.40 돈't Lie Ⅱ #1 (Don't Lie Ⅱ #1)",
    "[GOING SEVENTEEN 2020] EP.25 디에잇과 12인의 그림자 #1 (THE 8 and the 12 Shadows #1)",
    "[GOING SEVENTEEN 2020] EP.23 드립 : 세븐틴 갓 탤런트 #1 (Ad-lib : Seventeen's got Talent #1)"
]


video_data = []

for title in recent_videos:
    video_data.append({"title": title, "type": "recent"})

for title in popular_videos:
    video_data.append({"title": title, "type": "popular"})


def get_video_id(title):
    request = youtube.search().list(
        part="snippet",
        q=title,
        maxResults=1,
        type="video"
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["id"]["videoId"]
    return None


def get_comments(video_id):
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    while request:
        response = request.execute()

        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            text = snippet["textDisplay"]

            try:
                if detect(text) != "en":
                    continue
            except:
                continue

            comments.append({
                "video_id": video_id,
                "text": text,
                "likes": snippet["likeCount"],
                "date": snippet["publishedAt"]
            })

        request = youtube.commentThreads().list_next(request, response)

    return comments


all_comments = []

for video in video_data:
    title = video["title"]
    type = video["type"]

    print(f"Looking for a video: {title}")
    video_id = get_video_id(title)

    if not video_id:
        print("Not found")
        continue

    print(f"Downloading comments for: {video_id}")

    comments = get_comments(video_id)

    for c in comments:
        c["video_title"] = title
        c["type"] = type

    all_comments.extend(comments)

    print(f"All comments: {len(all_comments)}")

    time.sleep(1)  


df = pd.DataFrame(all_comments)
df.to_csv("going_seventeen_comments.csv", index=False, encoding="utf-8-sig")

print("DONE")