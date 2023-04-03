from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def summarize(text):
  stopWords = set(stopwords.words("english"))
  words = word_tokenize(text)

  freqTable = dict()
  for word in words:
    word = word.lower()
    if word in stopWords:
      continue
    if word in freqTable:
      freqTable[word] += 1
    else:
      freqTable[word] = 1

  sentences = sent_tokenize(text)
  sentenceValue = dict()

  for sentence in sentences:
    for word, freq in freqTable.items():
      if word in sentence.lower():
        if sentence in sentenceValue:
          sentenceValue[sentence] += freq
        else:
          sentenceValue[sentence] = freq


  sumValues = 0
  for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

  average = int(sumValues / len(sentenceValue))

  summary = ''
  for sentence in sentences:
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.3 * average)):
      summary += " " + sentence
    
  return summary

def summarize_text(text, chunk_size=500, max_length=100, min_length=10, num_beams=4, gpu_device=0):
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-xsum-12-6")
    model = AutoModelForSeq2SeqLM.from_pretrained("sshleifer/distilbart-xsum-12-6").to(gpu_device)

    # Split the input text into chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Summarize each chunk and combine the summaries
    summaries = []
    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors='pt').to(gpu_device)
        summary_ids = model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            num_beams=num_beams,
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
        summaries.append(summary)
    summary = ' '.join(summaries)

    return summary

def get_transcript(video_link):
    video_id = re.search(r'v=([^&]*)', video_link).group(1)
    transcript = yta.get_transcript(video_id)
    lines = ""
    temp = ""
    for line in transcript:
      temp = line['text']
      lines += temp.replace("\n", " ")
    with open("clean.txt", "w") as f:
      f.write(lines)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  link = ''
  summary = ""
  final = ""
  if request.method == 'POST':
    link = request.form['link']
    method = request.form['method']
    get_transcript(link)
    with open("clean.txt", "r") as f:
      input_text = f.read()
    now = len(input_text.split())
    if method == 'nlp':
      summary = summarize(input_text)
    elif method == 'ml':
      summary = summarize_text(input_text)
    nsw = len(summary.split())
    summary += "\n\n" + "No. of original words = " + str(now) + "\n\n" + "No. of words after Summrization: " + str(nsw)
    if nsw == 0:
      final = "No Transcript found."
    else:
      final = summary
  return render_template('index.html', value = final)

if __name__ == '__main__':
  app.run("0.0.0.0")