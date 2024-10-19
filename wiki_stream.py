import streamlit as st
import spacy
from collections import Counter
import random
import wikipediaapi

# Load the English model for tokenization
nlp_model = spacy.load("en_core_web_sm")

# Function to create MCQs from input text
def create_mcqs(input_text, question_count=5):
    processed_doc = nlp_model(input_text)
    sentence_list = [sentence.text for sentence in processed_doc.sents]
    selected_sentences = random.sample(sentence_list, min(question_count, len(sentence_list)))

    mcq_list = []
    for sentence in selected_sentences:
        sentence_doc = nlp_model(sentence)
        noun_list = [token.text for token in sentence_doc if token.pos_ == "NOUN"]

        if len(set(noun_list)) < 2:
            continue

        noun_frequency = Counter(noun_list)
        if noun_frequency:
            main_noun = noun_frequency.most_common(1)[0][0]
            question_format = sentence.replace(main_noun, "__________")
            choices = [main_noun]
            distractors = list(set(noun_list) - set([main_noun]))

            for _ in range(3):
                if distractors:
                    distractor = random.choice(distractors)
                    choices.append(distractor)
                    distractors.remove(distractor)

            if len(choices) < 4:
                continue

            random.shuffle(choices)
            correct_option = chr(65 + choices.index(main_noun))
            mcq_list.append((question_format, choices, correct_option))

    return mcq_list

# Function to fetch Wikipedia content
def fetch_wikipedia_content(topic):
    user_agent = "MyWikipediaBot/1.0 (sohamyedgaonkar@gmail.com)"
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)
    page = wiki_wiki.page(topic)

    if page.exists():
        return page.text
    else:
        return None

# Streamlit App
st.title("MCQ Generator from Wikipedia")

# Input for Wikipedia topic
topic = st.text_input("Enter a Wikipedia topic:", "Python programming")

# Number of questions to generate
question_count = st.slider("Select the number of questions:", 1, 10, 5)

# Button to generate MCQs
if st.button("Generate MCQs"):
    # Fetch Wikipedia content based on the provided topic
    text = fetch_wikipedia_content(topic)

    if text:
        mcqs_tech = create_mcqs(text, question_count)

        if mcqs_tech:
            for i, mcq in enumerate(mcqs_tech, start=1):
                question_stem, answer_choices, correct_answer = mcq
                st.write(f"**Q{i}: {question_stem}?**")
                for j, choice in enumerate(answer_choices, start=1):
                    st.write(f"{chr(64+j)}. {choice}")
                st.write(f"**Correct Answer: {correct_answer}**\n")
        else:
            st.warning("Could not generate MCQs from the provided Wikipedia content.")
    else:
        st.warning("Could not fetch the Wikipedia page. Please check the topic and try again.")
