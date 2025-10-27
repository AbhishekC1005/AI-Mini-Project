"""Main entry point for the Google ADK Search Agent."""
from agent.search_agent import SearchAgent


def main():
    """Initialize and run the search agent."""
    agent = SearchAgent()
    agent.chat()


if __name__ == "__main__":
    main()
