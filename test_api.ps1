# Test the Crypto Agent API
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    message = "BTC"
} | ConvertTo-Json

Write-Host "Testing Crypto Agent API..." -ForegroundColor Cyan
Write-Host "Endpoint: http://localhost:8000/api/chat" -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method Post -Headers $headers -Body $body
    Write-Host "`nSuccess!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Cyan
    Write-Host $response.response -ForegroundColor White
} catch {
    Write-Host "`nError:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
