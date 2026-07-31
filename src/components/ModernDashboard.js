import { renderAuthModal } from './FirebaseAuthModal.js';
import { logoutUser, subscribeAuthState } from '../services/firebaseAuth.js';

export function initModernApp() {
  const root = document.getElementById('app-root');

  let currentUser = null;

  function render() {
    root.innerHTML = `
      <div style="max-width: 1320px; margin: 0 auto; padding: 2rem 1rem;">
        
        <!-- Navigation Topbar -->
        <header style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);">
              <i class="fa-solid fa-shield-halved" style="font-size: 1.5rem; color: white;"></i>
            </div>
            <div>
              <h1 class="font-heading" style="font-size: 1.6rem; font-weight: 900; background: linear-gradient(90deg, #c084fc 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ShieldEDR</h1>
              <p style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">Executive SOC Command Center v4.9</p>
            </div>
          </div>

          <div style="display: flex; align-items: center; gap: 1rem;">
            ${currentUser ? `
              <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(139, 92, 246, 0.3); padding: 0.4rem 1rem; border-radius: 9999px; display: flex; align-items: center; gap: 0.6rem;">
                <i class="fa-solid fa-user-shield" style="color: #34d399;"></i>
                <span style="font-size: 0.85rem; color: #f8fafc; font-weight: 600;">${currentUser.email}</span>
                <button id="btn-logout-header" style="background: none; border: none; color: #f43f5e; margin-left: 0.5rem; cursor: pointer;"><i class="fa-solid fa-right-from-bracket"></i></button>
              </div>
            ` : `
              <button id="btn-login-header" class="btn-gradient-purple">
                <i class="fa-solid fa-lock"></i> Firebase Login
              </button>
            `}
          </div>
        </header>

        <!-- Hero Status Banner -->
        <div class="glass-panel" style="padding: 2.2rem; margin-bottom: 2rem; border-color: rgba(168, 85, 247, 0.35);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.5rem;">
            <div>
              <div class="badge-emerald" style="margin-bottom: 1rem;">
                <span class="pulse-dot"></span> WAZUH SIEM MANAGER & WAF FIREWALL ACTIVE
              </div>
              <h2 class="font-heading" style="font-size: 2.4rem; font-weight: 900; color: #f8fafc; margin-bottom: 0.4rem;">
                24/7 Automated Threat Detection & Active Isolation
              </h2>
              <p style="color: #94a3b8; font-size: 1.05rem;">
                Multi-Tenant Isolation Silo: <code style="color: #c084fc; background: rgba(192, 132, 252, 0.15); padding: 0.2rem 0.6rem; border-radius: 6px;">grp_${currentUser ? currentUser.uid.substring(0, 8) : 'demo01'}</code>
              </p>
            </div>
            <div>
              <a href="#payment-section" class="btn-gradient-purple">
                <i class="fa-solid fa-credit-card"></i> Manage Subscription (₹1,000/yr)
              </a>
            </div>
          </div>
        </div>

        <!-- Metric Grid -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; margin-bottom: 2rem;">
          <div class="glass-panel" style="padding: 1.5rem; border-color: rgba(16, 185, 129, 0.35);">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Protected Endpoints</div>
            <div style="font-size: 2.3rem; font-weight: 900; color: #34d399; margin-top: 0.2rem;">15 Active</div>
            <div style="font-size: 0.82rem; color: #34d399; font-weight: 600; margin-top: 0.4rem;"><i class="fa-solid fa-circle-check"></i> 100% Monitored & Safe</div>
          </div>

          <div class="glass-panel" style="padding: 1.5rem; border-color: rgba(168, 85, 247, 0.35);">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Critical Alerts</div>
            <div style="font-size: 2.3rem; font-weight: 900; color: #c084fc; margin-top: 0.2rem;">0 Threats</div>
            <div style="font-size: 0.82rem; color: #c084fc; font-weight: 600; margin-top: 0.4rem;"><i class="fa-solid fa-shield"></i> All Processes Normal</div>
          </div>

          <div class="glass-panel" style="padding: 1.5rem; border-color: rgba(6, 182, 212, 0.35);">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">WAF Attacks Blocked</div>
            <div style="font-size: 2.3rem; font-weight: 900; color: #38bdf8; margin-top: 0.2rem;">142 Payloads</div>
            <div style="font-size: 0.82rem; color: #38bdf8; font-weight: 600; margin-top: 0.4rem;"><i class="fa-solid fa-fire-flame-curved"></i> SQLi & XSS Mitigated</div>
          </div>

          <div class="glass-panel" style="padding: 1.5rem; border-color: rgba(16, 185, 129, 0.35);">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700; text-transform: uppercase;">Health & Uptime</div>
            <div style="font-size: 2.3rem; font-weight: 900; color: #34d399; margin-top: 0.2rem;">99.98%</div>
            <div style="font-size: 0.82rem; color: #34d399; font-weight: 600; margin-top: 0.4rem;"><i class="fa-solid fa-server"></i> Manager Healthy</div>
          </div>
        </div>

        <!-- PhonePe Payment Section -->
        <div id="payment-section" class="glass-panel" style="padding: 2.2rem; margin-bottom: 2rem; background: linear-gradient(180deg, rgba(46, 16, 101, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%); border-color: #8b5cf6;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 2rem;">
            <div>
              <span style="background: linear-gradient(90deg, #8b5cf6 0%, #ec4899 100%); color: white; padding: 0.35rem 1rem; border-radius: 999px; font-size: 0.8rem; font-weight: 800;">🔥 MSME YEARLY SUBSCRIPTION</span>
              <h3 class="font-heading" style="font-size: 2.2rem; font-weight: 900; color: #ffffff; margin-top: 0.8rem;">
                MSME Enterprise Protection — ₹1,000 / year
              </h3>
              <p style="color: #c084fc; font-weight: bold; font-size: 1.1rem; margin-bottom: 1.2rem;">
                (Just ₹83 / month per computer)
              </p>
              <p style="color: #cbd5e1; font-size: 0.95rem; max-width: 500px;">
                Direct bank transfers with 0% gateway fees via PhonePe, GPay, Paytm, BHIM UPI directly to <b>6305001481@ybl</b>.
              </p>
            </div>

            <div style="background: white; padding: 1.2rem; border-radius: 16px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
              <img src="https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=upi%3A%2F%2Fpay%3Fpa%3D6305001481%40ybl%26pn%3DShieldEDR%2520Security%26am%3D1000%26cu%3DINR" alt="PhonePe UPI QR Code" style="width: 180px; height: 180px; display: block; margin: 0 auto;">
              <p style="color: #0f172a; font-weight: 800; font-size: 0.88rem; margin-top: 0.6rem;">Scan to pay ₹1,000</p>
            </div>
          </div>
        </div>

        <!-- 1-Click Agent Installer Box -->
        <div class="glass-panel" style="padding: 2rem; margin-bottom: 2rem; border-color: rgba(6, 182, 212, 0.4);">
          <h3 class="font-heading" style="color: #38bdf8; font-size: 1.5rem; margin-bottom: 0.5rem;">
            <i class="fa-solid fa-download"></i> 1-Click Agent Installer (Windows Batch Setup)
          </h3>
          <p style="color: #cbd5e1; font-size: 0.95rem; margin-bottom: 1rem;">
            Run this command on your Windows client devices to automatically bind them to your isolated group silo:
          </p>

          <div class="code-container">
            msiexec.exe /i wazuh-agent-4.9.0-1.msi /q WAZUH_MANAGER="10.0.11.57" WAZUH_REGISTRATION_SERVER="10.0.11.57" WAZUH_AGENT_GROUP="grp_${currentUser ? currentUser.uid.substring(0, 8) : 'demo01'}"
          </div>
        </div>

      </div>
    `;

    // Event Listeners
    const btnLoginHeader = document.getElementById('btn-login-header');
    if (btnLoginHeader) {
      btnLoginHeader.addEventListener('click', () => {
        renderAuthModal((user) => {
          currentUser = user;
          render();
        });
      });
    }

    const btnLogoutHeader = document.getElementById('btn-logout-header');
    if (btnLogoutHeader) {
      btnLogoutHeader.addEventListener('click', async () => {
        await logoutUser();
        currentUser = null;
        render();
      });
    }
  }

  // Subscribe to Firebase Auth State Observer
  subscribeAuthState((user) => {
    currentUser = user;
    render();
  });

  render();
}
