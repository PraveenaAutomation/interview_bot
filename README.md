# 🤖 Interview Q&A Bot

A smart web-based chatbot to help you practice and prepare for interviews. Get instant AI-generated answers to your questions and track your question history with a beautiful, modern UI.

---

## ✨ Features

- 💬 Ask technical and behavioral interview questions  
- 🤖 Get intelligent, contextual answers using LangGraph + Pinecone vector search  
- 🧠 Question history panel with timestamps  
- 🧹 "Clear History" button to reset session  
- 📱 Responsive design (desktop & mobile)  

---

## 🛠️ Tech Stack

### Frontend
- Vue 3  
- Vite  
- Tailwind CSS  
- lucide-vue-next  

### Backend
- Python Flask  
- LangGraph  
- Pinecone Vector DB  
- Flask-CORS  

---

## 🧩 Project Structure

```
interview_bot/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   │   └── bot-icon.png
│   │   └── components/
│   │       └── Chatbot.vue
│   ├── public/
│   ├── tailwind.config.js
│   ├── index.html
│   └── package.json
```

---

## ⚙️ Getting Started

### ✅ Prerequisites

- Python 3.8+  
- Node.js + npm  
- Pinecone account & API key  
- OpenAI account with valid billing  

---

### 🧪 Backend Setup

1. Navigate to the `backend` folder:

   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Pinecone and OpenAI credentials:

   ```
   OPENAI_API_KEY=your-openai-key
   PINECONE_API_KEY=your-pinecone-key
   PINECONE_ENV=your-pinecone-env
   PINECONE_INDEX_NAME=your-index-name
   ```

5. Start the Flask server:

   ```bash
   python app.py
   ```

   The server will run at: `http://localhost:5000`

---

### 🌐 Frontend Setup

1. Navigate to the `frontend` folder:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Start the Vite dev server:

   ```bash
   npm run dev
   ```

   The app will be available at: `http://localhost:5173`

---

## 🚀 Usage

1. Open the app in your browser.  
2. Ask an interview question like “What is Selenium?”  
3. View your answer and see the question logged in the left sidebar.  
4. Click **Clear History** to reset your session.  

---

## 🔁 API Endpoint

### `POST /ask`

**Request:**

```json
{
  "question": "What is Selenium?"
}
```

**Response:**

```json
{
  "question": "What is Selenium?",
  "answer": "Selenium is an open-source automation tool for web applications..."
}
```

---

## 🧹 To Do

- Add persistent history (e.g., LocalStorage or backend DB)  
- Add loading indicators and markdown support  
- Improve error boundaries and network handling  
- Add categories or skill filters (Frontend, Backend, DevOps, etc.)  

---

## 📜 License

MIT License

---

## 👩‍💻 Author

Built with ❤️ by [Praveena Kumar](https://www.linkedin.com/in/praveena-p-kumar-10403432/)
