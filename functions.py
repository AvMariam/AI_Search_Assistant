import json
import requests
import chromadb

from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from chromadb.utils import embedding_functions


# OpenAI private key
key = <YOUR KEY>


llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",
                 openai_api_key=key)


def extract_content(url):
    """
    This function extracts home and contact (if available) pages of the website.
    If website is locked or doesn't exist, function doesn't return anything.

    :param url: url of the website, which should be scraped,
    :return: html content of the website.
    """
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        contacts = None
        for version in ['/contact', '/contact-us', '/connect']:
            if requests.get(url+version).status_code == 200:
                contacts = requests.get(url+version).text
                break
        return html_content, contacts
    else:
        # # Print status code for information.
        # print("Error fetching URL:", response.status_code)
        return None, None


def remove_unwanted_tags(html_content, unwanted_tags=("script", "style", "span", "comment")):
    """
    This function removes unwanted HTML tags from the given HTML content.

    :param html_content: content received from website,
    :param unwanted_tags: array of tags that should be removed,
    default unwanted_tags=("script", "style", "span", "comment")
    :return: content without mentioned tags.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)

def remove_unnecessary_lines(content):
    """
    This function removes all whitespaced lines from extracted content.
    This is useful for shortening content.

    :param content: html content to clear,
    :return: clean content.
    """

    lines = content.split("\n")
    stripped_lines = [line.strip() for line in lines]
    non_empty_lines = [line for line in stripped_lines if line]
    seen = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in seen or seen.add(line))]
    cleaned_content = "".join(deduped_lines)
    return cleaned_content

def extract_text(html_content):
    """
    This function extracts text from html content
    (i.e. removes tags). It returns clear text from website content.
    This is the last step of web scraping.

    :param html_content: html content to clear,
    :return: clean text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text()
    return text_content


def collect_data(url, collection):
    """
    This function is pipeline for web scraping and necessary information extracting.
    Text extracted from website goes to LLM with prompt, and it returns needed information.

    :param url: website url provided by user.
    :param collection: list where LLM's answer is appended.
    :return: collection or text containing error message (if something is wrong with url).
    """
    schema = {"Name": "company name", "Contacts": ["phone number or email"], "Investment industry": ["industries"],
              "Investment rounds": ["unique types of rounds"], "About": "information about company"}
    home_content, contact_content = extract_content(url)
    if home_content:
        text_content = extract_text(remove_unnecessary_lines(remove_unwanted_tags(home_content)))
        if contact_content:
            contacts = extract_text(remove_unnecessary_lines(remove_unwanted_tags(contact_content)))
        else:
            contacts = ""

        messages = [
            ("system", "You are a helpful assistant that extracts information from the text in given format."),
            ("human",
             f"Extract information about company using {text_content}, {contacts} and "
             f"return in JSON-like string format: {schema}. "
             f"Ensure that property names are enclosed in double quotes without any other characters. "
             f"If information is not available don't add anything.")
        ]
        answer = llm.invoke(messages).content
        answer = json.loads(answer)
        collection.append(answer)

        return collection
    else:
        return "This webpage is locked or doesn't exist. Please check once again."

def add_to_db(item, collection):
    """
    This function is for adding new object to database.

    :param item: the object that should be added,
    :param collection: database.
    """
    collection.add(documents=[item["About"]],
                   ids=[item["Name"]],
                   metadatas=[{"Contacts": str(item["Contacts"]),
                               "Investment industry": str(item["Investment industry"]),
                               "Investment rounds": str(item["Investment rounds"])}])

def get_collection():
    """
    This function opens existing database.

    :return: database
    """
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=key,
        model_name="text-embedding-3-small"
    )
    client = chromadb.PersistentClient(path="database")
    collection = client.get_collection(name="DataBase", embedding_function=openai_ef)
    return collection

def find_similars(query):
    """
    This function finds 3 most similar objects from database based on the query.

    :param query: text to compare with,
    :return: list of the similar companies' names.
    """
    collection = get_collection()
    try:
        data_distances = collection.query(query_texts=query, n_results=4)["ids"]
        return data_distances[0][1:]
    except:
        return "Nothing similar was found"