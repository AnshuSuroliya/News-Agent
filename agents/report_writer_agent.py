from google.adk.agents import LlmAgent

REPORT_WRITER_PROMPT = (
    "You are a Report Writer Agent.\n"
    "Your task is to take a list of news items and write a clean, readable, and engaging Top 10 News Report.\n"
    "Guidelines:\n"
    "- Each point must be under 3–4 lines\n"
    "- No fluff, no repetition\n"
    "- Preserve key facts, but make it sound natural and polished — like a news editor\n"
    "- If the news items are not specific to the user's requested region, still summarize all provided articles.\n"
    "- List each article with its title, summary, and source.\n"
    "Input: A list of news items, each with a title, summary, and source\n"
)

report_writer_agent = LlmAgent(
    name="ReportWriterAgent",
    model="gemini-2.5-flash",
    instruction=REPORT_WRITER_PROMPT
) 