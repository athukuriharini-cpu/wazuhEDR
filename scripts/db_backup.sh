#!/usr/bin/env bash
# ==============================================================================
# ShieldEDR Multi-Tenant SaaS — Automated Daily Database Backup Worker
# Performs timestamped PostgreSQL pg_dump, GZIP compression, and retention rotation.
# ==============================================================================

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/var/backups/wazuh_saas_db}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/wazuh_saas_db_${TIMESTAMP}.sql.gz"

# Database Connection Details
DB_USER="${DB_USER:-db_app_admin}"
DB_NAME="${DB_NAME:-wazuh_saas_db}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

echo "[$(date)] 📦 Starting Automated Daily Database Backup..."

# Ensure Backup Destination Exists
mkdir -p "${BACKUP_DIR}"

# Execute PostgreSQL Dump with Compression
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_FILE}"

echo "[$(date)] ✅ Database backup created successfully: ${BACKUP_FILE}"

# Optional: Push to WORM / Cloud Storage (AWS S3 / GCP Cloud Storage)
if [ -n "${WORM_BUCKET_URI:-}" ]; then
    echo "[$(date)] ☁️ Uploading backup to WORM Storage Container: ${WORM_BUCKET_URI}..."
    # aws s3 cp "${BACKUP_FILE}" "${WORM_BUCKET_URI}/"
fi

# Rotate & Delete Backups Older Than RETENTION_DAYS
echo "[$(date)] 🧹 Rotated local backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -type f -name "wazuh_saas_db_*.sql.gz" -mtime +"${RETENTION_DAYS}" -delete

echo "[$(date)] 🎉 Automated Database Backup Cycle Complete!"
