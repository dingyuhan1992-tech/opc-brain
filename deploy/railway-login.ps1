$logFile = "$env:TEMP\railway_login.log"
$railway = "$env:APPDATA\npm\railway.cmd"

# Start railway login in background, capture output
Start-Job -Name RailwayLogin -ScriptBlock {
    param($railway, $logFile)
    & $railway login --browserless 2>&1 | Out-File -FilePath $logFile -Encoding utf8
} -ArgumentList $railway, $logFile

Start-Sleep -Seconds 5

# Read the device code from the log
$content = Get-Content $logFile -Raw
Write-Host "=== Railway Login Output ==="
Write-Host $content

# Extract the user code
if ($content -match 'user_code=([A-Z0-9-]+)') {
    $code = $matches[1]
    Write-Host "`n=== DEVICE CODE: $code ==="
    Write-Host "Open https://railway.com/activate and enter: $code"
} elseif ($content -match 'enter this code:\s*([A-Z0-9-]+)') {
    $code = $matches[1].Trim()
    Write-Host "`n=== DEVICE CODE: $code ==="
    Write-Host "Open https://railway.com/activate and enter: $code"
} else {
    Write-Host "Could not extract code from output"
    Write-Host "Full output: $content"
}

# Wait for authentication to complete (polling)
Write-Host "`nWaiting for authentication to complete..."
$maxWait = 300  # 5 minutes
$waited = 0
while ($waited -lt $maxWait) {
    Start-Sleep -Seconds 5
    $waited += 5
    $authContent = & $railway whoami 2>&1
    if ($authContent -notmatch "Unauthorized") {
        Write-Host "Authentication successful!"
        Write-Host $authContent
        break
    }
    if ($waited % 30 -eq 0) {
        Write-Host "Still waiting... ($waited seconds elapsed)"
    }
}
