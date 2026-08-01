"""Prompt template for the learning summary."""

SUMMARY_PROMPT_TEMPLATE = """
You are an expert learning assistant.
Summarize the following YouTube transcript into a comprehensive, extremely detailed study guide.

Your response must be structured and rich in insight. Use the transcript to produce:
- a highly detailed narrative summary that walks through the video content step by step,
- clear explanations of key ideas and concepts,
- supporting examples, definitions, and context where relevant,
- very detailed explanatory notes that expand on the material deeply,
- interview-style questions that test deep understanding, not just surface facts.
- if needed, gather information from many sources and use that broader context to give a more complete, detailed explanation.
- make it engaging and informative, as if you are teaching the material to someone new to the topic.

Return JSON matching the schema exactly.

Transcript:
{transcript}

{format_instructions}
"""
