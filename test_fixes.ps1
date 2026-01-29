# Test the Crypto Agent API with fixes
$headers = @{
    "Content-Type" = "application/json"
}

Write-Host "`n=== Testing Fixed Crypto Agent ===" -ForegroundColor Cyan
Write-Host "Server: http://localhost:8001" -ForegroundColor Yellow

# Test 1: BTC from Knowledge Base
Write-Host "`n[Test 1] Querying BTC (should use Knowledge Base)..." -ForegroundColor Cyan
$body1 = @{ message = "BTC" } | ConvertTo-Json
try {
    $response1 = Invoke-RestMethod -Uri "http://localhost:8001/api/chat" -Method Post -Headers $headers -Body $body1
    Write-Host "Success!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor White
    Write-Host $response1.response -ForegroundColor Gray
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: ETH from Knowledge Base
Write-Host "`n[Test 2] Querying Ethereum (should use Knowledge Base)..." -ForegroundColor Cyan
$body2 = @{ message = "Ethereum" } | ConvertTo-Json
try {
    $response2 = Invoke-RestMethod -Uri "http://localhost:8001/api/chat" -Method Post -Headers $headers -Body $body2
    Write-Host "Success!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor White
    Write-Host $response2.response -ForegroundColor Gray
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Unknown coin (should use API)
Write-Host "`n[Test 3] Querying ADA (might use API fallback)..." -ForegroundColor Cyan
$body3 = @{ message = "ADA" } | ConvertTo-Json
try {
    $response3 = Invoke-RestMethod -Uri "http://localhost:8001/api/chat" -Method Post -Headers $headers -Body $body3
    Write-Host "Success!" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor White
    Write-Host $response3.response -ForegroundColor Gray
}
catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== All Tests Complete ===" -ForegroundColor Cyan
