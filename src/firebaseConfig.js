import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getAuth, GoogleAuthProvider } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// Configuration for Firebase Authentication & Hosting
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || "AIzaSyDql4uecUhZNTJEMk0Xpuj38CvntaB3VvE",
  authDomain: process.env.FIREBASE_AUTH_DOMAIN || "nyayaai-app.firebaseapp.com",
  projectId: process.env.FIREBASE_PROJECT_ID || "elite-elevator-472112-s3",
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET || "nyayaai-app.firebasestorage.app",
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID || "855141879693",
  appId: process.env.FIREBASE_APP_ID || "1:855141879693:web:9b0f67c8fb8d90bb8277c4"
};

// Initialize Firebase App Instance
const app = initializeApp(firebaseConfig);

// Export Auth & DB Services
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
export default app;
