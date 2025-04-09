import argparse
import os
import logging
# Import the new crawl function and other necessary functions
from web_scrape import crawl_and_scrape, split_dom_content 
from llm_clients.hf_client import HFClient

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="AI Web Scraper CLI - Crawls depth 1 and uses Hugging Face API")
    parser.add_argument("start_url", help="The starting URL to crawl and scrape (e.g., https://example.com)")
    parser.add_argument("description", help="A description of the data to extract from each page (e.g., 'Summarize the main purpose of this page')")
    parser.add_argument("--model", default=os.getenv("HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct"), help="Hugging Face Model ID (optional, defaults to HF_MODEL_ID env var or meta-llama/Meta-Llama-3-8B-Instruct)")
    parser.add_argument("--depth", type=int, default=1, help="Crawling depth (default: 1)")

    args = parser.parse_args()

    # Ensure HF_TOKEN is set
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        logger.error("HF_TOKEN environment variable is not set. Please set it with your Hugging Face API token.")
        return

    logger.info(f"Using Hugging Face model: {args.model}")
    hf_client = HFClient(model_id=args.model, api_token=hf_token)

    # --- Crawling & Scraping ---
    logger.info(f"Starting crawl from {args.start_url} with depth {args.depth}")
    try:
        # Use the new crawl function
        scraped_data = crawl_and_scrape(args.start_url, max_depth=args.depth) 
        if not scraped_data:
            logger.error("Crawling and scraping failed or returned no content.")
            return
        logger.info(f"Crawled and scraped {len(scraped_data)} pages.")
        
    except Exception as e:
        logger.exception(f"Error during crawling/scraping: {e}")
        return

    # --- Parsing ---
    logger.info(f"Parsing content from {len(scraped_data)} pages with description: '{args.description}'")
    final_results = {}
    llm_params = None # Add parameters if needed, e.g., {"max_new_tokens": 1500}

    for url, cleaned_content in scraped_data.items():
        if cleaned_content is None:
            logger.warning(f"Skipping parsing for {url} as scraping failed.")
            final_results[url] = "Error: Scraping failed for this URL."
            continue
        
        logger.info(f"--- Parsing {url} ---")
        dom_chunks = split_dom_content(cleaned_content)
        page_parsed_results = []

        for i, chunk in enumerate(dom_chunks, start=1):
            # Construct prompt (adjust as needed for better results)
            prompt = f"Based on the following text content from {url}, extract only the information matching this description: '{args.description}'. Respond with only the extracted information, or nothing if no information matches.\n\nContent:\n{chunk}"
            logger.info(f"Processing chunk {i}/{len(dom_chunks)} for {url}...")
            try:
                response = hf_client.generate(prompt, params=llm_params)
                generated_text = hf_client.extract_generated_text(response)
                
                if generated_text:
                    page_parsed_results.append(generated_text.strip())
                    logger.info(f"Parsed chunk {i} for {url} successfully.")
                else:
                    logger.warning(f"No text extracted from chunk {i} response for {url}: {response}")
                    page_parsed_results.append("") # Append empty string if nothing found/extracted

            except Exception as e:
                error_message = f"Error processing chunk {i} for {url}: {e}"
                logger.error(error_message)
                page_parsed_results.append(f"ERROR: {error_message}")
        
        # Store the combined results for the page
        final_results[url] = "\n\n".join(filter(None, page_parsed_results))

    # --- Output ---
    print("\n--- Crawling and Parsing Complete ---")
    for url, result_text in final_results.items():
        print(f"\n=== Results for: {url} ===")
        if result_text:
            print(result_text)
        else:
            print("(No relevant information extracted)")

if __name__ == "__main__":
    main()
