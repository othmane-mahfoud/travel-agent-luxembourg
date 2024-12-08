import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.visitluxembourg.com/experience-luxembourg/festivals-events"

def fetch_event_details(event_url):
    if event_url == "None":
        return "None", "None"
    response = requests.get(event_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    category_elements = soup.find_all("span", class_="baseArticle__title__tags__item")

    if len(category_elements) > 1:
        category = category_elements[1].text.strip()  
    else:
        category = "None"
    
    base_article_div = soup.find('div', class_='baseArticle__text')
    if base_article_div:
       for tag in base_article_div(['strong', 'em', 'img', 'style', 'script']):
           tag.decompose()
    
       description = base_article_div.get_text(separator=" ", strip=True)
    
       description = description.split('<style>')[0] 
    
    
    return category, description

def scrape_page(url, events_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    event_wrappers = soup.find_all("div", class_="listItem__text")
    for event in event_wrappers:
        title_element = event.find("h5", class_="listItem__title__header")
        title = title_element.text.strip() if title_element else "None"

        start_date_element = event.find("small", string=lambda text: text and "When?" in text)
        start_date = start_date_element.text.replace("When?", "").strip() if start_date_element else "None"

        last_event_date_element = event.find("small", string=lambda text: text and "Last event date on" in text)
        end_date = last_event_date_element.text.replace("Last event date on", "").strip() if last_event_date_element else "None"

        location_element = event.find("small", string=lambda text: text and "Where?" in text)
        location = location_element.text.replace("Where?", "").strip() if location_element else "None"

        url_element = event.find("a", class_="listItem__main__fakelink")
        event_url = url_element["href"] if url_element else "None"

        category, description = fetch_event_details(event_url)

        events_list.append({
            "Event Name": title,
            "Image URL": None,
            "Start Date": f"{start_date.split(".")[2]}-{start_date.split(".")[1]}-{start_date.split(".")[0]}",
            "Start Time": "18:30:00",
            "Genre": category,
            "Subgenre": category,
            "Venue": location,
            "City": location.split(" ")[-1] if location.split(" ")[-1][-1] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] else "Luxembourg",
            "Address": location,
            "Description": description
        })

def scrape_all_pages(base_url, total_pages):
    events = []
    for page in range(1, total_pages + 1):
        current_url = f"{base_url}?page={page}"
        scrape_page(current_url, events)
    return events

if __name__ == "__main__":
    total_pages = 30  
    all_events = scrape_all_pages(base_url, total_pages)
    all_events_df = pd.DataFrame(all_events)
    all_events_df.to_csv("data/scraping_events.csv", index=False)