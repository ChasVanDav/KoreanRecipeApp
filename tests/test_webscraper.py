import unittest
from webscraper import get_subheaders
import requests_mock

class TestWebScraper(unittest.TestCase):
    
    def test_get_subheaders_with_missing_content(self):
        # URL for the CNN page
        url = 'https://www.cnn.com/travel/article/best-korean-dishes/index.html'
        
        # Mock the HTML content returned from the web
        mock_html = """
        <html>
            <body>
                <h2 class="subheader inline-placeholder">Bibimbap</h2>
                <h2 class="subheader inline-placeholder">Kimchi</h2>
                <h2 class="subheader inline-placeholder">Bulgogi</h2>
            </body>
        </html>
        """
        
        # Mock the HTTP GET request
        with requests_mock.Mocker() as mock:
            mock.get(url, text=mock_html)
            
            # Call the function and unpack values correctly
            subheaders, content_texts = get_subheaders()
            
            # Check that the missing content is replaced with default
            content_texts = [content if content else "No description available." for content in content_texts]

            # Verify the returned subheaders
            self.assertEqual(subheaders, ['Bibimbap', 'Kimchi', 'Bulgogi'])
            
            # Ensure the content is the default value
            self.assertEqual(content_texts, [
                "No description available.",
                "No description available.",
                "No description available."
            ])

if __name__ == '__main__':
    unittest.main()




