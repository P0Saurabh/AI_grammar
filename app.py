import streamlit as st
import PyPDF2
from gramformer import Gramformer
from textblob import TextBlob
import torch
import spacy
import re
import os
import pandas as pd
import time

# Initialize models
gf = Gramformer(models=1, use_gpu=torch.cuda.is_available())  # Grammar correction
nlp = spacy.load("en_core_web_sm")  # Punctuation and sentence processing

# Directory for reports
GENERATED_DIR = "generated_reports"
os.makedirs(GENERATED_DIR, exist_ok=True)

# Utility to fix contractions
def fix_contractions(text):
    contractions = {"dont": "don't", "its": "it's", "im": "I'm", "doesnt": "doesn't"}
    pattern = re.compile(r'\b(' + '|'.join(contractions.keys()) + r')\b')
    return pattern.sub(lambda x: contractions[x.group()], text)

# Correct spelling and grammar
def correct_text(text):
    spelling_corrected = TextBlob(text).correct()
    corrected_sentences = []
    original_sentences = re.split(r'(?<=[.!?])\s+', str(spelling_corrected))
    for sentence in original_sentences:
        corrected = gf.correct(sentence)
        corrected_sentences.append(list(corrected)[0] if corrected else sentence)
    return ' '.join(corrected_sentences), str(spelling_corrected)

# Highlight changes
def highlight_changes(original, corrected):
    original_words = original.split()
    corrected_words = corrected.split()
    highlighted = []
    for o, c in zip(original_words, corrected_words):
        if o != c:
            highlighted.append(f"<span style='color: red'><b>{c}</b></span>")
        else:
            highlighted.append(o)
    return ' '.join(highlighted)

# Analyze corrections
def analyze_corrections(original, corrected):
    original_words = original.split()
    corrected_words = corrected.split()
    spelling_changes = 0
    grammar_changes = 0

    for o, c in zip(original_words, corrected_words):
        if o != c:
            if TextBlob(o).correct() == c:
                spelling_changes += 1
            else:
                grammar_changes += 1

    return spelling_changes, grammar_changes

# Main Streamlit App
st.title("Grammar and Spelling Correction App")
st.write("Upload a PDF or input text to correct grammar, spelling, and view analytics.")

# Input Section
uploaded_pdf = st.file_uploader("Upload PDF File", type=["pdf"])
input_text = st.text_area("Or Paste Your Text Here", "")

if st.button("Correct Text"):
    text = ""
    with st.spinner("Processing... Please wait!"):
        time.sleep(1)

        # Extract text from PDF or input
        if uploaded_pdf:
            try:
                reader = PyPDF2.PdfReader(uploaded_pdf)
                text = ' '.join(page.extract_text() for page in reader.pages if page.extract_text())
                st.info("PDF text extracted successfully!")
            except Exception as e:
                st.error(f"Error extracting text from PDF: {e}")
                st.stop()
        elif input_text.strip():
            text = input_text
        else:
            st.warning("Please upload a PDF or input text to proceed.")
            st.stop()

        # Fix contractions
        original_text = fix_contractions(text)

        # Correct Text
        corrected_text, spelling_corrected_text = correct_text(original_text)

        # Highlight changes
        highlighted_text = highlight_changes(original_text, corrected_text)

        # Analyze corrections
        spelling_changes, grammar_changes = analyze_corrections(original_text, corrected_text)

        # Total changes
        total_changes = spelling_changes + grammar_changes

        # Display results
        st.subheader("Original Text")
        st.write(original_text)

        st.subheader("Corrected Text (Highlighted Changes in Red)")
        st.markdown(highlighted_text, unsafe_allow_html=True)

        # Display Analytics with Streamlit
        st.subheader("Correction Analytics")
        corrections_df = pd.DataFrame({
            "Correction Type": ["Spelling", "Grammar"],
            "Count": [spelling_changes, grammar_changes]
        })
        st.bar_chart(corrections_df.set_index("Correction Type"))

        st.write(f"**Total Corrections:** {total_changes}")

        # Save report
        report_path = os.path.join(GENERATED_DIR, "correction_report.txt")
        with open(report_path, "w") as report_file:
            report_file.write("Corrected Text:\n")
            report_file.write("====================\n")
            report_file.write(corrected_text)

        st.success("Correction report generated successfully!")
        st.download_button("Download Report", data=open(report_path, "rb"), file_name="correction_report.txt")
