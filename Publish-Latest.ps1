param(
    [string]$Message = 'Update journal club presentation',
    [switch]$BuildOnly
)
$ErrorActionPreference = 'Stop'
$sitePath = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$pythonPath = Join-Path $env:LOCALAPPDATA 'Python\pythoncore-3.14-64\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
}
& $pythonPath (Join-Path $sitePath 'build_public_site.py') --check
if ($LASTEXITCODE -ne 0) { throw 'Public-edition checks failed; nothing was published.' }
& $pythonPath (Join-Path $sitePath 'build_public_site.py')
if ($LASTEXITCODE -ne 0) { throw 'Public-edition build failed; nothing was published.' }
if ($BuildOnly) { Write-Output 'Reviewed public bundle rebuilt in site/dist.'; exit 0 }
if (-not (Test-Path -LiteralPath (Join-Path $sitePath '.git'))) {
    throw 'GitHub has not been connected to this isolated site folder. Connect the repository first, or use -BuildOnly.'
}
$repoTop = & git -C $sitePath rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0 -or -not [string]::Equals([System.IO.Path]::GetFullPath($repoTop), $sitePath, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'The Git repository must be this site folder, so private project files cannot be staged.'
}
$remote = & git -C $sitePath remote get-url origin
if ($LASTEXITCODE -ne 0 -or $remote -notmatch '^https://github\.com/[^/]+/[^/]+(?:\.git)?$|^git@github\.com:[^/]+/[^/]+(?:\.git)?$') {
    throw 'A GitHub origin for the selected repository is required.'
}
& git -C $sitePath add -- dist .github/workflows/pages.yml README.md build_public_site.py Publish-Latest.ps1 .gitignore
if ($LASTEXITCODE -ne 0) { throw 'Could not stage the public bundle.' }
& git -C $sitePath diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    & git -C $sitePath commit -m $Message
    if ($LASTEXITCODE -ne 0) { throw 'Could not commit. Check the Git author and authentication settings.' }
} elseif ($LASTEXITCODE -ne 0) { throw 'Could not inspect staged changes.' }
& git -C $sitePath push origin HEAD:main
if ($LASTEXITCODE -ne 0) { throw 'Push failed; the previous published version remains in place.' }
Write-Output 'Pushed the latest public bundle. GitHub Pages will deploy it at the existing site URL.'
