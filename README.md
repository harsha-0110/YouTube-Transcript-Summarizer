# Youtube Transcript Summarizer:

This is a web application that takes a YouTube video link, generates its transcript and provides a summarized version of the transcript using two methods: Natural Language Processing (NLP) and Machine Learning (ML). The summary can be useful for quickly understanding the main points of a long video without having to watch the entire video.

Installation
Clone the repository:
-`git clone https://github.com/harsha-0110/YouTube-Transcript-Summarizer.git`

Install the required dependencies using pip:
-`pip install -r requirements.txt`

Usage
- Run the application:
    `python app.py`
- Open a web browser and go to `http://localhost:5000/`.
- Enter a YouTube video link and select the summarization method you want to use (NLP or ML).
- Click on the "Summarize" button and wait for the summary to be generated.
- The summary will be displayed on the web page along with the number of original words and the number of words after summarization.
- Click the "Convert To Speech" to convert the summarized transcript into audio. 

Technology Stack
- Python
- Flask (web framework)
- Youtube_transcript_api (API for generating YouTube video transcripts)
- NLTK (Natural Language Toolkit for NLP tasks)
- Transformers (Python library for state-of-the-art NLP)

Contributors
- Surya G
- Harshavardhan A
