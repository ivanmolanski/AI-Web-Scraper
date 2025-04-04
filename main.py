import streamlit as st
import streamlit as st
from web_scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
# from parse import parse_with_ollama # No longer needed
from llm_clients.hf_client import HFClient # Import HFClient

# Initialize HFClient - replace with config if needed
# Assumes HF_TOKEN is set as an environment variable
hf_client = HFClient(model_id="meta-llama/Meta-Llama-3-8B-Instruct") 

#Contains UI
st.title("AI Web Scraper")
url = st.text_input("Enter a website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")

    # Ensure the URL has a scheme
    if url and not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        st.info(f"URL modified to: {url}")  # Inform user about the change

    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content  # store data in session to use it later

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)


if "dom_content" in st.session_state:
    parse_decription = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_decription:
            st.write("Parsing the content")

            dom_chunks = split_dom_content(st.session_state.dom_content)
            # result = parse_with_ollama(dom_chunks, parse_decription) # Replaced with HFClient call
            parsed_results = []
            # TODO: Add LLM parameters from config if needed
            # llm_params = config.get("llm_generation_parameters") 
            llm_params = None # Using defaults for now

            for i, chunk in enumerate(dom_chunks, start=1):
                # Construct a prompt suitable for the HF model
                # This might need refinement based on the model's expected input format
                # Using a simple instruction format for now
                prompt = f"Based on the following text content, extract only the information matching this description: '{parse_decription}'. Respond with only the extracted information, or nothing if no information matches.\n\nContent:\n{chunk}"
                
                st.write(f"Processing chunk {i}/{len(dom_chunks)}...") # Show progress
                try:
                    response = hf_client.generate(prompt, params=llm_params) # Use HFClient to generate
                    generated_text = hf_client.extract_generated_text(response) # Extract text from HF response
                    
                    if generated_text:
                        parsed_results.append(generated_text.strip())
                        print(f"Parsed chunk {i} of {len(dom_chunks)}")
                    else:
                        # Log warning but don't necessarily treat as error, might just be no data found
                        print(f"No text extracted from chunk {i} response: {response}")
                        parsed_results.append("") # Append empty string if nothing found/extracted

                except Exception as e:
                    error_message = f"Error processing chunk {i}: {e}"
                    st.error(error_message)
                    print(error_message)
                    parsed_results.append(f"ERROR: {error_message}") # Append error message to results
            
            result_text = "\n\n".join(filter(None, parsed_results)) # Join non-empty results with double newline
            st.write("--- Parsing Complete ---")
            st.text_area("Parsed Result", result_text, height=400) # Display final result in a text area
