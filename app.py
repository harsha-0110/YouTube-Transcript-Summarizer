from flask import Flask, render_template, request, send_from_directory
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

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
    if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
      summary += " " + sentence
  return summary

def get_transcript(video_link):
    video_id = re.search(r'v=([^&]*)', video_link).group(1)
    transcript = yta.get_transcript(video_id)
    lines = ""
    temp = ""
    for line in transcript:
      temp = line['text']
      lines += temp.replace("\n", " ")
    return lines

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  link = ''
  text = ""
  summary = ""
  final = ""
  if request.method == 'POST':
    link = request.form['link']
    text = get_transcript(link)
    now = len(text.split())
    summary = summarize(text)
    nsw = len(summary.split())
    summary += "\n\n" + "No. of original words = " + str(now) + "\n\n" + "No. of words after Summrization: " + str(nsw)
    if nsw == 0:
      final = "No Transcript found."
    else:
      final = summary
  return render_template('index.html', value = final)

if __name__ == '__main__':
  app.run()