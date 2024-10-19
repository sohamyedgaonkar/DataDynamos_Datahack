import streamlit as st
import pdfplumber
import spacy
from collections import Counter
import random

# Load Spacy English model
nlp_model = spacy.load("en_core_web_sm")

# MCQ generation function
def create_mcqs(input_text, question_count=5):
    processed_doc = nlp_model(input_text)
    sentence_list = [sentence.text for sentence in processed_doc.sents]
    selected_sentences = random.sample(sentence_list, min(question_count, len(sentence_list)))
    mcq_list = []
    for sentence in selected_sentences:
        sentence_doc = nlp_model(sentence)
        noun_list = [token.text for token in sentence_doc if token.pos_ == "NOUN"]
        if len(noun_list) < 2:
            continue
        noun_frequency = Counter(noun_list)
        if noun_frequency:
            main_noun = noun_frequency.most_common(1)[0][0]
            question_format = sentence.replace(main_noun, "__________")
            choices = [main_noun]
            for _ in range(3):
                distractor = random.choice(list(set(noun_list) - set([main_noun])))
                choices.append(distractor)

            random.shuffle(choices)

            correct_option = chr(64 + choices.index(main_noun) + 1)
            mcq_list.append((question_format, choices, correct_option))

    return mcq_list

# Streamlit UI
st.title("PDF MCQ Generator")

# File uploader for PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Open the PDF and extract text
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    # Display extracted text
    st.write("Extracted Text:")
    st.write(text)

    # Number of questions to generate
    question_count = st.slider("Number of MCQs to generate", 1, 10, 5)

    if st.button("Generate MCQs"):
        mcqs = create_mcqs(text, question_count=question_count)
        if mcqs:
            for i, (question, choices, correct_option) in enumerate(mcqs):
                st.write(f"Q{i+1}: {question}")
                for j, choice in enumerate(choices):
                    st.write(f"    {chr(65+j)}. {choice}")
                st.write(f"Correct Answer: {correct_option}")
        else:
            st.write("Not enough data to generate MCQs.")
