# AI_Search_Assistant

Welcome to the AI Search Assisitant! This project aims to assist users in extracting valuable information from Venture Capital (VC) websites and comparing them to find similar VCs. Whether you're an entrepreneur looking for potential investors or a researcher exploring the VC landscape, this tool can streamline your search process.

## How It Works
- Input VC Website URL: Users provide the URL of the VC website they want to analyze.
- Scraping and Storage: The Generative AI Assistant scrapes the homepage of the provided website and stores the content in a vector database.
- Information Extraction: Key information such as VC name, contacts, industries they invest in, and their participation in investment rounds is extracted and presented to the user.
- Comparison: The application calculates the cosine similarity between the embedded vectors of the provided VC website and other VC websites stored in the database. Based on this similarity measure, the three most similar VCs are identified and presented to the user.

## Technical Details
- Generative AI Assistant: The scraping process involves utilizing various functions to extract relevant information from the HTML content of VC websites. OpenAI's API key is employed to enhance the extraction process, ensuring accuracy and completeness of the gathered data.
- API Interface: Utilizing Flask, an API is created to serve as the interface for interacting with the AI Assistant.
- Database: For storage and retrieval of embedded vectors, ChromaDB is utilized. ChromaDB offers robust features for managing vector data efficiently, facilitating fast and scalable comparison between VC websites.

## How to Use
- Clone the repository from GitHub.
- Set up the required environment by installing the packages listed in the requirements.txt file.
- Obtain an OpenAI Secret API key and add it within the code where required (in functions.py and creating_db.py files).
- Deploy the application either on the cloud platform of your choice or using Docker containers.
- Access the application through the provided URL.
- Enter the VC website URL you want to analyze.

## Here are screenshots of how app works:
  ![image](https://github.com/AvMariam/AI_Search_Assistant/assets/125482296/10cebe31-7cb2-4d38-9c6d-29c27021055a)
  ![image](https://github.com/AvMariam/AI_Search_Assistant/assets/125482296/67402680-97bd-467e-a91b-735e0c26d180)
  

## Technologies Used
- OpenAI API
- Flask
- ChromaDB

Contributions to the project are welcome! Feel free to submit pull requests or open issues for any improvements or bug fixes.
For any questions or inquiries, please contact hi.avmariam@gmail.com.
