// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCbkt3Z96R4OxDrlB4hMAaJ8DOD23jf5E8",
    authDomain: "groqproject.firebaseapp.com",
    projectId: "groqproject",
    storageBucket: "groqproject.firebasestorage.app",
    messagingSenderId: "1089940432283",
    appId: "1:1089940432283:web:a250724ff3d2d29b346d3e",
    measurementId: "G-7WHBHGC51X"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
