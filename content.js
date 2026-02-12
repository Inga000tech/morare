export const astrologyEvents2026 = {
  "2026-02-13": {
    title: "Saturn enters Aries",
    meaning: "Saturn is the planet of discipline, Aries the sign of initiation. A three-year cycle of disciplined courage begins."
  },
  "2026-02-17": {
    title: "Solar Eclipse in Aquarius",
    meaning: "A hard reset in technology, community, and collective ideals."
  },
  "2026-02-20": {
    title: "Saturn Conjunct Neptune in Aries",
    meaning: "Dreams meet reality. A rare meeting at the start of the zodiac signaling a rebirth of the collective dream."
  },
  "2026-02-26": {
    title: "Mercury Retrograde in Pisces",
    meaning: "Communication goes underwater. Focus on intuition and art rather than logic and logistics."
  },
  "2026-03-03": {
    title: "Total Lunar Eclipse in Virgo",
    meaning: "A 'blood moon' focused on health and work. Time to release perfectionism that paralyzes progress."
  },
  "2026-03-20": {
    title: "Astrological New Year",
    meaning: "The Equinox. Sun enters Aries. A fresh surge of life force and the official start of the zodiacal cycle."
  },
  "2026-03-22": {
    title: "Neptune Cazimi in Aries",
    meaning: "Spiritual clarity. The fog is momentarily burned away, offering a vision of your highest potential."
  },
  "2026-04-19": {
    title: "Mars Conjunct Saturn in Aries",
    meaning: "Controlled power. The urge to move fast meets the need for structure. Strategic action is required."
  },
  "2026-04-25": {
    title: "Uranus enters Gemini",
    meaning: "The communication revolution begins. Radical shifts in learning, AI, and decentralized systems for the next 7 years."
  },
  "2026-05-22": {
    title: "Uranus Cazimi in Gemini",
    meaning: "Lightning bolt insights. A day for breakthrough ideas and sudden cognitive shifts."
  },
  "2026-06-09": {
    title: "Venus Conjunct Jupiter in Cancer",
    meaning: "Abundance and luck. A peak day for love, family, and finding emotional security."
  },
  "2026-06-29": {
    title: "Jupiter enters Leo & Mercury Retrograde",
    meaning: "Jupiter brings a year of creativity and drama. Meanwhile, Mercury starts a review of family roots."
  },
  "2026-07-03": {
    title: "Mars Conjunct Uranus in Gemini",
    meaning: "Volatile energy. Breakthroughs or accidents. Great for breaking out of a long-term rut."
  },
  "2026-07-26": {
    title: "North Node enters Aquarius",
    meaning: "Karmic shift. The collective focus moves from individual ego (Leo) to group contribution (Aquarius)."
  },
  "2026-07-27": {
    title: "Saturn Retrograde in Aries",
    meaning: "Reviewing leadership. A time to internalize the lessons of self-discipline learned earlier this year."
  },
  "2026-08-12": {
    title: "Total Solar Eclipse in Leo",
    meaning: "Creative rebirth. Ego reset. Reinvention of how you shine and express your true self."
  },
  "2026-08-27": {
    title: "Partial Lunar Eclipse in Pisces",
    meaning: "Emotional release. Letting go of old illusions and finalizing a cycle of spiritual healing."
  },
  "2026-10-03": {
    title: "Venus Retrograde in Scorpio",
    meaning: "Relationship deep-dive. Reviewing trust, intimacy, and shared resources."
  },
  "2026-10-24": {
    title: "Mercury Retrograde in Scorpio",
    meaning: "Investigation and depth. Uncovering hidden truths and revisiting intense conversations."
  },
  "2026-11-12": {
    title: "Jupiter Conjunct South Node in Leo",
    meaning: "Karmic check-in. Walking away from vanity or titles that no longer serve your growth."
  },
  "2026-12-23": {
    title: "Supermoon in Cancer",
    meaning: "The year ends in softness. Emotional nourishment. Cocooning and coming home to yourself."
  }
};

export function getIntegrationText(date) {
  return {
    title: "Integration Period",
    meaning: "No major celestial shift today. The work is internal. The transformation is subtle. Integration is where growth becomes permanent."
  };
}

// ... keep your astrologyEvents2026 object at the top ...

export const dailyQuestions = [
  "What does my 'inner child' need to feel safe today?",
  "What is one noise or distraction I can eliminate this morning?",
  "If I were my own best friend, what encouragement would I give myself right now?",
  "Which 'inner critic' voice is loudest today, and what is its name?",
  "What would 'good enough' look like for today?",
  "What is a 'micro-win' I can celebrate by 10:00 AM?",
  "If today were a movie, what would the genre be?",
  "What is one 'No' I need to say to protect my 'Yes'?",
  "What part of 'Future Me' am I building this morning?",
  "If I had 20% more courage today, what would I do differently?",
  "What is one boundary I need to reinforce today?",
  "What is the 'theme song' for my intentions today?",
  "How can I show up authentically in my first meeting/interaction?",
  "What is one thing I’m doing today purely because I want to?",
  "What legacy—even a tiny one—do I want to leave by tonight?",
  "What am I currently avoiding that needs my attention?",
  "What emotion am I trying to 'fix' rather than feel?",
  "Where am I seeking validation from others today?",
  "What is one 'shadow' trait (like envy or pride) that might pop up today?",
  "How am I subconsciously making things harder for myself?",
  "What is the most honest thing I could say to myself right now?",
  "What am I 'hiding' behind my busyness?",
  "What would happen if I didn't try to be 'perfect' today?",
  "What is the 'unspoken' need behind my current stress?",
  "What is one thing I’m looking forward to in the next 12 hours?",
  "What is a 'tiny luxury' I can grant myself today?",
  "What is something beautiful I saw within five minutes of waking up?",
  "How can I add a moment of 'play' to my afternoon?",
  "What is one thing about my physical space that I appreciate?",
  "What is a strength of mine that I often overlook?",
  "If I were a character in a book, what would the narrator say about me today?",
  "What is one 'soul-nourishing' food or drink I’ll have today?",
  "What is a question I hope someone asks me today?",
  "What is the 'one word' that defines my intention for this day?"
];

/**
 * Gets a unique question for the day based on the date
 */
export function getDailyQuestion(dateString) {
  const date = new Date(dateString);
  // This creates a unique index based on the day of the year
  const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 86400000);
  const index = dayOfYear % dailyQuestions.length;
  return dailyQuestions[index];
}

// Keep your existing getIntegrationText function below
export function getIntegrationText(date) {
  return {
    title: "Integration Period",
    meaning: "No major celestial shift today. The work is internal. The transformation is subtle. Integration is where growth becomes permanent."
  };
}
