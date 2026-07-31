import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getAuth, GoogleAuthProvider } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// Firebase Web Configuration Parameters
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || "AIzaSyDemoKey_ShieldEDR2026_Secured",
  authDomain: process.env.FIREBASE_AUTH_DOMAIN || "shieldedr-saas.firebaseapp.com",
  projectId: process.env.FIREBASE_PROJECT_ID || "shieldedr-saas",
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET || "shieldedr-saas.appspot.com",
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID || "987654321098",
  appId: process.env.FIREBASE_APP_ID || "1:987654321098:web:a1b2c3d4e5f6a7b8c9"
};

// Initialize Firebase App Instance
const app = initializeApp(firebaseConfig);

// Export Auth & DB Services
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
export default app;
