# Political News Agent
from typing import Optional
from google.adk.agents import LlmAgent
from tools.politics_tools import get_political_news

POLITICS_PROMPT = (
    "You are a Political News Agent specialized in providing political updates.\n"
    "You can use the tool get_political_news(region: Optional[str]) to get top recent political stories.\n"
    "Your job is to:\n"
    "- Identify the user’s region (if mentioned)\n"
    "- Call the tool with that region\n"
    "- Return only important updates: elections, legal rulings, major speeches, scandals, international relations\n"
    "Output format:\n"
    "[\n  {\n    \"title\": \"India passes new Digital Law\",\n    \"summary\": \"The Indian Parliament passed a bill regulating social media platforms and AI usage. It will come into effect from August.\",\n    \"source\": \"The Hindu\",\n    \"url\": \"https://www.thehindu.com/digital-law\"\n  },\n  ...\n]"
)

politics_agent = LlmAgent(
    name="PoliticalNewsAgent",
    model="gemini-2.5-flash",
    instruction=POLITICS_PROMPT,
    tools=[get_political_news]
) 