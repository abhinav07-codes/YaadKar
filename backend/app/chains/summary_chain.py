"""LangChain summary chain assembly."""

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from app.config import API_BASE_URL, GROQ_API_KEY, MODEL_NAME
from app.models.response import SummaryResponse
from app.prompts.summary_prompt import SUMMARY_PROMPT_TEMPLATE


def build_summary_chain():
    """Constructs and returns a reusable LangChain chain."""
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Set it in backend/.env before running summarization."
        )

    parser = PydanticOutputParser(pydantic_object=SummaryResponse)
    prompt = PromptTemplate(
        template=SUMMARY_PROMPT_TEMPLATE,
        input_variables=["transcript"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    base_url = API_BASE_URL.rstrip('/')
    if base_url.endswith('/openai/v1'):
        base_url = base_url[: -len('/openai/v1')]

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        base_url=base_url,
        temperature=0.2,
    )
    return prompt | llm | parser
