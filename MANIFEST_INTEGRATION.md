# Using free-claude-code with Manifest

This guide explains how to use free-claude-code with [Manifest](https://github.com/manifestdotbuild/manifest), a smart model router for personal AI agents.

## What is Manifest?

Manifest is a smart router that sits between an agent and its LLM providers. It scores each request and routes it to the cheapest model that can handle it. The dashboard tracks costs, tokens, and messages across any agent that speaks OpenAI-compatible HTTP.

## Why Use Manifest with free-claude-code?

1. **Cost Optimization**: Manifest automatically routes simple requests to cheaper models and complex requests to more capable models
2. **Multi-Provider Support**: Manifest supports providers that free-claude-code doesn't natively support
3. **Analytics Dashboard**: Track your usage, costs, and token consumption in real-time
4. **Automatic Fallbacks**: If one provider fails, Manifest can automatically fall back to another

## Setup

### 1. Install and Start Manifest

Follow the [Manifest installation guide](https://manifest.build/docs/self-hosted) or use Docker:

```bash
# Using Docker (recommended)
docker pull manifestdotbuild/manifest:latest
docker run -d \
  --name manifest \
  -p 2099:3001 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e BETTER_AUTH_SECRET=$(openssl rand -hex 32) \
  manifestdotbuild/manifest:latest
```

Verify Manifest is running:
```bash
curl http://localhost:2099/api/v1/health
```

### 2. Configure Manifest

1. Open the Manifest dashboard at `http://localhost:2099`
2. Create an account or sign in
3. Create a new agent (e.g., "claude-code-agent")
4. Configure your LLM providers (add API keys for OpenAI, Anthropic, etc.)
5. Set up routing tiers (simple/standard/complex/reasoning)
6. Copy your agent's API key (starts with `mnfst_`)

### 3. Configure free-claude-code

Edit `.env` in the free-claude-code directory:

```bash
# Manifest Config
MANIFEST_BASE_URL="http://localhost:2099/v1"

# Use Manifest's "auto" model for all requests
MODEL_OPUS="manifest/auto"
MODEL_SONNET="manifest/auto"
MODEL_HAIKU="manifest/auto"
MODEL="manifest/auto"

# Set your auth token
ANTHROPIC_AUTH_TOKEN="freecc"
```

The `manifest/auto` model name tells Manifest to automatically select the best model based on request complexity.

### 4. Start free-claude-code

Use the provided startup script:

```bash
./start-with-manifest.sh
```

Or start manually:

```bash
uv run uvicorn server:app --host 0.0.0.0 --port 8082
```

### 5. Configure Claude Code CLI

Point Claude Code at free-claude-code:

```bash
# Bash/Zsh
export ANTHROPIC_BASE_URL=http://localhost:8082
export ANTHROPIC_API_KEY=freecc

# PowerShell
$env:ANTHROPIC_BASE_URL = "http://localhost:8082"
$env:ANTHROPIC_API_KEY = "freecc"
```

## How It Works

```
┌──────────────────┐
│   Claude Code    │
│       CLI        │
└─────────┬────────┘
          │ Anthropic Messages API
          ▼
┌──────────────────┐
│ free-claude-code │ ◄── Converts Anthropic format to OpenAI format
└─────────┬────────┘
          │ OpenAI Chat Completions API
          ▼
┌──────────────────┐
│    Manifest      │ ◄── Routes to best model based on complexity
└─────────┬────────┘
          │
    ┌─────┴─────┬─────────┬──────────┐
    ▼           ▼         ▼          ▼
┌────────┐  ┌────────┐ ┌────────┐ ┌────────┐
│ OpenAI │  │Anthropic│ │ Gemini │ │ Local  │
└────────┘  └────────┘ └────────┘ └────────┘
```

## Model Routing

When you use `manifest/auto`, Manifest will:

1. **Analyze the request**: Score it based on complexity (keyword analysis, tool use, thinking requirements)
2. **Select a tier**: Route to simple/standard/complex/reasoning tier
3. **Choose a model**: Pick the cheapest model in that tier that you've configured
4. **Execute**: Send the request to the selected provider

Example routing (your tiers may differ):
- Simple question → GPT-4o-mini
- Code generation → Claude 3.5 Sonnet
- Complex reasoning → Claude 3.5 Opus or o1
- Local-only mode → Ollama llama3

## Monitoring

View your usage in the Manifest dashboard:
- Real-time token usage and costs
- Per-model and per-tier analytics
- Request logs with routing decisions
- Cost projections and alerts

## Troubleshooting

### Manifest connection fails

```
⏺ Provider API request failed.
  Request ID: req_...
```

**Solution**: Verify Manifest is running:
```bash
curl http://localhost:2099/api/v1/health
```

### Authentication errors

**Solution**: Make sure `ANTHROPIC_AUTH_TOKEN` in `.env` matches what Claude Code is sending:
```bash
# In .env
ANTHROPIC_AUTH_TOKEN="freecc"

# When running claude
export ANTHROPIC_API_KEY=freecc
```

### No models available

**Solution**: Configure at least one provider in the Manifest dashboard and assign models to tiers.

### Slow responses

**Solution**: 
1. Check Manifest dashboard for provider timeouts
2. Verify your provider API keys are valid
3. Check your internet connection
4. Consider using local models for faster responses

## Advanced Configuration

### Use specific Manifest models

Instead of `manifest/auto`, you can target specific models:

```bash
# Use a specific model
MODEL_OPUS="manifest/claude-3-5-sonnet-20241022"
MODEL_SONNET="manifest/gpt-4o"
MODEL_HAIKU="manifest/gpt-4o-mini"
```

### Change Manifest port

If your Manifest instance runs on a different port:

```bash
MANIFEST_BASE_URL="http://localhost:YOUR_PORT/v1"
```

### Use Manifest with other providers

You can mix Manifest with direct provider access:

```bash
# Route Opus to Manifest, but use direct NVIDIA NIM for others
MODEL_OPUS="manifest/auto"
MODEL_SONNET="nvidia_nim/nvidia/nemotron-super-70b"
MODEL_HAIKU="nvidia_nim/nvidia/llama-3.1-nemotron-70b-instruct"
```

## Benefits Over Direct Provider Access

1. **Cost savings**: 30-70% cost reduction through smart routing
2. **Better reliability**: Automatic fallbacks if a provider is down
3. **Unified analytics**: Track all usage in one dashboard
4. **No code changes**: Just point free-claude-code at Manifest
5. **Provider abstraction**: Switch providers without reconfiguring clients

## Next Steps

- Read the [Manifest documentation](https://manifest.build/docs)
- Configure [routing tiers](https://manifest.build/docs/routing) for your workload
- Set up [cost alerts](https://manifest.build/docs/notifications)
- Try [specificity routing](https://manifest.build/docs/specificity) for task-specific models
