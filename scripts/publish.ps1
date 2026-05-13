# Load .env file
Get-Content "$PSScriptRoot\..\.env" | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)\s*$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

npm version patch
$env:NODE_AUTH_TOKEN = $env:NODE_AUTH_TOKEN
npm publish
