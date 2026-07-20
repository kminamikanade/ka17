$inputText = Read-Host "请输入关键词（多个关键词用空格分开）"

if ([string]::IsNullOrWhiteSpace($inputText)) {
    exit
}

$searchDirs = @(

    "C:\c_wk\10_会社\PDF-相关\4-5-検索 -  PDF -場所と会社名"

    # 其他目录
    "C:\c_wk"
    # "C:\Excel"

)

$keywords = $inputText.Split(
    ' ',
    [System.StringSplitOptions]::RemoveEmptyEntries
)

Write-Host ""
Write-Host "正在搜索..."
Write-Host ""

$results = foreach ($dir in $searchDirs) {

    if (Test-Path $dir) {

        Get-ChildItem $dir -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object {

            $name = $_.Name

            foreach ($kw in $keywords) {

                if ($name -like "*$kw*") {
                    return $true
                }
            }

            return $false
        }
    }
}

if (-not $results) {

    Write-Host "没有找到文件。" -ForegroundColor Yellow
    exit
}

$results = $results | Sort-Object DirectoryName, Name

Write-Host "找到 $($results.Count) 个文件：" -ForegroundColor Green
Write-Host "========================================================"

for ($i = 0; $i -lt $results.Count; $i++) {

    Write-Host "[$($i + 1)] $($results[$i].DirectoryName)  →  $($results[$i].Name)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================================"

while ($true) {

    $choice = Read-Host "输入编号定位文件（直接回车退出）"

    if ([string]::IsNullOrWhiteSpace($choice)) {
        break
    }

    if ($choice -notmatch '^\d+$') {
        continue
    }

    $idx = [int]$choice - 1

    if ($idx -ge 0 -and $idx -lt $results.Count) {

        Start-Process explorer.exe "/select,`"$($results[$idx].FullName)`""
    }
}