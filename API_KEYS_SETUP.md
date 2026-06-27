# API Keys Setup Guide

Get your API keys set up in under 10 minutes!

## 1. Anthropic Claude API Key

### Step 1: Create Account
1. Go to https://console.anthropic.com
2. Click "Sign Up"
3. Use your Google account or email
4. Verify your email

### Step 2: Get $5 Free Credit
- New accounts get $5 in free credits automatically!
- Enough for thousands of searches during development

### Step 3: Create API Key
1. Once logged in, click your profile (top right)
2. Go to "API Keys"
3. Click "Create Key"
4. Name it: `codemind-dev`
5. **Copy the key immediately** (starts with `sk-ant-`)
6. Save it somewhere safe - you won't see it again!

### Cost Estimate
- Sonnet 4.5: ~$3 per 1M input tokens, ~$15 per 1M output tokens
- For CodeMind: ~$0.003 per search query (analyzing code)
- Your $5 credit = ~1,600 searches! 🎉

---

## 2. OpenAI API Key (for Embeddings)

### Step 1: Create Account
1. Go to https://platform.openai.com
2. Click "Sign up"
3. Use your Google account or email
4. Verify your phone number (required)

### Step 2: Add Payment Method
⚠️ **Important**: OpenAI requires a payment method, but embeddings are VERY cheap!
1. Go to "Settings" → "Billing"
2. Click "Add payment method"
3. Add your credit/debit card
4. (Optional) Set a usage limit: $5/month is plenty

### Step 3: Create API Key
1. Go to "API Keys" (left sidebar)
2. Click "Create new secret key"
3. Name it: `codemind-embeddings`
4. **Copy the key immediately** (starts with `sk-`)
5. Save it somewhere safe!

### Cost Estimate
- text-embedding-3-small: $0.02 per 1M tokens
- For CodeMind: ~$0.02 per 1,000 searches
- 1,000 searches = $0.02 (2 cents!) 💰
- Budget $5/month = 250,000 searches

---

## 3. Configure Your Environment

Once you have both keys, add them to your backend `.env` file:

```bash
cd backend
cp .env.example .env
```

Then edit `backend/.env` and add your keys:

```bash
# AI APIs
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# Leave these for later (Supabase setup)
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_SERVICE_KEY=
```

**Security Tips:**
- Never commit `.env` to git (already in `.gitignore`)
- Never share your API keys publicly
- Never put them in frontend code
- Use environment variables for deployment

---

## 4. Test Your Keys

Run this quick test to verify your keys work:

```bash
cd backend
source venv/bin/activate
python3 -c "
from anthropic import Anthropic
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Test Anthropic
try:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    print('✅ Anthropic key works!')
except Exception as e:
    print(f'❌ Anthropic key error: {e}')

# Test OpenAI
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    print('✅ OpenAI key works!')
except Exception as e:
    print(f'❌ OpenAI key error: {e}')
"
```

You should see:
```
✅ Anthropic key works!
✅ OpenAI key works!
```

---

## Troubleshooting

### "Invalid API key" error
- Double-check you copied the entire key
- Make sure there are no spaces or quotes around the key
- In `.env` file, format should be: `KEY=value` (no quotes)
- Try regenerating the key and copying again

### "Insufficient credits" (Anthropic)
- Check your credit balance at https://console.anthropic.com
- If used up $5, add payment method
- Or wait for monthly credit refresh

### "Payment method required" (OpenAI)
- OpenAI requires payment method even for small usage
- Add a card with a $5 limit if concerned
- Embeddings are so cheap you'll barely use anything

### "ModuleNotFoundError"
- Make sure you're in the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

---

## Next Steps

Once your keys are working:

1. ✅ API keys configured
2. ⏭️ Set up Supabase (see [SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md))
3. ⏭️ Index your 203 code examples
4. ⏭️ Start the servers and test!

---

## Cost Summary (Monthly)

Assuming 1,000 searches/month:

| Service | Usage | Cost |
|---------|-------|------|
| OpenAI Embeddings | 1,000 searches | $0.02 |
| Claude Analysis | 1,000 searches | $3.00 |
| **Total** | | **~$3/month** |

For development (100 searches while building):
- OpenAI: < $0.01
- Claude: $0.30
- **Total: ~$0.30** ✅

Your $5 Anthropic credit covers your entire development phase!

---

## Security Checklist

- [ ] API keys stored in `.env` file
- [ ] `.env` file is in `.gitignore`
- [ ] Never committed keys to git
- [ ] Keys not shared publicly
- [ ] (Optional) Set usage limits in OpenAI dashboard

---

**Ready to continue?** Head to [GETTING_STARTED.md](GETTING_STARTED.md) Step 3!
