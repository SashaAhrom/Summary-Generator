from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


async def get_ai_summary(description):
    """
    Generate an AI summary for the given course description using OpenAI's API.
    
    Args:
        description (str): The course description to summarize.
    
    Returns:
        str: The generated AI summary.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "user", "content": f"Summarize this online course: [{description}]"}
            ]
        )
        summary = response.choices[0].message.content.strip()

        if not summary:
            raise ValueError("Summary is empty.")

        if "I'm sorry" in summary or "As an AI" in summary:
            raise ValueError("Unusable summary content.")

        return summary

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to generate summary: {str(e)}"
        )
