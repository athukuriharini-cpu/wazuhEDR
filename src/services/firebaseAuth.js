import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  sendPasswordResetEmail
} from 'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js';

import { auth, googleProvider } from '../firebaseConfig.js';

/**
 * Signs in an existing user with Email and Password
 */
export async function loginWithEmail(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    console.error('Firebase Auth Login Error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Registers a new user with Email and Password
 */
export async function registerWithEmail(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return { success: true, user: userCredential.user };
  } catch (error) {
    console.error('Firebase Auth Register Error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Sign in using Google OAuth Popup
 */
export async function loginWithGoogle() {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    return { success: true, user: result.user };
  } catch (error) {
    console.error('Firebase Google Auth Error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Sends a password reset email
 */
export async function resetPassword(email) {
  try {
    await sendPasswordResetEmail(auth, email);
    return { success: true, message: 'Password reset link sent to your email.' };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Signs out the active user session
 */
export async function logoutUser() {
  try {
    await signOut(auth);
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Listens for Firebase Auth state changes
 */
export function subscribeAuthState(callback) {
  return onAuthStateChanged(auth, (user) => {
    callback(user);
  });
}
