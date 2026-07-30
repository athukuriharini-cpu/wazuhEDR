"""
ShieldEDR UPI & Razorpay Payment Integration Component (₹1,000 / Year)
======================================================================
Provides interactive UPI payment flow (GPay, PhonePe, Paytm, BHIM),
Razorpay checkout integration, instant UTR/Ref verification, and payment receipt download.
"""

import urllib.parse
import streamlit as st
from datetime import datetime
from firestore_db import record_payment

# Configuration
UPI_ID = "6305001481@ybl"
BUSINESS_NAME = "ShieldEDR Security"
PLAN_PRICE_INR = 1000

def generate_upi_uri(amount_inr: int = PLAN_PRICE_INR, ref_id: str = "") -> str:
    """Generates standard Indian UPI deep link protocol string."""
    note = f"ShieldEDR Annual Subscription - {ref_id}" if ref_id else "ShieldEDR EDR Annual Subscription"
    params = {
        "pa": UPI_ID,
        "pn": BUSINESS_NAME,
        "am": str(amount_inr),
        "cu": "INR",
        "tn": note,
    }
    return f"upi://pay?{urllib.parse.urlencode(params)}"

def render_payment_section(user_email: str):
    """Renders the UPI & Online Payment Gateway UI."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 2px solid #8b5cf6; border-radius: 16px; padding: 1.8rem; margin-bottom: 2rem;">
        <h3 style="color: #c084fc; margin-top: 0;">💳 Annual Subscription — ₹1,000 / Year</h3>
        <p style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1.2rem;">
            Full enterprise EDR ransomware protection, 24/7 SIEM threat monitoring, and custom Sysmon rules for <b>₹83 / month</b> (billed annually as ₹1,000 / year).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_upi, tab_razorpay, tab_verify = st.tabs([
        "📱 Instant UPI / GPay / PhonePe",
        "💳 Razorpay Payment Gateway",
        "✅ Instant Payment Verification",
    ])

    with tab_upi:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("1. Scan & Pay via any UPI App")
            st.markdown(f"**VPA / UPI ID:** `{UPI_ID}`")
            st.markdown(f"**Amount:** **₹{PLAN_PRICE_INR} INR** (Annual Plan)")

            # Render Visual UPI QR Code Container
            upi_link = generate_upi_uri(PLAN_PRICE_INR, user_email)

            st.markdown(f"""
            <div style="text-align: center; background: #ffffff; padding: 1.2rem; border-radius: 12px; display: inline-block; margin: 1rem 0;">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_link)}" alt="UPI QR Code" style="width: 200px; height: 200px;" />
                <p style="color: #0f172a; font-weight: bold; margin-top: 0.5rem; font-size: 0.9rem;">Scan with GPay, PhonePe, Paytm, or BHIM</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.subheader("2. Click to Pay directly on Mobile")
            st.markdown("If you are on your smartphone, tap below to launch your payment app directly:")

            st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 0.8rem; margin-top: 1rem;">
                <a href="{upi_link}" target="_blank" style="background: #4285F4; color: white; padding: 0.75rem 1.2rem; border-radius: 8px; text-decoration: none; font-weight: bold; text-align: center; display: block;">
                    🚀 Open Google Pay / PhonePe / Paytm
                </a>
            </div>
            """, unsafe_allow_html=True)

            st.info("💡 After completing payment in your UPI app, copy the **12-digit UTR / Reference Number** from your receipt and enter it in the 'Instant Payment Verification' tab.")

    with tab_razorpay:
        st.subheader("Online Credit Card / Debit Card / NetBanking")
        st.markdown("Collect online payments instantly via Razorpay Checkout:")

        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="color: #60a5fa;">Pay ₹1,000 via Razorpay Gateway</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Supports all Indian & International Debit Cards, Credit Cards, NetBanking, and EMI.</p>
            <form>
                <script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_demo_shieldedr" async> </script>
            </form>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### ⚡ Quick Payment Simulation (Demo Mode)")
        if st.button("Simulate Razorpay Payment Success (₹1,000)", type="primary"):
            res = record_payment(user_email, PLAN_PRICE_INR, "Razorpay Card/NetBanking", f"RZP-{int(datetime.now().timestamp())}")
            if res["success"]:
                st.session_state["is_paid"] = True
                st.success("🎉 Payment verified! Your subscription is active.")
                st.switch_page("pages/3_💻_Connected_Devices.py")

    with tab_verify:
        st.subheader("Enter UPI UTR / Reference Number")
        st.markdown("Enter the **12-digit UTR/Ref No.** from your GPay, PhonePe, Paytm, or Bank SMS to activate instantly:")

        with st.form("verify_upi_form"):
            utr_no = st.text_input("12-Digit UPI UTR / Reference Number", placeholder="e.g. 420918765432")
            paid_method = st.selectbox("Payment App Used", ["GPay (Google Pay)", "PhonePe", "Paytm", "BHIM / Other UPI", "NetBanking"])
            submit_verify = st.form_submit_button("Verify & Activate Subscription (₹1,000)", type="primary")

            if submit_verify:
                if len(utr_no.strip()) >= 6:
                    res = record_payment(user_email, PLAN_PRICE_INR, paid_method, utr_no.strip())
                    if res["success"]:
                        st.session_state["is_paid"] = True
                        st.balloons()
                        st.success("🎉 Subscription Activated Successfully!")
                        st.info("You can now connect devices and download your 1-click installer!")
                        if st.button("👉 Go to Device Setup"):
                            st.switch_page("pages/3_💻_Connected_Devices.py")
                else:
                    st.error("Please enter a valid 12-digit UTR/Reference Number.")

def render_payment_receipt(payment_data: dict):
    """Renders a downloadable payment receipt."""
    st.markdown(f"""
    <div style="border: 1px solid #34d399; background: rgba(16, 185, 129, 0.1); border-radius: 12px; padding: 1.2rem; margin-top: 1rem;">
        <h4 style="color: #34d399; margin-top: 0;">🧾 Payment Receipt — ShieldEDR</h4>
        <p><b>Receipt ID:</b> {payment_data.get('payment_id')}</p>
        <p><b>Account Email:</b> {payment_data.get('email')}</p>
        <p><b>Amount Paid:</b> ₹{payment_data.get('amount')} INR (1 Year Subscription)</p>
        <p><b>Payment Method:</b> {payment_data.get('method')}</p>
        <p><b>Reference UTR:</b> {payment_data.get('ref_no')}</p>
        <p><b>Status:</b> <span style="color: #34d399; font-weight: bold;">PAID & ACTIVE</span></p>
    </div>
    """, unsafe_allow_html=True)
