# 查找不同的文件夹，包括子文件夹，自动创建目标文件夹

# UTF-8 防止中文乱码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8


# =============================
# 查找位置
# =============================

$SourcePaths = @'
C:\c_wk\10_会社\PDF-相关\Test
C:\c_wk\10_会社\PDF-相关\Test2
'@.Trim().Split("`n") |
ForEach-Object { $_.Trim() } |
Where-Object { $_ }



# =============================
# 第一类编号
# 找到这些 → 放到 文件夹1
# =============================

$Folder1Numbers = @'
15QQ
15R
15T

'@.Trim().Split("`n") |
ForEach-Object { $_.Trim() } |
Where-Object { $_ }



# =============================
# 第二类编号
# 找到这些 → 放到 文件夹2
# =============================

$Folder2Numbers = @'
26T00234
1231T4422
'@.Trim().Split("`n") |
ForEach-Object { $_.Trim() } |
Where-Object { $_ }



# =============================
# 目标位置
# =============================

$TargetRoot = 'C:\c_wk\10_会社\PDF-相关\完成'


# 两个文件夹名字
$Folder1Name = "第一类"
$Folder2Name = "第二类"



# 创建总文件夹
if (!(Test-Path $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null
}



$count = 0



# =============================
# 开始查找
# =============================

foreach ($path in $SourcePaths) {


    Get-ChildItem $path -File -Recurse |
    Where-Object {

        $_.Extension.ToLower() -in @(
            ".xls",
            ".xlsx",
            ".pdf",
            ".doc",
            ".docx",
            ".jpg",
            ".jpeg",
            ".png"
        )

    } |
    ForEach-Object {


        $TargetFolder = $null



        # -------------------------
        # 判断第一类
        # -------------------------

        foreach ($num in $Folder1Numbers) {

            if ($_.Name -like "*$num*") {

                $TargetFolder = Join-Path $TargetRoot $Folder1Name

                break
            }
        }



        # -------------------------
        # 判断第二类
        # -------------------------

        if ($null -eq $TargetFolder) {

            foreach ($num in $Folder2Numbers) {

                if ($_.Name -like "*$num*") {

                    $TargetFolder = Join-Path $TargetRoot $Folder2Name

                    break
                }
            }
        }



        # 没有匹配跳过

        if ($null -eq $TargetFolder) {
            return
        }



        # 自动创建分类文件夹

        if (!(Test-Path $TargetFolder)) {

            New-Item `
                -ItemType Directory `
                -Path $TargetFolder `
                -Force | Out-Null
        }



        # 目标文件

        $TargetFile = Join-Path $TargetFolder $_.Name



        Write-Host "=============================="
        Write-Host "地址 : $($_.DirectoryName)"
        Write-Host "文件 : $($_.Name)"
        Write-Host "放入 : $TargetFolder"
        Write-Host ""



        Copy-Item `
            -Path $_.FullName `
            -Destination $TargetFile `
            -Force



        $count++


    }
}



Write-Host ""
Write-Host "=============================="
Write-Host "完成文件数 : $count"
Write-Host "=============================="



Read-Host "Press Enter"