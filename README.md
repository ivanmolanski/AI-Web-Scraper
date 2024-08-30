# WebScrape-Ollama

![Video Example](https://github.com/user-attachments/assets/4c0d7834-e77e-47cc-872c-c0f4c92eb852)

WebScrape-Ollama is a powerful web scraping application designed to extract, clean, and parse data efficiently from web pages 
using Selenium, BeautifulSoup, and the Ollama 3.1 model. The app provides a streamlined interface for interacting with scraped 
data, making it easy to harness the information you need.

## How To Get Started
1. **Initialize the Environment:** Set up your environment by installing the required dependencies listed in the `requirements.txt` file.
2. **Install Ollam 3.1:** Or any other version of [Ollama](https://ollama.com) (just make sure to change model version in parse.py)
3. **Run the App:** Start the application using Streamlit by running:

    ```
    streamlit run app.py
    ```

4. **Input Target URL:** Provide the URL of the webpage you want to scrape.
5. **Scrape and Parse Data:** The app will scrape the webpage, clean the data, and parse it based on the specified parameters.

## Features
- **Data Extraction with Selenium:**
  - The app uses Selenium to interact with web pages, handling dynamic content and JavaScript-loaded elements.
  - Automates the process of navigating through pages, clicking elements, and collecting data.

- **Data Cleaning and Parsing:**
  - BeautifulSoup, along with `lxml` and `html5lib`, is used to clean and structure the raw HTML data.
  - The app parses the cleaned data to extract only the relevant information as per user-defined criteria.

- **AI-Enhanced Data Processing:**
  - Leverages the power of the Ollama 3.1 model through `langchain_ollama` to process and refine the extracted data, ensuring high accuracy and relevance.
  - Streamlines complex data interpretation tasks with advanced AI capabilities.

- **User-Friendly Interface:**
  - Built using Streamlit, the app provides an intuitive interface for users to input URLs, manage scraping tasks, and view results in real time.
  - Displays parsed data in an organized and easy-to-read format.

## What I Used To Build The Web App
- **Python 3**
- **Streamlit:** For building the web application interface.
- **Selenium:** For web scraping and browser automation.
- **BeautifulSoup4:** For parsing and navigating the HTML structure of web pages.
- **lxml and html5lib:** For efficient HTML and XML processing.
- **langchain and langchain_ollama:** For integrating AI-powered data processing with the Ollama 3.1 model.
- **python-dotenv:** For managing environment variables securely.
