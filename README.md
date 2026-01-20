# Spam Text & Phishing Link Detection System

This Project detects spam text and phishing links
using machine learning and a Flask-based web application.


## Project Purpose

- Identify spam text messages
- Detect phishing or malicious URLs
- Show probability-based results (95% – 99%)


## Technologies Used

- HTML, CSS, JavaScript
- Python
- Flask
- Scikit-learn
- Naive Bayes Classifier
- Joblib
  

## Dataset

Public datasets were used:
- Spam text datasets (SMS / email spam)
- Phishing URL datasets (PhishTank, OpenPhish)

These datasets are labeled as Spam or Safe and are commonly used
for academic and research purposes.



## Model Training

- Text data was vectorized using TF-IDF
- Naive Bayes algorithm was used for classification
- The trained model was saved and loaded in Flask for predictions



## How It Works

1. User enters text or a URL
2. Flask sends input to the ML model
3. Model predicts Spam or Safe
4. Result is shown with probability and icon



## Developer

Aqsa Khalid 
# spam-text-and-phishing-link-detector
A Flask-based machine learning project that detects spam text and phishing links with probability-based results.
