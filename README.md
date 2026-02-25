# Morare

> A daily ritual built around real human courage.

Every day, Morare surfaces a true story of someone who did something meaningful on this date in history — then distills it into a word, a quote, a reflection question, and a writing space.

## Stack

- **Frontend:** Single HTML file — no framework, no build step
- **Backend:** Netlify Functions (serverless)
- **AI:** Anthropic Claude Haiku (story + word + quote + reflection)
- **Storage:** localStorage (upgradeable to Supabase)

## Deploy

See `DEPLOY.md` for the full step-by-step guide.

## Local development

Open `public/index.html` directly in a browser to preview the UI.

For the API to work locally, install the Netlify CLI:

```bash
npm install -g netlify-cli
netlify dev
```

Then set `ANTHROPIC_API_KEY` in a `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```
