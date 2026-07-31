import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getAuth, GoogleAuthProvider } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// User Provided Firebase Web SDK Credentials
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || "AIzaSyDOEUe0o6lJoqo8cv7OwPstE-lkyHqagQw",
  authDomain: process.env.FIREBASE_AUTH_DOMAIN || "elite-elevator-472112-s3.firebaseapp.com",
  projectId: process.env.FIREBASE_PROJECT_ID || "elite-elevator-472112-s3",
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET || "elite-elevator-472112-s3.firebasestorage.app",
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID || "537133039027",
  appId: process.env.FIREBASE_APP_ID || "1:537133039027:web:59547872f73e1ea8101fc6",
  measurementId: process.env.FIREBASE_MEASUREMENT_ID || "G-C08VLZRSD7"
};

// Initialize Firebase App Instance
const app = initializeApp(firebaseConfig);

// Export Auth & DB Services
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
export default app;
