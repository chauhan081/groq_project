# Groq: Multilingual AI Assistant

**TechieGuys** presents **Groq**, a real-time, multilingual AI assistant that understands your questions in three ways:

- **Text Input**
- **Audio Input**
- **Image Input**

### Features

1. **Text Input**: Ask questions in any language (English, Hindi, Hinglish), and get fast, accurate responses powered by Groq.
2. **Audio Input**: Speak your questions and receive voice responses — ideal for visually impaired users.
3. **Image Input**: Upload an image, and the assistant will analyze and provide answers based on the image's content.

### Technologies Used

- **Frontend**: React.js, Bootstrap
- **Backend**: FastAPI, Groq AI Engine
- **Speech-to-Text**: For voice input
- **Image Recognition**: For analyzing images

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chauhan081/groq_project.git
   cd groq_project
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Run the backend with **Uvicorn**:
   ```bash
   uvicorn app:app --reload
   ```

5. Run the frontend:
   ```bash
   npm run dev
   ```

### Contributing

Feel free to fork the repository and contribute by adding features, fixing bugs, or improving documentation.
