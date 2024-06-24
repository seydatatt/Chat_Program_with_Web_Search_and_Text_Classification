# Chat_Program_with_Web_Search_and_Text_Classification

This project is a Chat Program that analyzes user input text, classifies it into relevant topics, and fetches appropriate links from the web. The program continues to run until the user issues an exit command. It utilizes a text classification model and web search to provide related links based on the classified topics.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Introduction
This project aims to develop a chat program that can analyze user input, classify it into relevant topics, and fetch related links from the web. It uses a pre-trained text classification model and a web search API to enhance user interaction by providing relevant information.

## Features
- **Text Classification:** Classifies user input into predefined categories.
- **Web Search:** Fetches relevant links from the web based on the classified topic.
- **Database Management:** Saves classified topics and search results in an SQLite database.
- **Interactive Chat:** Continuously interacts with the user until an exit command is given.

## Installation
To run this project locally, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/chat-program.git
    cd chat-program
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up API keys:**
   - Obtain an API key from the Google Custom Search API.
   - Set the `API_KEY` and `CX` (custom search engine ID) in the `ChatProgram` initialization.

## Usage
To use the Chat Program, follow these steps:

1. **Run the program:**
    ```sh
    python chat_program.py
    ```

2. **Interact with the chat:**
   - Input text related to different topics.
   - The program will classify the text, search for related links, and display them.
   - To exit the program, input `q`.

## Acknowledgements
This project utilizes the following resources:
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Google Custom Search API](https://developers.google.com/custom-search/)
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
