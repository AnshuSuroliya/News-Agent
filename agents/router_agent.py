from google.adk.agents import LlmAgent

ROUTER_PROMPT = (
    "You are a router agent in a news aggregation system.\n"
    "Your task is to analyze the user's query and classify it into one of these categories:\n"
    "- 'tech_ai' → for queries related to technology, AI, machine learning, tools, software, startups\n"
    "- 'politics' → for political news, elections, leaders, laws, government actions\n"
    "- 'general' → for anything else (finance, sports, entertainment, etc.)\n"
    "Output the category as a JSON object:\n"
    '{ "category": "tech_ai" }'
)

router_agent = LlmAgent(
    name="RouterAgent",
    model="gemini-2.5-flash",
    instruction=ROUTER_PROMPT
) 