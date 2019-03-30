import json
from unittest.mock import Mock, patch

from reverse_youtube_playlist import (
    reverse_youtube_playlist,
    build_playlist_url,
    get_video_ids_from_playlist,
    YOUTUBE_KEY
)


@patch('reverse_youtube_playlist.build_playlist_url')
@patch('reverse_youtube_playlist.get_video_ids_from_playlist')
def test_reverse_youtube_playlist(get_video_ids, build_playlist):
    get_video_ids.return_value = [1, 2, 3]
    reverse_youtube_playlist(
        'http://youtube.com/?list=foobar'
    )
    build_playlist.assert_called_once_with([3, 2, 1])

def test_build_playlist_url():
    videos_ids = ['foo', 'bar', 'foo', 'bar', 'foo']
    expected_url = (
        "https://www.youtube.com/watch_videos?video_ids=foo,bar,foo,bar,foo"
    )

    builded_correctly = build_playlist_url(videos_ids) == expected_url
    assert(builded_correctly)

def test_get_video_ids_from_playlist(requests_mock):
    api_url = (
        'https://www.googleapis.com/youtube/v3/playlistItems?'
        'part=snippet&maxResults=50'
        '&playlistId=PLJ85jmdKU96JIZjV6Rpbc1ZidaClDdnpF&key=foo'
    )

    with open('fixture.json', 'r') as fixture:
        requests_mock.get(
            api_url,
            json=json.load(fixture)
        )
    YOUTUBE_KEY = 'foo'

    playlist_url = 'https://www.youtube.com/watch?v=UVlAYHsIB2g&list=PLJ85jmdKU96JIZjV6Rpbc1ZidaClDdnpF'
    video_ids = get_video_ids_from_playlist(playlist_url)
    assert(video_ids == ['bar-foo-video-id', 'foo-bar-video-id'])
    