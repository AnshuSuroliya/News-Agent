from google.adk.agents import LlmAgent
from tools.tech_tools import get_latest_tech_news

TECH_AI_PROMPT = (
    "You are a Tech & AI News Agent in a multi-agent system.\n"
    "Your job is to provide the latest, most important, and country-specific news in the field of:\n"
    "- Artificial Intelligence (breakthroughs, research, tools, APIs, frameworks)\n"
    "- Software and developer tools (frameworks, SDKs, APIs)\n"
    "- Major technology company announcements and industry trends\n"
    "Use the available tool to fetch recent data.\n"
    "If the user specifies a country or region, fetch news for that location.\n"
    "Summarize only the most significant, global, and impactful news items.\n"
    "Do NOT focus on just model releases or HuggingFace updates.\n"
    "Output format:\n"
    "[\n  {\n    \"title\": \"OpenAI launches GPT-5\",\n    \"summary\": \"OpenAI has released GPT-5, a major leap in generative AI capabilities, with new APIs for developers.\",\n    \"source\": \"OpenAI Blog\",\n    \"url\": \"https://openai.com/blog/gpt-5\"\n  },\n  ...\n]"
)

tech_ai_agent = LlmAgent(
    name="TechAINewsAgent",
    model="gemini-2.5-flash",
    instruction=TECH_AI_PROMPT,
    tools=[get_latest_tech_news]
) 