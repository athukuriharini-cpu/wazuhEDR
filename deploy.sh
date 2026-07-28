#!/usr/bin/env bash
# ==============================================================================
# ShieldEDR / Wazuh EDR One-Command Ubuntu Deployment Script
# Optimized for Budget Linux Cloud Servers (4GB - 8GB RAM)
# Target OS: Ubuntu 20.04 / 22.04 / 24.04 LTS
# ==============================================================================

set -euo pipefail

# ANSI Color Definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Helper Logging Functions
info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

echo -e "${CYAN}${BOLD}"
echo "=============================================================================="
echo "    🛡️ ShieldEDR — Automated Wazuh EDR Platform Installer (MSME Edition)    "
echo "=============================================================================="
echo -e "${NC}"

# ------------------------------------------------------------------------------
# 1. System Pre-Flight Checks
# ------------------------------------------------------------------------------
info "Performing pre-flight environment checks..."

# Root / Sudo Check
if [ "$EUID" -ne 0 ]; then
    error "This deployment script must be run as root or with sudo privileges: sudo ./deploy.sh"
fi

# RAM Assessment
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_MB=$((TOTAL_RAM_KB / 1024))
info "Detected System RAM: ${TOTAL_RAM_MB} MB"

if [ "$TOTAL_RAM_MB" -lt 3500 ]; then
    warn "System RAM is below 4GB (${TOTAL_RAM_MB} MB). Wazuh Indexer may experience memory pressure."
    warn "Recommendation: Add a 2GB-4GB swap file using 'fallocate -l 4G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile'"
else
    success "RAM check passed (${TOTAL_RAM_MB} MB available)."
fi

# ------------------------------------------------------------------------------
# 2. Linux Kernel Optimization for OpenSearch / Wazuh Indexer
# ------------------------------------------------------------------------------
info "Configuring kernel parameters (vm.max_map_count)..."
CURRENT_MAX_MAP=$(sysctl -n vm.max_map_count 2>/dev/null || echo 0)

if [ "$CURRENT_MAX_MAP" -lt 262144 ]; then
    info "Setting vm.max_map_count=262144..."
    sysctl -w vm.max_map_count=262144
    if ! grep -q "vm.max_map_count=262144" /etc/sysctl.conf; then
        echo "vm.max_map_count=262144" >> /etc/sysctl.conf
    fi
    success "Kernel setting vm.max_map_count updated permanently."
else
    success "Kernel setting vm.max_map_count is already optimal ($CURRENT_MAX_MAP)."
fi

# ------------------------------------------------------------------------------
# 3. Docker & Docker Compose Dependency Verification / Installation
# ------------------------------------------------------------------------------
info "Checking Docker and Docker Compose availability..."

if ! command -v docker &> /dev/null; then
    info "Docker is not installed. Installing Docker Engine automatically..."
    apt-get update -qq
    apt-get install -y -qq curl ca-certificates gnupg lsb-release
    curl -fsSL https://get.docker.com | bash
    systemctl enable --now docker
    success "Docker installed successfully."
else
    success "Docker is already installed ($(docker --version))."
fi

if ! docker compose version &> /dev/null; then
    info "Docker Compose plugin is not installed. Installing docker-compose-plugin..."
    apt-get update -qq
    apt-get install -y -qq docker-compose-plugin
    success "Docker Compose plugin installed successfully."
else
    success "Docker Compose plugin is active ($(docker compose version --short))."
fi

# ------------------------------------------------------------------------------
# 4. Verify Project Files Readiness
# ------------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

info "Verifying deployment configuration files in $SCRIPT_DIR..."

if [ ! -f "$SCRIPT_DIR/docker-compose.yml" ]; then
    error "Missing docker-compose.yml in $SCRIPT_DIR."
fi

if [ ! -f "$SCRIPT_DIR/local_rules.xml" ]; then
    error "Missing local_rules.xml in $SCRIPT_DIR."
fi

success "All required deployment files verified."

# ------------------------------------------------------------------------------
# 5. Launch Wazuh EDR Container Stack
# ------------------------------------------------------------------------------
info "Starting ShieldEDR Stack via Docker Compose..."
docker compose down --remove-orphans 2>/dev/null || true
docker compose up -d --build

info "Waiting for Wazuh Indexer and Manager healthchecks (this may take 45-60 seconds)..."

RETRY_COUNT=0
MAX_RETRIES=20
HEALTHY=false

while [ "$RETRY_COUNT" -lt "$MAX_RETRIES" ]; do
    INDEXER_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' wazuh.indexer 2>/dev/null || echo '"unknown"')
    MANAGER_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' wazuh.manager 2>/dev/null || echo '"unknown"')
    
    if [ "$INDEXER_STATUS" == '"healthy"' ] && [ "$MANAGER_STATUS" == '"healthy"' ]; then
        HEALTHY=true
        break
    fi
    
    echo -n "."
    sleep 5
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

echo ""
if [ "$HEALTHY" = true ]; then
    success "All Wazuh EDR containers are healthy and operational!"
else
    warn "Containers launched. Some services are still warming up or healthchecks pending."
fi

# ------------------------------------------------------------------------------
# 6. Deployment Summary & Access Credentials
# ------------------------------------------------------------------------------
SERVER_IP=$(hostname -I | awk '{print $1}')

echo -e "\n${GREEN}${BOLD}=============================================================================="
echo "    🎉 ShieldEDR Deployment Complete! Platform Access Details                "
echo "==============================================================================${NC}"
echo -e "${CYAN}📊 ShieldEDR Light Dashboard:${NC}   http://${SERVER_IP}:8501"
echo -e "${CYAN}🛡️ Wazuh SIEM Dashboard:${NC}        https://${SERVER_IP}:8443"
echo -e "${CYAN}⚙️ Wazuh REST API:${NC}              https://${SERVER_IP}:55000"
echo -e "${CYAN}🔑 Default Wazuh Credentials:${NC}   Username: ${BOLD}admin${NC} | Password: ${BOLD}SecretPassword1!${NC}"
echo -e "${CYAN}📜 Custom MSME Ruleset:${NC}        Active at /var/ossec/etc/rules/local_rules.xml"
echo -e "${CYAN}💻 Agent Registration Port:${NC}    1515/tcp & 1514/udp"
echo -e "=============================================================================="
echo -e "${YELLOW}Quick Windows Agent Install Command:${NC}"
echo -e "  msiexec.exe /i wazuh-agent-4.9.0-1.msi /q WAZUH_MANAGER='${SERVER_IP}' WAZUH_REGISTRATION_SERVER='${SERVER_IP}'"
echo -e "${GREEN}==============================================================================${NC}\n"
