// src/App.jsx
import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import Home from "./pages/Home";
import Login from "./components/Login";
import Chat from "./pages/Chat";
import Navbar from "./components/Navbar";
import Signup from "./components/Signup";
import Logout from "./components/Logout";
import AuthStatus from "./components/AuthStatus";

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState("en-US");

  return (
    <>
      <Navbar
        selectedLanguage={selectedLanguage}
        onLanguageChange={setSelectedLanguage}
      />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/status" element={<AuthStatus />} />
        <Route
          path="/chat"
          element={<Chat selectedLanguage={selectedLanguage} />}
        />
      </Routes>
    </>
  );
}

export default App;
