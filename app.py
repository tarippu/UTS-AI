from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
from textblob import TextBlob as tb

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def main():
    if request.method == 'POST': 

        link = request.form['link']
        a = urlparse(link)
        a.query
        vid = a.query[2:]

        URL = "https://www.googleapis.com/youtube/v3/commentThreads"
        API_KEY = "AIzaSyB9M8at9waqOd3CjpdHvKKIBoMRfg0U2Ws"
        VIDEO_ID = vid

        response = requests.get(f"{URL}?key={API_KEY}&videoId={VIDEO_ID}&part=snippet")
        response_json = response.json()

        comments = []
        comment = []
        creator = []
        i = 0
        for item in response_json["items"]:
            if i <= 5:
                author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                content = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

                creator.append(author)
                comment.append(content)

                i += 1
            else :
                break
        
        mood = []
        for i in comment:
            sentimen = tb(i).sentiment.polarity
            if sentimen < 0:
                mood.append("Sentiment Negativ")
            elif sentimen == 0:
                mood.append("Sentiment Netral")
            else :
                mood.append("Sentiment Positiv")

        return render_template('index.html', link = link, mood = mood, creator = creator, comment = comment)
    return render_template('form.html')


# if __name__ == "__main__":
#     app.run(debug=True) 