#!/bin/bash

# Load .env file
if [ -f "$(dirname "$0")/../.env" ]; then
    set -a
    source "$(dirname "$0")/../.env"
    set +a
fi

npm version patch
npm config set "//registry.npmjs.org/:_authToken" "$NODE_AUTH_TOKEN"
npm publish
