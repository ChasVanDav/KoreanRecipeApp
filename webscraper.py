import requests
from bs4 import BeautifulSoup

def get_subheaders():
    url = 'https://www.cnn.com/travel/article/best-korean-dishes/index.html'
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find all subheaders
    subheaders = soup.find_all(class_="subheader inline-placeholder")

    subheader_texts = []  
    content_texts = []  

    for subheader in subheaders:
        subheader_text = subheader.get_text(strip=True)  # Extract subheader text
        subheader_texts.append(subheader_text)

        # Find related paragraph(s) until the next subheader
        content_paragraphs = []
        for sibling in subheader.find_next_siblings():
            if sibling in subheaders:  # Stop when next subheader appears
                break
            if sibling.name == "p":  # Collect paragraph texts
                content_paragraphs.append(sibling.get_text(strip=True))

        # Combine paragraphs into one string and store
        content_texts.append(" ".join(content_paragraphs) if content_paragraphs else "No description available.")

    return subheader_texts, content_texts

