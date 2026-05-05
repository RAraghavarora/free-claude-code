#!/bin/bash
# Simple startup script for free-claude-code with Manifest
# This script verifies Manifest is running and starts free-claude-code

set -e

echo "🔍 Checking if Manifest is running on http://localhost:2099..."
if ! curl -s -f http://localhost:2099/api/v1/health > /dev/null 2>&1; then
    echo "❌ Manifest is not running on http://localhost:2099"
    echo "   Please start Manifest first using docker or npm"
    echo "   Docker: cd manifest && docker-compose up -d"
    exit 1
fi

echo "✅ Manifest is running"
echo ""
echo "🚀 Starting free-claude-code..."
echo "   Listening on http://0.0.0.0:8082"
echo ""
echo "   To use with Claude Code CLI, set:"
echo "   export ANTHROPIC_BASE_URL=http://localhost:8082"
echo "   export ANTHROPIC_API_KEY=freecc"
echo ""

# Start the server
cd "$(dirname "$0")"
exec uv run uvicorn server:app --host 0.0.0.0 --port 8082
