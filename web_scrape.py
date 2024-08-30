import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def scrape_website(website):
    print("Lauching Chrome browser...")
    
    chrome_driver_path = "./chromedriver" #Specify where chrome driver is
    options = webdriver.ChromeOptions() #Specify how the crhome driver should operate (e.g. run headless, ignore images, etc)
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        driver.get(website) #use web driver to go to specific website
        print("Page loaded...")
        html = driver.page_source
        
        return html
    finally:
        driver.quit()
        
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser") #parse content
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return ""
    
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    for script_or_style in soup(["script", "style"]): #look inside parsed content and remove script or style
        script_or_style.extract()
        
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip() #remove all \n that are not seperating text and remove trailing spaces
        )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000): #split content for token limit of llm
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    