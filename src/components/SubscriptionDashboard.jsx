import React, { useState, useEffect } from 'react';

export default function SubscriptionDashboard() {
  const [tenantData, setTenantData] = useState({
    wazuhGroupId: 'grp_01a2b3c4',
    paymentStatus: 'active',
    planName: 'Annual EDR Protection — ₹1,000 / Year',
    deploymentCommand: 'msiexec.exe /i wazuh-agent-4.9.0-1.msi /q WAZUH_MANAGER="10.0.11.57" WAZUH_AGENT_GROUP="grp_01a2b3c4"'
  });
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(tenantData.deploymentCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div style={{
      fontFamily: "'Inter', sans-serif",
      backgroundColor: '#07090e',
      color: '#f8fafc',
      padding: '2rem',
      borderRadius: '16px',
      border: '1px solid rgba(139, 92, 246, 0.25)',
      boxShadow: '0 20px 40px -15px rgba(0, 0, 0, 0.7)'
    }}>
      {/* Header Banner */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.95) 100%)',
        border: '1px solid rgba(168, 85, 247, 0.35)',
        borderRadius: '16px',
        padding: '1.8rem',
        marginBottom: '2rem'
      }}>
        <span style={{
          background: 'rgba(16, 185, 129, 0.15)',
          color: '#34d399',
          border: '1px solid rgba(16, 185, 129, 0.35)',
          padding: '0.35rem 0.9rem',
          borderRadius: '9999px',
          fontSize: '0.82rem',
          fontWeight: 700
        }}>
          ✅ SUBSCRIPTION ACTIVE (₹1,000 / YEAR)
        </span>
        <h1 style={{
          fontSize: '2.2rem',
          fontWeight: 900,
          color: '#f8fafc',
          marginTop: '0.6rem',
          marginBottom: '0.3rem'
        }}>
          Multi-Tenant Isolation Silo
        </h1>
        <p style={{ color: '#94a3b8', fontSize: '1rem', margin: 0 }}>
          Assigned Dedicated Tenant Group: <code style={{ color: '#c084fc', background: 'rgba(192, 132, 252, 0.15)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>{tenantData.wazuhGroupId}</code>
        </p>
      </div>

      {/* 1-Click Deployment Script Box */}
      <div style={{
        background: 'rgba(15, 23, 42, 0.75)',
        border: '1px solid rgba(6, 182, 212, 0.35)',
        borderRadius: '16px',
        padding: '1.8rem',
        marginBottom: '2rem'
      }}>
        <h3 style={{ color: '#38bdf8', marginTop: 0, marginBottom: '0.5rem' }}>
          🚀 1-Click Endpoint Agent Installation Command
        </h3>
        <p style={{ color: '#cbd5e1', fontSize: '0.95rem', marginBottom: '1rem' }}>
          Run this command on your Windows, Linux, or macOS client devices to automatically bind them to your isolated group silo:
        </p>

        <div style={{
          position: 'relative',
          background: '#0b0f19',
          border: '1px solid rgba(148, 163, 184, 0.2)',
          borderRadius: '10px',
          padding: '1.2rem',
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: '0.9rem',
          color: '#34d399',
          overflowX: 'auto'
        }}>
          <code>{tenantData.deploymentCommand}</code>
          <button
            onClick={handleCopy}
            style={{
              position: 'absolute',
              top: '0.8rem',
              right: '0.8rem',
              background: copied ? '#10b981' : '#8b5cf6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              padding: '0.4rem 0.8rem',
              fontWeight: 'bold',
              cursor: 'pointer',
              fontSize: '0.8rem'
            }}
          >
            {copied ? 'Copied!' : 'Copy Command'}
          </button>
        </div>
      </div>
    </div>
  );
}
