# Load .env file
Get-Content "$PSScriptRoot\..\.env" | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*)\s*$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}

npm version patch
npm config set "//registry.npmjs.org/:_authToken" $env:NODE_AUTH_TOKEN
npm publish
