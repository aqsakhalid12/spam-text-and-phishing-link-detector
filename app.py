from flask import Flask, request, jsonify, render_template
import re
from urllib.parse import urlparse
import joblib

app = Flask(__name__)

# ML-load-model
try:
    textModel = joblib.load('text_phish/text_model.pkl')
    vectorizerModel = joblib.load('text_phish/vectorizer.pkl')
    loadModel = True
    print(" Model files loaded Successfully.")
except:
    textModel = None
    vectorizerModel = None
    loadModel = False
    print("Model files not found!")

phishingSites = [
    "secure-bank.co",
    "moradacerta.site",
    "consultefinanceiro.services",
    "win-prize-claim-now.xyz"
]


def identifyUrls(text):
    pattern = r'https?://(?:[a-zA-Z0-9$-_@.&+!*(),]|(?:%[0-9a-fA-F]{2}))+'
    return re.findall(pattern, text)


def checkMalicious(url):
    url = url.lower()
    domain = urlparse(url).netloc
    suspiciousEnds = ['.online', '.xyz',
                      '.site', '.live', '.info', '.top', '.co']
    keywords = ['login', 'verify', 'account', 'security',
                'update', 'signin', 'webscr', 'password']

    if any(k in url for k in keywords):
        return True, "Contains suspicious keywords"
    if len(url) > 75:
        return True, "URL unusually long"
    if domain in phishingSites:
        return True, "URL in phishing database"
    lastPart = domain.split('.')[-1]
    if lastPart in suspiciousEnds:
        return True, "Suspicious TLD"
    return False, "No phishing indicators"


def checkText(text):
    lowerText = text.lower()

    if loadModel:
        try:
            vect = vectorizerModel.transform([lowerText])
            pred = textModel.predict(vect)[0]
            return ("Spam (ML)", "Classified as Spam") if pred == 1 else ("Safe (ML)", "Classified as Safe")
        except:
            pass

    keywords = ['urgent', 'win', 'prize', 'claim', 'free',
                'money back', 'congratulations', 'click here']
    if any(k in lowerText for k in keywords):
        return "Suspicious", "Contains spam keywords"
    if len(re.findall(r'[A-Z]{3,}', text)) > 2 and len(text) > 20:
        return "Suspicious", "Excessive capitals"
    return "Safe", "No spam keywords"

# routes


@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def analyze():
    data = request.form 

    # Url-analysis
    if 'url' in data:
        urls = identifyUrls(data['url'])
        results = []
        for url in urls:
            phishing, reason = checkMalicious(url)
            results.append({"url": url, "heuristic_check": {
                           "result": "Suspicious" if phishing else "Safe", "reason": reason}})
        return jsonify(results)

    # Text-analysis
    if 'userInput' in data:
        text = data['userInput']
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
        spamResult, spamMassage = checkText(text)
        urls = identifyUrls(text)
        urlResult = [{"url": u, "heuristic_check": {"result": "Suspicious" if checkMalicious(
            u)[0] else "Safe", "reason": checkMalicious(u)[1]}} for u in urls]
        return jsonify({"textAnalysis": {"text": text, "spamCheck": {"result": spamResult, "reason": spamMassage}}, "urlCheck": urlResult})

    return jsonify({"error": "Provide 'url' or 'userInput'"}), 400


if __name__ == '__main__':
    app.run(debug=True)
