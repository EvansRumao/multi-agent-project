# Import the tool decorator from LangChain
# This allows us to convert normal Python functions into tools
# that can be used by AI agents.
from langchain.tools import tool 

# Import requests library for sending HTTP requests to websites
import requests

# Import BeautifulSoup for parsing and extracting HTML content
from bs4 import BeautifulSoup

# Import TavilyClient for performing web searches
from tavily import TavilyClient

# Import os module to access environment variables
import os 

# Import load_dotenv to load API keys from .env file
from dotenv import load_dotenv

# Import rich print for better formatted console output
from rich import print


# Load environment variables from the .env file
# Example:
# TAVILY_API_KEY=your_api_key_here
load_dotenv()


# Create a Tavily client using the API key stored in environment variables
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# -----------------------------
# WEB SEARCH TOOL
# -----------------------------

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information on a topic.
    
    Parameters:
        query (str): The search query entered by the user.
    
    Returns:
        str: A formatted string containing titles, URLs, and snippets
             from search results.
    """

    # Perform the search using Tavily API
    # max_results=5 means only top 5 results will be returned
    results = tavily.search(query=query, max_results=5)

    # Create an empty list to store formatted results
    out = []

    # Loop through each search result
    for r in results['results']:

        # Format the title, URL, and first 300 characters of content
        out.append(
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:300]}\n"
        )

    # Join all results using separator lines
    return "\n----\n".join(out)


# -----------------------------
# URL SCRAPING TOOL
# -----------------------------

@tool
def scrape_url(url: str) -> str:
    """
    Scrape the content of a webpage and return extracted text.
    
    Parameters:
        url (str): The webpage URL to scrape.
    
    Returns:
        str: Extracted paragraph text from the webpage
             or an error message if scraping fails.
    """

    try:
        # Send GET request to the webpage
        # timeout=8 prevents waiting forever if site is slow
        # User-Agent header makes the request look like a browser
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraph (<p>) tags in the webpage
        paragraphs = soup.find_all('p')

        # Extract text from each paragraph and combine them
        text = '\n'.join([p.get_text() for p in paragraphs])

        # Return the extracted text
        return text

    except Exception as e:
        # If any error occurs, return the error message
        return f"Error scraping URL: {str(e)}"


# -----------------------------
# TESTING THE TOOLS
# -----------------------------

# Invoke the web search tool with a query
# This searches for latest AI news and prints the results
print(web_search.invoke("What is the latest news on AI?"))


# Invoke the scraping tool on a BBC technology article
# This extracts and prints paragraph text from the webpage
print(
    scrape_url.invoke(
        "https://www.bbc.com/news/technology-56933733"
    )
)
