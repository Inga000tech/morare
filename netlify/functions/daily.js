exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  let month, day, year;
  try {
    const body = JSON.parse(event.body || '{}');
    month = body.month; day = body.day; year = body.year;
  } catch (e) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Bad request body' }) };
  }

  if (!month || !day) {
    return { statusCode: 400, headers, body: JSON.stringify({ error: 'Missing date params' }) };
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, headers, body: JSON.stringify({ error: 'GEMINI_API_KEY not configured in Netlify environment variables' }) };
  }

  const prompt = `Today is ${month} ${day}, ${year}.

Generate a Morare daily ritual entry. Return ONLY a raw JSON object — no markdown fences, no explanation, no extra text before or after.

{
  "storyTitle": "Short punchy headline for a real positive, brave, creative or scientific historical event on this exact date in history",
  "storyBody": "Vivid narrative 160-200 words about this event. Written like a human journal entry — alive, sensory, emotional. NOT Wikipedia. Show the human behind the act. End with one sentence on why it still matters.",
  "word": "ONE single powerful psychologically-resonant word from the story theme (e.g. Audacity, Devotion, Defiance, Curiosity, Resilience, Precision, Wonder, Patience, Courage, Vision, Tenacity, Clarity)",
  "wordTheme": "5-9 word thematic phrase capturing this word in context",
  "quoteType": "quote OR poem — choose whatever fits the word best today",
  "quoteText": "If quote: a powerful non-cliche quote aligned with the word, NOT from generic motivational lists, drawn from literature philosophy history or science. If poem: a short meaningful poem 4-12 lines from Rilke Whitman Mary Oliver Rumi Hafiz or similar — use actual line breaks with \\n",
  "quoteAttr": "Author name and source e.g. Mary Oliver, from Upstream: Selected Essays",
  "monkStory": "A contemplative short story or parable 140-180 words loosely inspired by the word. Can be a Zen koan story, Sufi tale, desert father parable, or Buddhist teaching story. Warm, wise, slightly mysterious. Use \\n\\n between paragraphs.",
  "monkAttr": "Tradition or source e.g. A Zen teaching story or Adapted from Sufi tradition",
  "reflectionQuestion": "One sharp, productively uncomfortable question tied to the word. Personal, specific, honest. NOT vague."
}`;

  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { temperature: 0.85, maxOutputTokens: 1500 }
        })
      }
    );

    if (!response.ok) {
      const errBody = await response.text();
      console.error('Gemini error:', response.status, errBody);
      return {
        statusCode: response.status,
        headers,
        body: JSON.stringify({ error: `Gemini API error: ${response.status}`, detail: errBody })
      };
    }

    const data = await response.json();
    const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
    const clean = raw
      .replace(/^```json\s*/i, '')
      .replace(/^```\s*/i, '')
      .replace(/```\s*$/, '')
      .trim();

    const parsed = JSON.parse(clean);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(parsed)
    };

  } catch (err) {
    console.error('Function error:', err.message);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'Internal error', detail: err.message })
    };
  }
};
