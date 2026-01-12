# PowerShell script to create client distribution package
# Run this in PowerShell: .\create-client-package.ps1

Write-Host "Creating mai-tools API Client Package..." -ForegroundColor Cyan

# Create package directory
$packageDir = "mai-tools-api-client"
if (Test-Path $packageDir) {
    Remove-Item $packageDir -Recurse -Force
}
New-Item -ItemType Directory -Path $packageDir | Out-Null

# Copy documentation files
Write-Host "Copying documentation files..." -ForegroundColor Yellow
Copy-Item "API_DOCUMENTATION.md" -Destination $packageDir
Copy-Item "API_QUICK_REFERENCE.md" -Destination $packageDir
Copy-Item "API_INTEGRATION_ARCHITECTURE.md" -Destination $packageDir
Copy-Item "api_demo.html" -Destination $packageDir

# Create API URL file
Write-Host "Creating API URL file..." -ForegroundColor Yellow
$apiUrl = Read-Host "Enter your production API URL (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($apiUrl)) {
    $apiUrl = "https://bamaco-calc-api.onrender.com"
}

@"
mai-tools API Base URL
======================

Production API: $apiUrl

Interactive Docs: ${apiUrl}/docs
OpenAPI Spec: ${apiUrl}/openapi.json

Usage Example:
--------------
const API_BASE_URL = '$apiUrl';

fetch(`${API_BASE_URL}/rating`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ level: 13.7, achievement: 100.3 })
});
"@ | Out-File -FilePath "$packageDir\API_BASE_URL.txt" -Encoding UTF8

# Create README for the package
Write-Host "Creating package README..." -ForegroundColor Yellow
@"
# mai-tools API - Client Integration Package

This package contains everything you need to integrate the mai-tools rating calculator API into your website.

## Files Included

- **API_DOCUMENTATION.md** - Complete API guide with examples and UI recommendations
- **API_QUICK_REFERENCE.md** - Quick lookup for endpoints and code snippets
- **API_INTEGRATION_ARCHITECTURE.md** - System diagrams and integration patterns
- **api_demo.html** - Interactive HTML demo (open in browser to test the API)
- **API_BASE_URL.txt** - Your production API endpoint

## Quick Start

1. **Read the Quick Reference**
   - Open `API_QUICK_REFERENCE.md` for a fast overview of all endpoints

2. **Test the API**
   - Open `api_demo.html` in your browser
   - See all three calculators in action
   - View the source code for implementation examples

3. **Read Full Documentation**
   - Open `API_DOCUMENTATION.md` for complete integration guide
   - Includes React, Vue, and vanilla JavaScript examples
   - UI component recommendations included

4. **Integrate into Your Site**
   - Copy the API base URL from `API_BASE_URL.txt`
   - Follow the code examples in the documentation
   - Implement error handling as documented

## Available Endpoints

- **POST /rating** - Calculate rating for a chart level and achievement
- **POST /rating-range** - Get min/max rating for a level at a specific rank
- **POST /recommended-levels** - Get chart recommendations for a target rating
- **GET /ranks** - Get all rank definitions
- **GET /health** - Health check

## Support

For questions or issues, please refer to the documentation files or contact the API maintainer.

## API Base URL

See `API_BASE_URL.txt` for your production API endpoint.

---

Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@ | Out-File -FilePath "$packageDir\README.txt" -Encoding UTF8

# Create ZIP archive
Write-Host "Creating ZIP archive..." -ForegroundColor Yellow
$zipFile = "mai-tools-api-client.zip"
if (Test-Path $zipFile) {
    Remove-Item $zipFile -Force
}
Compress-Archive -Path "$packageDir\*" -DestinationPath $zipFile

# Cleanup temporary directory
Remove-Item $packageDir -Recurse -Force

Write-Host "`n✅ Client package created successfully!" -ForegroundColor Green
Write-Host "📦 Package: $zipFile" -ForegroundColor Cyan
Write-Host "📁 Contents:" -ForegroundColor Cyan
Write-Host "   - API_DOCUMENTATION.md" -ForegroundColor White
Write-Host "   - API_QUICK_REFERENCE.md" -ForegroundColor White
Write-Host "   - API_INTEGRATION_ARCHITECTURE.md" -ForegroundColor White
Write-Host "   - api_demo.html" -ForegroundColor White
Write-Host "   - API_BASE_URL.txt" -ForegroundColor White
Write-Host "   - README.txt" -ForegroundColor White
Write-Host "`n🚀 Share this ZIP file with websites that want to integrate your API!" -ForegroundColor Green
