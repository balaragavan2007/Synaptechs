# 🎓 Synaptechs: Your Personalized AI Learning Assistant

![Synaptechs Banner](https_link_to_a_cool_banner_image.png)  Hey there! 👋 This is a personalized learning assistant I built for the Defang.io Hackathon. It's designed to be a smart study buddy that helps you learn better and faster.

---

## ✨ Cool Features

* **Chat with Your Notes:** Upload your PDFs and even pictures of notes, and ask the AI questions about them.
* **Internet Power:** If your notes don't have the answer, the AI can search the web to find it.
* **See with AI Eyes:** Upload any image and ask the AI to describe what's in it using Gemini Vision.
* **Study Tools:** Automatically creates quizzes from your documents, summarizes topics, and schedules study sessions for you.

---

## 🛠️ Tech Stack

* **Frontend (UI):** Streamlit
* **Backend & AI Logic:** Python & LangChain
* **AI Models:** Groq (Llama 3), Google Gemini Vision
* **Database:** ChromaDB (for storing document knowledge)
* **Deployment:** Docker & Defang.io

---

## 🚀 How to Run it Yourself

Want to try it out? Here's how:

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/balaragavan2007/Synaptechs.git
    ```
2.  **Install everything:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Add your API keys:** Create a file named `.env` and paste your secret API keys inside.
    ```
    GROQ_API_KEY="your-key"
    TAVILY_API_KEY="your-key"
    GOOGLE_API_KEY="your-key"
    ```
4.  **Launch the app:**
    ```bash
    streamlit run app.py
    ```

---

##  live Demo

[Link to your live Defang.io application will go here!]
