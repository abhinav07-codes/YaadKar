const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');

let currentNotesText = '';

async function getCurrentTabUrl() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.url || '';
}

function setStatus(message, isError = false) {
  statusEl.textContent = message;
  statusEl.classList.toggle('error', isError);
}

function buildNotesText(data) {
  const sections = [
    { title: 'Summary', items: [data.summary] },
    { title: 'Key Points', items: data.key_points },
    { title: 'Detailed Explanation', items: data.detailed_explanation },
    { title: 'Interview Questions', items: data.interview_questions },
  ];

  const lines = [];
  sections.forEach((section) => {
    lines.push(`${section.title}:`);
    if (section.items.length) {
      section.items.forEach((item, index) => {
        lines.push(`${index + 1}. ${item}`);
      });
    } else {
      lines.push('No content available.');
    }
    lines.push('');
  });

  return lines.join('\n').trim();
}

function renderResults(data) {
  resultsEl.innerHTML = '';
  currentNotesText = buildNotesText(data);
  copyBtn.hidden = !currentNotesText;

  const sections = [
    { title: 'Summary', items: [data.summary] },
    { title: 'Key Points', items: data.key_points },
    { title: 'Detailed Explanation', items: data.detailed_explanation },
    { title: 'Interview Questions', items: data.interview_questions },
  ];

  sections.forEach((section) => {
    const card = document.createElement('div');
    card.className = 'card';

    const heading = document.createElement('h2');
    heading.textContent = section.title;
    card.appendChild(heading);

    if (section.items.length) {
      const list = document.createElement('ul');
      section.items.forEach((item) => {
        const li = document.createElement('li');
        li.textContent = item;
        list.appendChild(li);
      });
      card.appendChild(list);
    } else {
      const empty = document.createElement('p');
      empty.textContent = 'No content available.';
      card.appendChild(empty);
    }

    resultsEl.appendChild(card);
  });
}

async function copyNotes() {
  if (!currentNotesText) {
    setStatus('No notes to copy yet.', true);
    return;
  }

  try {
    await navigator.clipboard.writeText(currentNotesText);
    setStatus('Notes copied to clipboard.');
  } catch {
    try {
      const temp = document.createElement('textarea');
      temp.value = currentNotesText;
      document.body.appendChild(temp);
      temp.select();
      document.execCommand('copy');
      document.body.removeChild(temp);
      setStatus('Notes copied to clipboard.');
    } catch {
      setStatus('Unable to copy notes in this browser.', true);
    }
  }
}

async function generateNotes() {
  generateBtn.disabled = true;
  copyBtn.hidden = true;
  setStatus('Fetching current video...');
  resultsEl.innerHTML = '';

  try {
    const url = await getCurrentTabUrl();
    if (!url) {
      throw new Error('No active tab URL found.');
    }

    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
      throw new Error('Open a YouTube video before generating notes.');
    }

    setStatus('Sending request to backend...');
    const response = await fetch('http://127.0.0.1:8000/summarize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const responseText = await response.text();
    let data;

    try {
      data = JSON.parse(responseText);
    } catch {
      data = { detail: responseText || 'No response body' };
    }

    if (!response.ok) {
      throw new Error(
        data.detail || `Failed to summarize video (${response.status}).`
      );
    }

    renderResults(data);
    setStatus('Summary generated successfully.');
  } catch (error) {
    setStatus(error.message || 'Something went wrong.', true);
  } finally {
    generateBtn.disabled = false;
  }
}

generateBtn.addEventListener('click', generateNotes);
copyBtn.addEventListener('click', copyNotes);
