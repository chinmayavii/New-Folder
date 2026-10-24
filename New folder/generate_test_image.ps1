Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap 500, 200
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::White)
$font = New-Object System.Drawing.Font('Arial', 16, [System.Drawing.FontStyle]::Bold)
$brush = [System.Drawing.Brushes]::Black
$text = "PHYSICS FORMULAS - UNIT 3`n`n1. Ohm's Law: V = I * R`n2. Electric Power: P = V * I`n3. Joule's Heating Law: H = I^2 * R * t"
$g.DrawString($text, $font, $brush, 20, 20)
$bmp.Save("sample_notes\Sample_Physics_Notes.png", [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
$g.Dispose()
Write-Host "Created sample_notes\Sample_Physics_Notes.png"
