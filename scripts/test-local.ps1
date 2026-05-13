# test-local.ps1 — Copy one or more skills to ~/.agents/skills/ for local testing
# Usage:
#   .\scripts\test-local.ps1                          # installs ALL skills
#   .\scripts\test-local.ps1 rightcode-tdd            # installs one skill
#   .\scripts\test-local.ps1 rightcode-tdd rightcode-diagnose  # installs multiple skills

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$SkillNames
)

$SkillsSource = Join-Path $PSScriptRoot "..\skills"
$SkillsDest   = Join-Path $env:USERPROFILE ".agents\skills"

# Resolve skills to install
if ($SkillNames.Count -eq 0) {
    $skills = Get-ChildItem -Path $SkillsSource -Directory
} else {
    $skills = $SkillNames | ForEach-Object {
        $dir = Join-Path $SkillsSource $_
        if (-not (Test-Path $dir)) {
            Write-Error "Skill not found: $_"
            exit 1
        }
        Get-Item $dir
    }
}

New-Item -ItemType Directory -Force -Path $SkillsDest | Out-Null

foreach ($skill in $skills) {
    $dest = Join-Path $SkillsDest $skill.Name
    if (Test-Path $dest) {
        Remove-Item -Recurse -Force $dest
    }
    Copy-Item -Recurse $skill.FullName $dest
    Write-Host "Installed: $($skill.Name) -> $dest" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done. Reload VS Code (or your agent host) to pick up the changes." -ForegroundColor Cyan
