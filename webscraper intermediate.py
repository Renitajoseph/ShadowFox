import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# --- Add Flask imports and app setup ---
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
URL = "https://shadowfox.in/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
OUTPUT_FILE = 'scraped_data.csv'
MAX_RETRIES = 3
TIMEOUT = 10

def scrape_website():
    """Main function to scrape website data"""
    try:
        # Fetch webpage with error handling
        html_content = fetch_webpage(URL)
        
        # Parse and extract data
        soup = BeautifulSoup(html_content, 'html.parser')
        scraped_data = extract_data(soup)
        
        # Save data
        save_to_csv(scraped_data)
        print(f"Successfully scraped {len(scraped_data)} items")
        
    except Exception as e:
        print(f"Scraping failed: {str(e)}")

def fetch_webpage(url):
    """Fetch webpage content with error handling"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=TIMEOUT
            )
            response.raise_for_status()
            
            # Check content type
            if 'text/html' not in response.headers.get('Content-Type', ''):
                raise ValueError("Non-HTML content received")
                
            return response.text
        
        except (requests.RequestException, ValueError) as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                sleep_time = random.uniform(2, 5)
                print(f"Retrying in {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
    
    raise Exception(f"Failed to fetch webpage after {MAX_RETRIES} attempts")

def extract_data(soup):
    """Extract data from BeautifulSoup object"""
    data = []
    
    try:
        # Identify containers - adjust selector based on actual page structure
        containers = soup.select('div.post-item')  # Example selector
        
        for container in containers:
            try:
                # Extract elements - update selectors per ShadowFox structure
                title = container.select_one('h2 a').text.strip()
                link = container.select_one('h2 a')['href'].strip()
                summary = container.select_one('p').text.strip() if container.select_one('p') else "N/A"
                
                data.append({
                    'title': title,
                    'link': link,
                    'summary': summary
                })
                
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Extraction error: {str(e)}")
    
    return data

def save_to_csv(data):
    """Save scraped data to CSV file"""
    if not data:
        print("No data to save")
        return
        
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'link', 'summary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in data:
                writer.writerow(item)
                
    except IOError as e:
        print(f"File save error: {str(e)}")

@app.route('/scrape', methods=['POST'])
def scrape_api():
    """
    API endpoint to scrape website based on frontend request.
    Expects JSON: { "url": "...", "data_type": "...", "output_format": "..." }
    """
    data = request.get_json()
    url = data.get('url', 'https://shadowfox.in/')
    # data_type and output_format can be used for advanced logic if needed
    try:
        html_content = fetch_webpage(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        scraped_data = extract_data(soup)
        return jsonify({'success': True, 'results': scraped_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def webscraper_frontend():
    return render_template('webscraper frontend.html')

if __name__ == "__main__":
    # To run as both script and Flask app
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'flask':
        app.run(debug=True)
    else:
        scrape_website()