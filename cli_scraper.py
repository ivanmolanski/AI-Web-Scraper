import argparse
import os
import logging
from web_scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from llm_clients.hf_client import HFClient

# Basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="AI Web Scraper CLI - Uses Hugging Face API")
    parser.add_argument("url", help="The full URL of the website to scrape (e.g., https://example.com)")
    parser.add_argument("description", help="A description of the data to extract (e.g., 'Extract the main article title and author')")
    parser.add_argument("--model", default=os.getenv("HF_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct"), help="Hugging Face Model ID (optional, defaults to HF_MODEL_ID env var or meta-llama/Meta-Llama-3-8B-Instruct)")
    
    args = parser.parse_args()

    # Ensure HF_TOKEN is set
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        logger.error("HF_TOKEN environment variable is not set. Please set it with your Hugging Face API token.")
        return

    logger.info(f"Using Hugging Face model: {args.model}")
    hf_client = HFClient(model_id=args.model, api_token=hf_token)

    # --- Scraping ---
    logger.info(f"Scraping URL: {args.url}")
    try:
        html_result = scrape_website(args.url)
        if not html_result:
            logger.error("Scraping failed or returned empty content.")
            return
        
        body_content = extract_body_content(html_result)
        cleaned_content = clean_body_content(body_content)
        logger.info(f"Scraped and cleaned content (length: {len(cleaned_content)} characters).")
        
    except Exception as e:
        logger.exception(f"Error during scraping: {e}")
        return

    # --- Parsing ---
    logger.info(f"Parsing content with description: '{args.description}'")
    dom_chunks = split_dom_content(cleaned_content)
    parsed_results = []
    llm_params = None # Add parameters if needed, e.g., {"max_new_tokens": 1500}

    for i, chunk in enumerate(dom_chunks, start=1):
        prompt = f"Based on the following text content, extract only the information matching this description: '{args.description}'. Respond with only the extracted information, or nothing if no information matches.\n\nContent:\n{chunk}"
        logger.info(f"Processing chunk {i}/{len(dom_chunks)}...")
        try:
            response = hf_client.generate(prompt, params=llm_params)
            generated_text = hf_client.extract_generated_text(response)
            
            if generated_text:
                parsed_results.append(generated_text.strip())
                logger.info(f"Parsed chunk {i} successfully.")
            else:
                logger.warning(f"No text extracted from chunk {i} response: {response}")
                parsed_results.append("") # Append empty string if nothing found/extracted

        except Exception as e:
            error_message = f"Error processing chunk {i}: {e}"
            logger.error(error_message)
            parsed_results.append(f"ERROR: {error_message}")

    result_text = "\n\n".join(filter(None, parsed_results))
    
    # --- Output ---
    print("\n--- Parsing Complete ---")
    print("\nParsed Result:")
    print(result_text)

if __name__ == "__main__":
    main()
