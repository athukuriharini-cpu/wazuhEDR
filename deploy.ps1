# Deploy ShieldEDR Dashboard to Google Cloud Run & Firebase Hosting
# -----------------------------------------------------------------
# Usage: ./deploy.ps1 -ProjectId "your-gcp-project-id"

param (
    [Parameter(Mandatory=$true)]
    [string]$ProjectId,

    [string]$Region = "us-central1",
    [string]$ServiceName = "shield-edr-dashboard",
    [string]$WazuhHost = "10.0.0.2",
    [string]$WazuhUser = "wazuh-wui",
    [string]$WazuhPass = "wazuh-wui"
)

Write-Host "🚀 Setting GCP Project to: $ProjectId" -ForegroundColor Cyan
gcloud config set project $ProjectId

Write-Host "📦 Building container image with Google Cloud Build..." -ForegroundColor Cyan
gcloud builds submit --tag "gcr.io/$ProjectId/$ServiceName`:latest" .

Write-Host "☁️ Deploying container to Google Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $ServiceName `
    --image "gcr.io/$ProjectId/$ServiceName`:latest" `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --set-env-vars "WAZUH_API_HOST=$WazuhHost,WAZUH_API_USER=$WazuhUser,WAZUH_API_PASS=$WazuhPass,SHIELD_DEMO_MODE=false"

Write-Host "🔥 Deploying Firebase Hosting rewrites..." -ForegroundColor Cyan
firebase deploy --only hosting

Write-Host "✅ Deployment Complete!" -ForegroundColor Green
