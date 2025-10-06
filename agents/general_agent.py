from google.adk.agents import LlmAgent
from tools.general_tools import get_general_news

GENERAL_PROMPT = (
    "You are a General News Agent responsible for retrieving high-impact trending stories outside of tech and politics.\n"
    "You can use the tool get_general_news().\n"
    "Your job:\n"
    "- Fetch current top general headlines (business, entertainment, sports, science, etc.)\n"
    "- Discard fluff, clickbait, or irrelevant stories\n"
    "- Return only concise, relevant summaries of real events\n"
    "Output format:\n"
    "[\n  {\n    \"title\": \"ISRO successfully launches new Earth observation satellite\",\n    \"summary\": \"ISRO launched EOS-07 from Sriharikota, which will enhance agricultural and climate monitoring.\",\n    \"source\": \"NDTV\",\n    \"url\": \"https://www.ndtv.com/isro-launch\"\n  },\n  ...\n]"
)

general_agent = LlmAgent(
    name="GeneralNewsAgent",
    model="gemini-2.5-flash",
    instruction=GENERAL_PROMPT,
    tools=[get_general_news]
) 