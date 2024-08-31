# WebScrape-Ollama
![Video Example](https://github.com/user-attachments/assets/5fd4378b-ea65-467b-aace-3e3218b4fd7e)

WebScrape-Ollama is a powerful web scraping application designed to extract, clean, and parse data efficiently from web pages 
using Selenium, BeautifulSoup, and the Ollama 3.1 model. The app provides a streamlined interface for interacting with scraped 
data, making it easy to harness the information you need. *Works well with Wikipedia pages*

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

## Areas for Improvement

While the current version of the web scraping AI app performs well, there are several areas where it could be enhanced:

- **Speed of Processing:** The app could benefit from optimization techniques to reduce the time it takes to scrape and process large volumes of data. Implementing more efficient algorithms and parallel processing could significantly improve performance.
  
- **Captcha Handling:** One of the challenges with web scraping is dealing with CAPTCHA tests, which often prevent automated scripts from accessing certain websites. Integrating advanced CAPTCHA-solving techniques or bypass strategies would allow the app to scrape data more effectively.

- **Error Handling:** Enhancing the app’s ability to handle unexpected errors, such as network timeouts or changes in website structure, would make it more robust and reliable.

- **Scalability:** As the data sources grow, ensuring that the app can scale efficiently to handle increased loads without compromising on speed or accuracy is crucial.

- **User-Friendly Interface:** Improving the user interface to make the app more accessible to non-technical users would broaden its usability and appeal.

