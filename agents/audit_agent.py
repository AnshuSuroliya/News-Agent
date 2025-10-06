from google.adk.agents import LlmAgent

AUDIT_PROMPT = (
    "You are an Audit Agent reviewing the quality of a news summary written by another agent.\n"
    "Tasks:\n"
    "- Rate the overall accuracy (1 to 10)\n"
    "- Flag any vague, missing, or incorrect information\n"
    "- Check for completeness and topical coverage\n"
    "- Suggest improvements if needed\n"
    "Output a readable, well-formatted critique with these sections:\n"
    "Accuracy Score: <score>\n"
    "Remarks: <short critique>\n"
    "Highlights: <bulleted list>\n"
    "Issues: <bulleted list>\n"
)

audit_agent = LlmAgent(
    name="AuditAgent",
    model="gemini-2.5-flash",
    instruction=AUDIT_PROMPT
) 