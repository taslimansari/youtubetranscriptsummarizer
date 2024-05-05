from flask import Flask, request, json
from youtube_transcript_api import YouTubeTranscriptApi
import re
import heapq
import nltk
from deepmultilingualpunctuation import PunctuationModel

app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')
model = PunctuationModel()

@app.get('/summary')
def summary_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    transcript, summary = get_summary(get_transcript(video_id))
    response = app.response_class(
        response=json.dumps({
        "transcript": transcript,
        "summary": summary
        }),
        status=200,
        mimetype='application/json')
    return response

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([d['text'] for d in transcript_list])
        transcript = model.restore_punctuation(transcript)
        return transcript
    except Exception as ex:
        print("Exception:",{ex})
        if(str(ex).__contains__("TranscriptsDisabled")):
            print("No transcript error")
        return "No transcript"

def get_summary(transcript):
    if(transcript == "No transcript"):
        return "No subtitles found for the video. Try some other URL"
    transcript = re.sub(r'\[[0-9]*\]',' ', transcript)
    transcript = re.sub(r'\s+', ' ', transcript)
    fomrattedTranscript = re.sub('[^a-zA-Z]',' ',transcript)
    fomrattedTranscript = re.sub(r'\s+',' ', fomrattedTranscript)
    sentenceList = nltk.sent_tokenize(transcript)
    stopwords = nltk.corpus.stopwords.words('english')
    
    word_frequencies = {}
    for word in nltk.word_tokenize(fomrattedTranscript):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    sentence_scores = {}
    for sent in sentenceList:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(" ")) < 50:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    # print("Transcript: ", transcript)
    print("*** \nSummary: ", summary)                    
    return transcript,summary
    

if __name__ == '__main__':
    app.run()