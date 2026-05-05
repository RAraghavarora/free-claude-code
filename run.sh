#!/bin/bash
# Quick Start: free-claude-code with Manifest
# This single command starts free-claude-code configured to use Manifest

set -e

cd "$(dirname "$0")"

echo "🚀 Starting free-claude-code with Manifest integration"
echo ""
echo "📋 Configuration:"
echo "   • Manifest URL: http://localhost:2099/v1"
echo "   • free-claude-code: http://0.0.0.0:8082"
echo "   • Models: manifest/auto (all tiers)"
echo ""

# Check if Manifest is running
echo "🔍 Checking Manifest..."
if curl -s -f http://localhost:2099/api/v1/health > /dev/null 2>&1; then
    echo "✅ Manifest is running"
else
    echo "⚠️  Manifest is not responding on http://localhost:2099"
    echo "   Make sure Manifest is running before using free-claude-code"
    echo ""
fi

echo ""
echo "📖 To use with Claude Code CLI, run:"
echo "   export ANTHROPIC_BASE_URL=http://localhost:8082"
echo "   export ANTHROPIC_API_KEY=freecc"
echo "   claude"
echo ""
echo "Starting server..."
echo ""

exec uv run uvicorn server:app --host 0.0.0.0 --port 8082
