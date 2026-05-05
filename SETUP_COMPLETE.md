# ✅ FREE-CLAUDE-CODE + MANIFEST INTEGRATION COMPLETE

## 🎯 What Changed

I've successfully integrated Manifest as a provider in free-claude-code. Here's what was added:

### New Files
1. **`providers/manifest/__init__.py`** - Manifest provider module
2. **`providers/manifest/client.py`** - OpenAI-compatible Manifest client
3. **`run.sh`** - Single command to start free-claude-code (use this!)
4. **`MANIFEST_INTEGRATION.md`** - Complete integration guide
5. **`start-with-manifest.sh`** - Alternative startup with health checks

### Modified Files
1. **`.env`** - Configured to use `manifest/auto` for all models
2. **`config/provider_catalog.py`** - Added Manifest provider descriptor
3. **`config/settings.py`** - Added `manifest_base_url` and `manifest_proxy` settings
4. **`providers/registry.py`** - Added Manifest provider factory
5. **`providers/defaults.py`** - Exported `MANIFEST_DEFAULT_BASE`
6. **`smoke/lib/config.py`** - Added Manifest smoke test support
7. **`.env.example`** - Updated with Manifest configuration

## 🚀 Quick Start - Single Command

### Prerequisites
1. **Start Manifest** (must be running first):
   ```bash
   # Using Docker (recommended)
   docker run -d \
     --name manifest \
     -p 2099:3001 \
     -e DATABASE_URL=postgresql://user:pass@host/db \
     -e BETTER_AUTH_SECRET=$(openssl rand -hex 32) \
     manifestdotbuild/manifest:latest
   
   # Or if you have it installed already
   cd /path/to/manifest && npm start
   ```

2. **Verify Manifest is running**:
   ```bash
   curl http://localhost:2099/api/v1/health
   ```

### Start free-claude-code

**Single command to run from any project directory:**

```bash
cd /Users/raghav/raghav/free-claude-code && ./run.sh
```

That's it! The server will start on `http://0.0.0.0:8082`

### Use with Claude Code

```bash
# Set environment variables
export ANTHROPIC_BASE_URL=http://localhost:8082
export ANTHROPIC_API_KEY=freecc

# Run Claude Code from any directory
cd /your/project
claude
```

## 🔄 How It Works

```
Claude Code CLI
    ↓ (Anthropic Messages API)
free-claude-code
    ↓ (Converts to OpenAI format)
Manifest @ localhost:2099
    ↓ (Routes based on complexity)
Your configured providers (OpenAI, Anthropic, Gemini, Ollama, etc.)
```

The flow:
1. Claude Code sends Anthropic Messages API requests to free-claude-code
2. free-claude-code's Manifest provider converts them to OpenAI format
3. Manifest routes each request to the optimal model based on complexity scoring
4. Responses flow back through the same chain

## ⚙️ Configuration

Your current `.env` is configured as:

```bash
MANIFEST_BASE_URL="http://localhost:2099/v1"
MODEL_OPUS="manifest/auto"
MODEL_SONNET="manifest/auto"
MODEL_HAIKU="manifest/auto"
MODEL="manifest/auto"
ANTHROPIC_AUTH_TOKEN="freecc"
```

### What `manifest/auto` Means

The `auto` model tells Manifest to automatically select the best model for each request based on:
- Complexity scoring (keywords, tool use, reasoning requirements)
- Your configured routing tiers in Manifest dashboard
- Cost optimization (cheapest model that can handle the request)

Example routing (depends on your Manifest configuration):
- `"What is 2+2?"` → GPT-4o-mini (simple)
- `"Write a Python function"` → Claude 3.5 Sonnet (standard)
- `"Design a distributed system"` → Claude 3.5 Opus (complex)
- `"Solve this math proof"` → o1 (reasoning)

## 📊 Monitoring

View your usage in the Manifest dashboard:
```bash
open http://localhost:2099
```

You'll see:
- Real-time token usage and costs
- Per-model and per-tier analytics
- Request routing decisions
- Cost projections and alerts

## 🔧 Troubleshooting

### Error: "Provider API request failed"

**Cause**: Manifest is not running or not accessible

**Fix**:
```bash
# Check if Manifest is running
curl http://localhost:2099/api/v1/health

# Restart Manifest if needed
docker restart manifest

# Check logs
docker logs manifest
```

### Error: "Unknown provider_type: 'manifest'"

**Cause**: Old code cached, dependencies not synced

**Fix**:
```bash
cd /Users/raghav/raghav/free-claude-code
uv sync
uv run uvicorn server:app --host 0.0.0.0 --port 8082
```

### Slow responses

**Cause**: Manifest routing overhead or provider timeouts

**Fix**:
1. Check Manifest dashboard for slow providers
2. Configure faster models in your tiers
3. Use local models (Ollama) for development

### No models available

**Cause**: No providers configured in Manifest

**Fix**:
1. Open Manifest dashboard at http://localhost:2099
2. Go to Settings → Routing
3. Add at least one provider (OpenAI, Anthropic, etc.)
4. Assign models to tiers

## 📚 Next Steps

1. **Configure Manifest providers**: Add your API keys in the Manifest dashboard
2. **Set up routing tiers**: Configure which models to use for simple/standard/complex/reasoning
3. **Monitor costs**: Set up cost alerts in Manifest
4. **Try specificity routing**: Configure task-specific routing (coding, data analysis, etc.)

## 📖 Documentation

- **Full Integration Guide**: See `MANIFEST_INTEGRATION.md`
- **Manifest Docs**: https://manifest.build/docs
- **free-claude-code README**: See `README.md`

## 🎉 What You Get

1. **Cost Optimization**: 30-70% savings through smart routing
2. **Multi-Provider Support**: Access any provider Manifest supports
3. **Automatic Fallbacks**: If one provider fails, Manifest tries another
4. **Unified Analytics**: Track all usage in one dashboard
5. **Zero Code Changes**: Just point free-claude-code at Manifest

## 🛠️ Advanced Usage

### Use specific models instead of `auto`

```bash
# In .env
MODEL_OPUS="manifest/claude-3-5-sonnet-20241022"
MODEL_SONNET="manifest/gpt-4o"
MODEL_HAIKU="manifest/gpt-4o-mini"
```

### Mix Manifest with direct providers

```bash
# Route Opus to Manifest, others to NVIDIA NIM
MODEL_OPUS="manifest/auto"
MODEL_SONNET="nvidia_nim/nvidia/nemotron-super-70b"
MODEL_HAIKU="nvidia_nim/nvidia/llama-3.1-nemotron-70b-instruct"
```

### Change Manifest port

```bash
# If Manifest runs on a different port
MANIFEST_BASE_URL="http://localhost:3001/v1"
```

## 💡 Tips

1. **Start simple**: Use `manifest/auto` to let Manifest handle routing
2. **Monitor first week**: Check the dashboard to see routing patterns
3. **Tune tiers**: Adjust your Manifest tiers based on actual usage
4. **Set cost alerts**: Get notified before hitting budget limits
5. **Use local models**: Configure Ollama in Manifest for free development

Enjoy your cost-optimized, multi-provider Claude Code setup! 🚀
