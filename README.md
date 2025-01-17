

# 📚 Grammar and Spelling Correction App

A powerful **Streamlit** web application that corrects grammar and spelling in PDF documents or text inputs. The app also provides analytics on the number of spelling and grammar corrections and allows users to download correction reports.

## 🚀 Features
- 📄 **PDF Upload**: Extract and correct text from PDF files.  
- ✍️ **Text Input**: Paste text directly for instant correction.  
- ✅ **Grammar and Spelling Correction**: Uses **Gramformer** and **TextBlob** for advanced text correction.  
- 🔍 **Analytics Visualization**: Displays the number of spelling and grammar corrections via bar charts.  
- 📥 **Downloadable Reports**: Generates and allows downloading of corrected text reports.

---

## 🛠️ Tech Stack
- **Python**  
- **Streamlit** (Web UI)  
- **Gramformer** (Grammar Correction)  
- **TextBlob** (Spelling Correction)  
- **PyPDF2** (PDF Text Extraction)  
- **spaCy** (Text Processing)  
- **Pandas** (Data Analytics)  

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/grammar-spelling-correction-app.git
   cd grammar-spelling-correction-app
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

---


## 📄 Example Report

- **Original Text:** Displays the input text.  
- **Corrected Text:** Highlights grammar and spelling corrections.  
- **Analytics:** Bar chart showing correction counts.  
- **Download:** Correction report in `.txt` format.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📧 Contact

For any queries or feedback, reach out at **your-email@example.com**.

---

## ⚖️ License

This project is licensed under the [MIT License](LICENSE).

---

Let me know if you'd like any adjustments or customization!
