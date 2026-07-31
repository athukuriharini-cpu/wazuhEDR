import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js';
import { getAuth, GoogleAuthProvider } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';
import { getFirestore } from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js';

// Configuration for Clean Default Firebase Project (elite-elevator-472112-s3)
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY || "AIzaSyDemoKey_ShieldEDR2026_Secured",
  authDomain: process.env.FIREBASE_AUTH_DOMAIN || "elite-elevator-472112-s3.firebaseapp.com",
  projectId: process.env.FIREBASE_PROJECT_ID || "elite-elevator-472112-s3",
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET || "elite-elevator-472112-s3.appspot.com",
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID || "537133039027",
  appId: process.env.FIREBASE_APP_ID || "1:537133039027:web:a1b2c3d4e5f6a7b8c9"
};

// Initialize Firebase App Instance
const app = initializeApp(firebaseConfig);

// Export Auth & DB Services
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
export const db = getFirestore(app);
export default app;
