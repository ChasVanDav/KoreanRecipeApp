import unittest
from unittest.mock import patch
import requests
from app import search_youtube

class TestYouTubeAPI(unittest.TestCase):

    @patch('requests.get')
    def test_search_youtube(self, mock_get):
        # define the mock response based on the real API output
        mock_response = {
            "kind": "youtube#searchListResponse",
            "etag": "cXs_uzDbdsncDnA5RitI7N8YHB0",
            "nextPageToken": "CAUQAA",
            "regionCode": "US",
            "pageInfo": {
                "totalResults": 1000000,
                "resultsPerPage": 5
            },
            "items": [
                {
                    "kind": "youtube#searchResult",
                    "etag": "T-ohqTUJQ4oewOmyaHmpChSaPTA",
                    "id": {
                        "kind": "youtube#video",
                        "videoId": "eh6KRZIMyZo"
                    },
                    "snippet": {
                        "publishedAt": "2022-06-18T14:30:08Z",
                        "channelId": "UCKm-azHviA02KfpUCSWoFYQ",
                        "title": "How to make THE EASIEST Korean Shaved Ice 🍧 (Bingsu 빙수) AT HOME!",
                        "description": "Korean Shaved Ice is something I always enjoyed in the Spring and Summer in Korea~! The frozen milk was still a bit thick here ...",
                        "thumbnails": {
                            "default": {"url": "https://i.ytimg.com/vi/eh6KRZIMyZo/default.jpg"},
                            "medium": {"url": "https://i.ytimg.com/vi/eh6KRZIMyZo/mqdefault.jpg"},
                            "high": {"url": "https://i.ytimg.com/vi/eh6KRZIMyZo/hqdefault.jpg"}
                        },
                        "channelTitle": "JENtendo",
                        "liveBroadcastContent": "none",
                        "publishTime": "2022-06-18T14:30:08Z"
                    }
                }
            ]
        }

        # mock response for video statistics
        mock_stats_response = {
            "items": [
                {
                    "statistics": {
                        "viewCount": "10000"
                    }
                }
            ]
        }

        # mock the `requests.get` method to return the mock response
        def mock_requests_get(url, *args, **kwargs):
            if "search" in url:
                return mock_get_response(mock_response)
            elif "videos" in url:
                return mock_get_response(mock_stats_response)
        
        def mock_get_response(data):
            mock_resp = unittest.mock.Mock()
            mock_resp.json.return_value = data
            return mock_resp

        mock_get.side_effect = mock_requests_get

        # call the function 
        print("Calling search_youtube with query 'Bingsu'")
        video_id, video_url, video_title, video_metadata = search_youtube('Bingsu')

        # print results
        print(f"Video ID: {video_id}")
        print(f"Video URL: {video_url}")
        print(f"Video Title: {video_title}")
        print(f"Video Metadata: {video_metadata}")

        #assertions
        self.assertEqual(video_id, "eh6KRZIMyZo")
        self.assertEqual(video_url, "https://www.youtube.com/watch?v=eh6KRZIMyZo")
        self.assertEqual(video_title, "How to make THE EASIEST Korean Shaved Ice 🍧 (Bingsu 빙수) AT HOME!")
        self.assertEqual(video_metadata['channelTitle'], "JENtendo")
        self.assertEqual(video_metadata['viewCount'], '10000')  
        
if __name__ == '__main__':
    unittest.main()








