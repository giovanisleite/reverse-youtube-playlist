from decouple import config
import requests
from urllib import parse

YOUTUBE_KEY = config('YOUTUBE_API_KEY')

def reverse_youtube_playlist(playlist_url):
    video_ids = get_video_ids_from_playlist(playlist_url)
    video_ids_reversed = video_ids[::-1]
    return build_playlist_url(video_ids_reversed)

def build_playlist_url(video_ids):
    new_playlist_url = (
        f"https://www.youtube.com/watch_videos?video_ids={','.join(video_ids)}"
    )
    return new_playlist_url

def get_video_ids_from_playlist(playlist_url):
    playlist_id = extract_playlist_id(playlist_url)
    playlist_items = get_playlist_information(playlist_id)

    video_ids = []
    while(True):
        video_ids = video_ids + extract_video_ids_from_response(playlist_items)
        next_page_token = playlist_items.get('nextPageToken', False)
        if not next_page_token:
            break
        playlist_items = get_playlist_information(playlist_id, next_page_token)
    return video_ids

def extract_playlist_id(playlist_url):
    return parse.parse_qs(parse.urlparse(playlist_url).query)['list'][0]

def get_playlist_information(playlist_id, page_token=None):
    page_token_parameter = f'?pageToken={page_token}' if page_token else ''

    api_url = (
        'https://www.googleapis.com/youtube/v3/playlistItems?'
        'part=snippet&maxResults=50'
        f'&playlistId={playlist_id}&key={YOUTUBE_KEY}{page_token_parameter}'
    )

    return requests.get(api_url).json()

def extract_video_ids_from_response(response):
    return [
        video['snippet']['resourceId']['videoId']
        for video in response['items']
        if video['snippet']['title'] != 'Private video'
    ]
