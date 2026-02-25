# 🚀 Morare — Complete Deployment Guide
## GitHub + Netlify + Anthropic API · All Free

---

## What you're deploying

```
morare/
├── public/
│   └── index.html          ← The entire app
├── netlify/
│   └── functions/
│       └── daily.js        ← Serverless function (hides your API key)
└── netlify.toml            ← Netlify configuration
```

---

## STEP 1 — Get your free Anthropic API key

1. Go to **https://console.anthropic.com**
2. Sign up for a free account
3. Go to **API Keys** → click **Create Key**
4. Copy the key — it looks like: `sk-ant-api03-xxxxx...`
5. Store it somewhere safe (you'll need it in Step 4)

> 💡 You get **$5 free credit** on signup — enough for ~20,000 story generations.
> Claude Haiku (what Morare uses) costs ~$0.00025 per call.

---

## STEP 2 — Push your project to GitHub

### Option A: Using GitHub Desktop (easiest)
1. Download **GitHub Desktop** from desktop.github.com
2. Open it → **File → New Repository**
3. Name it `morare`, set the local path to where you saved the `morare/` folder
4. Click **Create Repository**
5. Click **Publish repository** → make it **Private** (your API key stays server-side, but no need to make it public)
6. Done ✓

### Option B: Using terminal
```bash
cd morare
git init
git add .
git commit -m "Initial Morare deploy"
gh repo create morare --private --source=. --push
```

---

## STEP 3 — Connect to Netlify

1. Go to **https://app.netlify.com** and sign up (free)
2. Click **Add new site → Import an existing project**
3. Choose **Deploy with GitHub**
4. Authorize Netlify → select your `morare` repository
5. Build settings will auto-detect from `netlify.toml`:
   - **Publish directory:** `public`
   - **Functions directory:** `netlify/functions`
6. Click **Deploy site**

Netlify will give you a URL like `https://random-name-123.netlify.app`

---

## STEP 4 — Add your API key (THE IMPORTANT STEP)

This is how your key stays secret — it lives on Netlify's servers, never in your code.

1. In Netlify, go to your site → **Site configuration → Environment variables**
2. Click **Add a variable**
3. Set:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** paste your key from Step 1 (`sk-ant-api03-...`)
4. Click **Save**
5. Go to **Deploys → Trigger deploy → Deploy site**

Your site will redeploy and the API will now work. ✓

---

## STEP 5 — (Optional) Set a custom domain

If you have a domain (or want a free one):

**Free subdomain from Netlify:**
- Go to **Domain management → Add custom domain**
- Enter something like `morare.netlify.app` — you can customise the prefix for free

**If you buy a domain later (Porkbun is cheapest ~$10/yr for .com):**
- Add it in Netlify's Domain management
- Netlify handles SSL automatically — free

---

## How it works day-to-day

```
User opens Morare
      ↓
Browser checks localStorage for today's cached story
      ↓ (if no cache)
Browser calls /api/daily (your Netlify Function)
      ↓
Netlify Function calls Anthropic API with your hidden key
      ↓
Story, word, quote, reflection → returned to browser
      ↓
Cached in localStorage until midnight
      ↓ (next day)
New API call, new story
```

**Result:** Each unique visitor triggers 1 API call per day.
1,000 daily users = ~$0.25/day. 10,000 = ~$2.50/day.

---

## Upgrading accounts to a real database (when you're ready)

Right now, accounts + entries are stored in the browser's `localStorage`.
This means:
- ✅ Works offline
- ✅ Zero cost
- ✅ No backend needed
- ❌ Entries are browser-specific (clear browser = lose entries)
- ❌ No sync across devices

**When you want real cloud accounts (still free):**

Use **Supabase** (free tier: 500MB, unlimited users):
1. Sign up at supabase.com
2. Create a project → get your `SUPABASE_URL` and `SUPABASE_ANON_KEY`
3. Create two tables: `users` and `entries`
4. Replace the localStorage auth in `index.html` with Supabase calls

I can build that upgrade for you when you're ready — just ask.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Site deploys but shows "could not be reached" | Check that `ANTHROPIC_API_KEY` is set in Netlify env vars and re-deployed |
| Function not found (404 on /api/daily) | Check `netlify.toml` is in root, `functions = "netlify/functions"` |
| API returns error | Check your Anthropic account has credit remaining |
| Stories not updating daily | LocalStorage cache — clear browser cache to force refresh |

---

## Making changes

1. Edit files locally in the `morare/` folder
2. Commit + push to GitHub
3. Netlify auto-deploys in ~30 seconds

That's it. No build process, no npm, no complexity.

---

## Cost summary

| Service | Cost |
|---|---|
| Netlify hosting | Free forever |
| Netlify Functions (125k calls/mo) | Free |
| GitHub repository | Free |
| Anthropic API | ~$0.00025/story · $5 free to start |
| Custom domain (optional) | ~$10/year if you want one |

**To run Morare for 1,000 daily users: ~$7.50/month — just the API.**

---

*Built with Netlify + Anthropic Claude Haiku · Morare*
