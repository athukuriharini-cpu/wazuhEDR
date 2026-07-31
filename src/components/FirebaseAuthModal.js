import { loginWithEmail, registerWithEmail, loginWithGoogle, resetPassword } from '../services/firebaseAuth.js';

export function renderAuthModal(onSuccessCallback) {
  const modalOverlay = document.createElement('div');
  modalOverlay.id = 'firebase-auth-modal';
  modalOverlay.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(7, 9, 14, 0.85); backdrop-filter: blur(12px);
    display: flex; align-items: center; justify-content: center; z-index: 9999;
  `;

  modalOverlay.innerHTML = `
    <div class="glass-panel" style="width: 420px; padding: 2.2rem; border-color: rgba(168, 85, 247, 0.4); position: relative;">
      <button id="close-auth-modal" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; color: #94a3b8; font-size: 1.2rem; cursor: pointer;">&times;</button>
      
      <div style="text-align: center; margin-bottom: 1.5rem;">
        <i class="fa-solid fa-shield-halved" style="font-size: 2.5rem; color: #c084fc; margin-bottom: 0.5rem;"></i>
        <h2 class="font-heading" style="font-size: 1.8rem; color: #f8fafc;">ShieldEDR Account</h2>
        <p style="color: #94a3b8; font-size: 0.9rem;">Firebase Authentication & Multi-Tenant Access</p>
      </div>

      <div id="auth-error-msg" style="display: none; background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.4); color: #f43f5e; padding: 0.6rem; border-radius: 8px; font-size: 0.85rem; margin-bottom: 1rem; text-align: center;"></div>

      <form id="auth-form">
        <div style="margin-bottom: 1rem;">
          <label style="display: block; color: #cbd5e1; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem;">Email Address</label>
          <input type="email" id="auth-email" required placeholder="admin@yourcompany.com" style="width: 100%; background: #0f172a; border: 1px solid rgba(148, 163, 184, 0.3); border-radius: 10px; padding: 0.7rem; color: white; outline: none;">
        </div>

        <div style="margin-bottom: 1.2rem;">
          <label style="display: block; color: #cbd5e1; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.4rem;">Password</label>
          <input type="password" id="auth-password" required placeholder="••••••••••••" style="width: 100%; background: #0f172a; border: 1px solid rgba(148, 163, 184, 0.3); border-radius: 10px; padding: 0.7rem; color: white; outline: none;">
        </div>

        <button type="submit" id="btn-login-email" class="btn-gradient-purple" style="width: 100%; justify-content: center; margin-bottom: 0.8rem;">
          <i class="fa-solid fa-right-to-bracket"></i> Sign In with Email
        </button>

        <button type="button" id="btn-register-email" style="width: 100%; background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.3); color: white; padding: 0.7rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin-bottom: 1rem;">
          Create New Account
        </button>
      </form>

      <div style="display: flex; align-items: center; margin: 1rem 0;">
        <div style="flex: 1; height: 1px; background: rgba(148, 163, 184, 0.2);"></div>
        <span style="color: #64748b; font-size: 0.75rem; padding: 0 0.8rem; font-weight: 600;">OR</span>
        <div style="flex: 1; height: 1px; background: rgba(148, 163, 184, 0.2);"></div>
      </div>

      <button type="button" id="btn-google-auth" style="width: 100%; background: #ffffff; color: #0f172a; border: none; padding: 0.75rem; border-radius: 10px; font-weight: 700; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.6rem;">
        <i class="fa-brands fa-google" style="color: #ea4335;"></i> Continue with Google
      </button>
    </div>
  `;

  document.body.appendChild(modalOverlay);

  // Close modal handler
  document.getElementById('close-auth-modal').addEventListener('click', () => {
    modalOverlay.remove();
  });

  const showError = (msg) => {
    const errBox = document.getElementById('auth-error-msg');
    errBox.textContent = msg;
    errBox.style.display = 'block';
  };

  // Form submit handler (Login)
  document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('auth-email').value;
    const pass = document.getElementById('auth-password').value;
    const res = await loginWithEmail(email, pass);
    if (res.success) {
      modalOverlay.remove();
      if (onSuccessCallback) onSuccessCallback(res.user);
    } else {
      showError(res.error);
    }
  });

  // Register handler
  document.getElementById('btn-register-email').addEventListener('click', async () => {
    const email = document.getElementById('auth-email').value;
    const pass = document.getElementById('auth-password').value;
    if (!email || !pass) {
      showError('Please enter both Email and Password to register.');
      return;
    }
    const res = await registerWithEmail(email, pass);
    if (res.success) {
      modalOverlay.remove();
      if (onSuccessCallback) onSuccessCallback(res.user);
    } else {
      showError(res.error);
    }
  });

  // Google OAuth handler
  document.getElementById('btn-google-auth').addEventListener('click', async () => {
    const res = await loginWithGoogle();
    if (res.success) {
      modalOverlay.remove();
      if (onSuccessCallback) onSuccessCallback(res.user);
    } else {
      showError(res.error);
    }
  });
}
