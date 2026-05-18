# test-local.ps1 — Copy one or more skills to ~/.agents/skills/ and ~/.bob/skills/ for local testing
# Usage:
#   .\scripts\test-local.ps1                          # installs ALL skills
#   .\scripts\test-local.ps1 rc-tdd            # installs one skill
#   .\scripts\test-local.ps1 rc-tdd rc-diagnose  # installs multiple skills

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$SkillNames
)

$SkillsSource = Join-Path $PSScriptRoot "..\skills"

# Install targets: ~/.agents/skills/ (GitHub Copilot, Claude Code, Cursor, etc.)
#                  ~/.bob/skills/    (IBM Bob)
$SkillsDestAgents = Join-Path $env:USERPROFILE ".agents\skills"
$SkillsDestBob    = Join-Path $env:USERPROFILE ".bob\skills"

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

foreach ($destRoot in @($SkillsDestAgents, $SkillsDestBob)) {
    New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

    foreach ($skill in $skills) {
        $dest = Join-Path $destRoot $skill.Name
        if (Test-Path $dest) {
            Remove-Item -Recurse -Force $dest
        }
        Copy-Item -Recurse $skill.FullName $dest
        Write-Host "Installed: $($skill.Name) -> $dest" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Done. Reload your agent host (VS Code, IBM Bob, etc.) to pick up the changes." -ForegroundColor Cyan
