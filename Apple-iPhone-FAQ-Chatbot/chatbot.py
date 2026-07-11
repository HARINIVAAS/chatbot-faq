import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read FAQ dataset
data = pd.read_csv("faq.csv")

questions = data["Question"]
answers = data["Answer"]

# Stop words
stop_words = {
    "is", "the", "a", "an", "to", "of", "on", "in",
    "for", "and", "can", "i", "do", "does", "my",
    "how", "what", "who"
}

# Preprocessing
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Train the model
processed_questions = questions.apply(preprocess)

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(processed_questions)

# Function to answer questions
def get_answer(user_question):
    processed = preprocess(user_question)

    user_vector = vectorizer.transform([processed])

    similarity = cosine_similarity(user_vector, faq_vectors)

    index = similarity.argmax()

    score = similarity[0][index]

    if score > 0.25:
        return answers.iloc[index]

    return "Sorry, I don't have information about that. Please ask about iPhone 16 features, camera, battery, display, charging, Apple Intelligence, or model comparisons."

# Run only in terminal
if __name__ == "__main__":

    while True:

        question = input("\nAsk your question (type 'exit' to quit): ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        print("\n🤖", get_answer(question))