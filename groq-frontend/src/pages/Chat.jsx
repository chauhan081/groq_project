import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import Navbar from "../components/Navbar";

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const Chat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState("en-US");

  const messagesEndRef = useRef(null);
  const recognition = useRef(null);

  const userId = "123"; // Dummy user ID (replace with Firebase Auth if needed)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (SpeechRecognition) {
      recognition.current = new SpeechRecognition();
      recognition.current.continuous = false;
      recognition.current.interimResults = false;
      recognition.current.lang = selectedLanguage;

      recognition.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
      };

      recognition.current.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setIsListening(false);
      };

      recognition.current.onend = () => setIsListening(false);
    }
  }, [selectedLanguage]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/api/text", {
        user_id: userId,
        prompt: input,
        lang: selectedLanguage,
      });

      const botMessage = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error fetching response." },
      ]);
    }

    setInput("");
    setLoading(false);
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMessages((prev) => [...prev, { sender: "user", text: "[Image Uploaded]" }]);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("lang", selectedLanguage);

    try {
      const res = await axios.post("http://localhost:8000/api/image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const imageResponse = res.data.llm_response || res.data.description;

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: imageResponse,
          imageUrl: `http://localhost:8000/${res.data.filename}`,
        },
      ]);
    } catch (err) {
      console.error("Image upload error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error processing image." },
      ]);
    }

    setLoading(false);
  };

  const handleAudioUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMessages((prev) => [...prev, { sender: "user", text: "[Audio Uploaded]" }]);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/audio", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: `📝 Transcription: ${res.data.transcription}` },
        { sender: "bot", text: "🔊 Audio response:", audio: res.data.tts_audio_file },
      ]);
    } catch (err) {
      console.error("Audio upload error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error processing audio." },
      ]);
    }

    setLoading(false);
  };

  const toggleListening = () => {
    if (!SpeechRecognition) {
      alert("Speech Recognition is not supported in your browser.");
      return;
    }

    recognition.current.lang = selectedLanguage;

    if (isListening) {
      recognition.current.stop();
    } else {
      recognition.current.start();
    }

    setIsListening(!isListening);
  };

  return (
    <div className="container-fluid d-flex flex-column vh-100 p-0">
      <div className="flex-grow-1 overflow-auto px-3 py-2" style={{ background: "#f8f9fa" }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            className="my-2 d-flex"
            style={{ justifyContent: msg.sender === "user" ? "flex-end" : "flex-start" }}
          >
            <div
              className={`p-2 rounded shadow-sm bg-${msg.sender === "user" ? "primary" : "secondary"} text-white`}
              style={{ maxWidth: "75%", whiteSpace: "pre-wrap" }}
            >
              <ReactMarkdown>{msg.text}</ReactMarkdown>
              {msg.imageUrl && <img src={msg.imageUrl} alt="Uploaded" style={{ maxWidth: "100%", height: "auto" }} />}
              {msg.audio && (
                <audio controls style={{ marginTop: "5px" }}>
                  <source src={`http://localhost:8000/${msg.audio}`} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-start my-2">
            <span className="badge bg-warning text-dark">Typing...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="d-flex align-items-center px-3 py-2 bg-white border-top" style={{ position: "sticky", bottom: 0 }}>
        <input
          className="form-control me-2"
          placeholder="Type or speak your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          disabled={loading}
        />
        <label className="btn btn-outline-secondary me-2 mb-0" title="Upload Image">
          🖼️
          <input type="file" accept="image/*" hidden onChange={handleImageUpload} />
        </label>
        <button
          className={`btn ${isListening ? "btn-danger" : "btn-outline-secondary"} me-2`}
          onClick={toggleListening}
          title="Voice Input"
        >
          🎙️
        </button>
        <button className="btn btn-primary" onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chat;
