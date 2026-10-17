# ── MySQL Password Reset + CloudHire Full Setup ─────────────────────────────
# Run this script in PowerShell as ADMINISTRATOR

Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   CloudHire MySQL Setup Script" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan

$MYSQL_BIN = "C:\Program Files\MySQL\MySQL Server 8.0\bin"
$NEW_PASSWORD = "CloudHire@123"

# Step 1: Stop MySQL service
Write-Host "`n[1/5] Stopping MySQL service..." -ForegroundColor Yellow
net stop MySQL80 2>&1 | Out-Null
Start-Sleep -Seconds 3
Write-Host "      MySQL stopped." -ForegroundColor Green

# Step 2: Start mysqld with skip-grant-tables (safe mode)
Write-Host "`n[2/5] Starting MySQL in safe mode..." -ForegroundColor Yellow
$safeModeProcess = Start-Process -FilePath "$MYSQL_BIN\mysqld.exe" `
    -ArgumentList "--skip-grant-tables", "--skip-networking", "--console" `
    -NoNewWindow -PassThru
Start-Sleep -Seconds 5
Write-Host "      MySQL safe mode running." -ForegroundColor Green

# Step 3: Reset root password
Write-Host "`n[3/5] Resetting root password to: $NEW_PASSWORD" -ForegroundColor Yellow
$sql = "FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY '$NEW_PASSWORD'; FLUSH PRIVILEGES;"
& "$MYSQL_BIN\mysql.exe" -u root --connect-timeout=10 -e $sql 2>&1
Start-Sleep -Seconds 2
Write-Host "      Password reset done." -ForegroundColor Green

# Step 4: Stop safe mode mysqld, restart normal service
Write-Host "`n[4/5] Restarting MySQL normally..." -ForegroundColor Yellow
Stop-Process -Id $safeModeProcess.Id -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
net start MySQL80 2>&1 | Out-Null
Start-Sleep -Seconds 5
Write-Host "      MySQL service restarted." -ForegroundColor Green

# Step 5: Create the database
Write-Host "`n[5/5] Creating cloudhire_db database..." -ForegroundColor Yellow
& "$MYSQL_BIN\mysql.exe" -u root "--password=$NEW_PASSWORD" `
    -e "CREATE DATABASE IF NOT EXISTS cloudhire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; SHOW DATABASES;" 2>&1
Write-Host "      Database created!" -ForegroundColor Green

Write-Host "`n═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host " ✅ MySQL setup complete!" -ForegroundColor Green
Write-Host "    New root password: $NEW_PASSWORD" -ForegroundColor White
Write-Host "    Database: cloudhire_db" -ForegroundColor White
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
