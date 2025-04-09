import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

def _get_driver():
    """Initializes and returns a Selenium WebDriver."""
    logger.debug("Initializing Chrome driver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    try:
        driver = webdriver.Chrome(options=options)
        logger.debug("Chrome driver initialized.")
        return driver
    except Exception as e:
        logger.exception(f"Failed to initialize Chrome driver: {e}")
        raise

def scrape_single_page(driver, url):
    """Scrapes HTML content from a single URL using a provided driver instance."""
    logger.info(f"Scraping URL: {url}")
    try:
        driver.get(url)
        logger.info(f"Page loaded: {url}")
        # Optional: Add wait condition if needed for dynamic content
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        return html
    except Exception as e:
        logger.error(f"Failed to scrape {url}: {e}")
        return None

def find_internal_links(base_url, html_content):
    """Finds all internal links on a page."""
    links = set()
    soup = BeautifulSoup(html_content, "html.parser")
    base_netloc = urlparse(base_url).netloc

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Join relative URLs with the base URL
        full_url = urljoin(base_url, href)
        # Parse the full URL
        parsed_url = urlparse(full_url)
        
        # Check if it's an HTTP/HTTPS link and belongs to the same domain
        if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc == base_netloc:
            # Optional: Ignore fragment identifiers (#)
            clean_url = parsed_url._replace(fragment="").geturl()
            links.add(clean_url)
            
    return links

def crawl_and_scrape(start_url, max_depth=1):
    """
    Crawls a website starting from start_url up to max_depth and scrapes content.
    Returns a dictionary mapping URL to its cleaned text content.
    """
    scraped_content = {}
    urls_to_visit = {start_url}
    visited_urls = set()
    
    driver = _get_driver() # Initialize driver once

    try:
        for depth in range(max_depth + 1):
            current_level_urls = list(urls_to_visit)
            urls_to_visit = set() # Prepare for next level
            
            logger.info(f"--- Crawling Depth {depth} ({len(current_level_urls)} URLs) ---")

            for url in current_level_urls:
                if url in visited_urls:
                    continue
                
                visited_urls.add(url)
                html = scrape_single_page(driver, url)

                if html:
                    body_content = extract_body_content(html)
                    cleaned_text = clean_body_content(body_content)
                    scraped_content[url] = cleaned_text
                    logger.info(f"Stored content for {url} (Length: {len(cleaned_text)})")

                    # Find links for the next level if depth allows
                    if depth < max_depth:
                        internal_links = find_internal_links(url, html)
                        new_links = internal_links - visited_urls
                        urls_to_visit.update(new_links)
                        logger.debug(f"Found {len(new_links)} new internal links on {url}")
                else:
                     scraped_content[url] = None # Mark as failed/empty
            
            if not urls_to_visit: # Stop if no new URLs found
                 logger.info("No new URLs found to visit at next depth.")
                 break
                 
    finally:
        logger.info("Closing Chrome driver.")
        driver.quit()
        
    return scraped_content
        
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
