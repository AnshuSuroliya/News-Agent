import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from agents.router_agent import router_agent
from agents.tech_ai_agent import tech_ai_agent
from agents.politics_agent import politics_agent
from agents.general_agent import general_agent
from agents.report_writer_agent import report_writer_agent
from agents.audit_agent import audit_agent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import json
import re

class NewsAggregatorManager:
    """
    Orchestrates the full news aggregation workflow: routing, news fetching, summarizing, and auditing.
    Uses Google ADK Runner and SessionService for all agent calls.
    """
    def __init__(self):
        self.router_agent = router_agent
        self.tech_ai_agent = tech_ai_agent
        self.politics_agent = politics_agent
        self.general_agent = general_agent
        self.report_writer_agent = report_writer_agent
        self.audit_agent = audit_agent
        self.session_service = InMemorySessionService()
        self.app_name = "news_aggregator"
        self.user_id = "user1"
        self.session_id = "news-session-1"

    async def get_news_summary(self, query: str) -> dict:
        await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        route_result = self._call_agent(self.router_agent, query)
        category = "general"
        if isinstance(route_result, str) and route_result.strip():
            cleaned = route_result.strip()
            cleaned = re.sub(r'^```[a-zA-Z]*', '', cleaned).strip()
            cleaned = re.sub(r'```$', '', cleaned).strip()
            if not cleaned.startswith('{'):
                cleaned = '{' + cleaned
            if not cleaned.endswith('}'):
                cleaned = cleaned + '}'
            try:
                parsed = json.loads(cleaned)
                category = parsed.get("category", "general").strip().lower()
            except Exception:
                category = "general"
        if category == "tech_ai":
            news_items = self._call_agent(self.tech_ai_agent, query)
        elif category == "politics":
            news_items = self._call_agent(self.politics_agent, query)
        else:
            news_items = self._call_agent(self.general_agent, query)
        summary = self._call_agent(self.report_writer_agent, news_items)
        audit_result = self._call_agent(self.audit_agent, summary)
        return {
            "summary": summary,
            "audit": audit_result,
            "category": category,
            "raw_news": news_items
        }

    def _call_agent(self, agent, input_data):
        runner = Runner(agent=agent, app_name=self.app_name, session_service=self.session_service)
        if not isinstance(input_data, str):
            input_data = json.dumps(input_data, ensure_ascii=False)
        content = types.Content(role="user", parts=[types.Part(text=input_data)])
        result = ""
        for event in runner.run(user_id=self.user_id, session_id=self.session_id, new_message=content):
            if hasattr(event, "is_final_response") and event.is_final_response():
                if hasattr(event, "content") and event.content and hasattr(event.content, "parts") and event.content.parts:
                    result = event.content.parts[0].text
                break
        return result

async def main() -> None:
    query = input("Enter your news query: ")
    mgr = NewsAggregatorManager()
    result = await mgr.get_news_summary(query)
    print("\n===== News Summary =====\n")
    print(result["summary"])
    print("\n===== Audit Result =====\n")
    print(result["audit"])
    # Write to file
    with open("news_report.txt", "w", encoding="utf-8") as f:
        f.write("===== News Summary =====\n\n")
        f.write(result["summary"] + "\n\n")
        f.write("===== Audit Result =====\n\n")
        f.write(result["audit"] + "\n")
    # Write audit only to a separate file
    with open("audit_report.txt", "w", encoding="utf-8") as f:
        f.write(result["audit"] + "\n")

if __name__ == "__main__":
    asyncio.run(main()) 