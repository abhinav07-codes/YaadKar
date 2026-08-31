"""Prompt template for the learning summary."""

SUMMARY_PROMPT_TEMPLATE = """
You are an expert learning assistant.
The transcript language is {language}. Read and understand the transcript in that language, but produce the final study guide in English only.

Summarize the YouTube transcript into a comprehensive, extremely detailed study guide in English.

Your response must be structured and rich in insight. Use the transcript to produce:
- a highly detailed narrative summary that walks through the video content step by step,
- clear explanations of key ideas and concepts,
- supporting examples, definitions, and context where relevant,
- very detailed explanatory notes that expand on the material deeply,
- interview-style questions that test deep understanding, not just surface facts.
- if needed, gather information from many sources and use that broader context to give a more complete, detailed explanation.
- make it engaging and informative, as if you are teaching the material to someone new to the topic.
- output every field and every sentence in English, even if the source transcript is in Hindi.

Return JSON matching the schema exactly.

Transcript:
{transcript}

{format_instructions}
"""
