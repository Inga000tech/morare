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
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: 'GEMINI_API_KEY not set. Go to Netlify → Site configuration → Environment variables, add GEMINI_API_KEY, then redeploy.' })
    };
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

  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  // Try multiple models — if one is rate limited, fall through to the next
  const models = ['gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash'];

  for (const model of models) {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        console.log(`Trying ${model}, attempt ${attempt}`);

        const response = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: prompt }] }],
              generationConfig: { temperature: 0.85, maxOutputTokens: 1500 }
            })
          }
        );

        if (response.status === 429) {
          console.log(`429 rate limit on ${model} attempt ${attempt}`);
          if (attempt < 3) { await sleep(attempt * 2500); continue; }
          else { break; } // try next model
        }

        if (!response.ok) {
          const errText = await response.text();
          console.error(`${model} HTTP ${response.status}:`, errText);
          break; // try next model
        }

        const data = await response.json();
        const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
        const clean = raw
          .replace(/^```json\s*/i, '')
          .replace(/^```\s*/i, '')
          .replace(/```\s*$/, '')
          .trim();

        const parsed = JSON.parse(clean);
        console.log(`Success with ${model}`);
        return { statusCode: 200, headers, body: JSON.stringify(parsed) };

      } catch (err) {
        console.error(`${model} attempt ${attempt} threw:`, err.message);
        if (attempt < 3) { await sleep(1000); continue; }
        break;
      }
    }
  }

  // All models exhausted — return a hardcoded fallback so the page never shows an error
  console.log('All models failed or rate limited. Serving fallback content.');
  return {
    statusCode: 200,
    headers,
    body: JSON.stringify({
      storyTitle: "Marie Curie becomes the first person to win two Nobel Prizes",
      storyBody: "In 1911, Marie Curie stood in Stockholm to accept her second Nobel Prize — this time in Chemistry, having already won one in Physics in 1903. She was the first person in history to win two. But the weeks before the ceremony had been brutal. The French press had attacked her character, her nationality, her grief. Her husband Pierre had died years before, and she was raising two daughters alone while running a laboratory and rewriting the boundaries of human knowledge.\n\nShe went to Stockholm anyway. She gave her lecture anyway. She spoke only of polonium and radium, of the nature of atoms, of what the invisible world contains.\n\nShe was not performing courage. She simply refused to let cruelty determine the direction of her life. The work was the answer. It always had been.",
      word: "Fortitude",
      wordTheme: "Continuing forward when the world pushes back",
      quoteType: "quote",
      quoteText: "Nothing in life is to be feared, only to be understood. Now is the time to understand more, so that we may fear less.",
      quoteAttr: "Marie Curie",
      monkStory: "A student came to his teacher frustrated. 'I work so hard,' he said, 'and still people criticise me. Still the world does not cooperate.'\n\nThe teacher handed him a bowl of water. 'Carry this across the courtyard without spilling a drop.'\n\nThe student walked carefully, eyes fixed on the bowl. He crossed the courtyard. Not a drop spilled.\n\n'Did you notice the clouds?' asked the teacher.\n\n'No.'\n\n'The children playing? The man at the gate who called your name?'\n\n'No,' said the student. 'I heard nothing. I was watching the water.'\n\nThe teacher nodded. 'That is fortitude. Not the absence of noise. The presence of focus.'",
      monkAttr: "A Zen teaching story",
      reflectionQuestion: "What criticism or external noise has been quietly pulling your attention away from the work only you can do — and what would change if you simply stopped listening to it?"
    })
  };
};
