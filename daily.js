// netlify/functions/daily.js
// This runs on Netlify's servers — your API key never reaches the browser

exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const { month, day, year } = JSON.parse(event.body || '{}');

  if (!month || !day) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing date' }) };
  }

  const prompt = `Today is ${month} ${day}, ${year}. Generate a Morare daily ritual entry as valid JSON only — no markdown, no explanation, no backticks.

Return exactly this JSON structure:
{
  "storyTitle": "A short punchy headline about a real positive/brave/creative/scientific/artistic/humanitarian historical event on this exact date in history",
  "storyBody": "A narrative 130-150 word story about this event. Write it like a human journal entry — vivid, alive, personal. Not Wikipedia. Show the courage, creativity, or beauty involved. End with one sentence about why it still matters.",
  "word": "ONE single powerful psychologically resonant action-oriented word extracted from the story's core theme (examples: Audacity, Devotion, Defiance, Curiosity, Resilience, Precision, Tenacity, Wonder, Courage, Vision, Patience)",
  "wordTheme": "A 5-8 word thematic phrase capturing the word's meaning in context",
  "quoteText": "A powerful non-cliché quote that deeply resonates with the word. Emotionally intelligent. Not from generic motivational lists. Draw from literature, philosophy, science, or history.",
  "quoteAuthor": "Full author name and brief context (e.g. Viktor Frankl, in Man's Search for Meaning)",
  "reflectionQuestion": "A single sharp, productively uncomfortable reflection question tied to the word and story. Make it personal, specific, and responsible — not vague. It should create a moment of honest self-examination."
}`;

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }],
      }),
    });

    if (!response.ok) {
      throw new Error(`Anthropic API error: ${response.status}`);
    }

    const data = await response.json();
    const text = data.content.map(c => c.text || '').join('').trim();
    
    // Strip any accidental markdown fences
    const clean = text.replace(/^```json\s*/i, '').replace(/```\s*$/i, '').trim();
    const parsed = JSON.parse(clean);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(parsed),
    };
  } catch (err) {
    console.error('Function error:', err);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Failed to generate content', detail: err.message }),
    };
  }
};
