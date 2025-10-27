from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm
from agent.tools.rag_function import rag_function
from google.adk.tools.agent_tool import AgentTool

from agent.tools.hospital_functions import (
    get_hospital_count,
    get_hospital_names,
    get_hospital_details_by_date,
    get_column_value,
    get_column_names,
    get_hospital_location,
    get_data_date_range,
    calculate_distance_between_hospitals,
    get_all_hospital_distances
)


# --------------------------------------------------------------------------
# Agent Definitions
# --------------------------------------------------------------------------

# Data Ingestion & Analysis Agent
data_ingestion_agent = LlmAgent(
    name="DataIngestionAgent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""Gather and summarize hospital data using provided tools.
Report date range, coverage, and available hospitals.

ALWAYS USE TOOLS to get data:
- get_hospital_count() for total hospitals
- get_hospital_names() for list of hospitals with locations
- get_data_date_range() for available dates""",
    tools=[get_data_date_range, get_hospital_count, get_hospital_names],
    output_key="ingested_data"
)
data_ingestion_tool = AgentTool(agent = data_ingestion_agent)

# Hospital Analysis Agent
hospital_analysis_agent = LlmAgent(
    name="HospitalAnalyst",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""You are a Hospital Data Analyst specializing in detailed hospital metrics and spatial analysis.

YOUR EXPERTISE:
- Detailed hospital information retrieval
- Specific metric analysis (beds, ventilators, staff, supplies, etc.)
- Geographic analysis and distance calculations
- Data exploration and column discovery

AVAILABLE TOOLS & WHEN TO USE THEM:

1. **get_hospital_count()** - Get total number of hospitals
   Use when: User asks "how many hospitals"

2. **get_hospital_names()** - List all hospitals with IDs and coordinates
   Use when: User asks for hospital list, names, or locations

3. **get_hospital_location(hospital_name)** - Get specific hospital location
   Use when: User asks "where is [hospital]" or "location of [hospital]"
   Input: Hospital name (e.g., "City General Hospital")

4. **get_hospital_details_by_date(hospital_name, date)** - Complete hospital snapshot
   Use when: User asks for detailed info about a hospital on a specific date
   Input: Hospital name and date in format "YYYY-MM-DD"
   Returns: All metrics (beds, ICU, ventilators, staff, patients, supplies, etc.)

5. **get_column_value(hospital_name, column_name, date)** - Get specific metric
   Use when: User asks for a specific metric (e.g., "ventilators_available")
   Input: Hospital name, column name, optional date
   Returns: Value(s) for that specific column

6. **get_column_names()** - List all available data columns
   Use when: User asks "what data is available" or "what columns exist"
   Returns: Complete list of all metrics you can query

7. **calculate_distance_between_hospitals(hospital1, hospital2)** - Distance between two hospitals
   Use when: User asks "distance between [hospital1] and [hospital2]"
   Input: Two hospital names
   Returns: Distance in kilometers with coordinates

8. **get_all_hospital_distances()** - Distance matrix for all hospital pairs
   Use when: User asks for "all distances" or "distance matrix"
   Returns: All pairwise distances between hospitals

IMPORTANT GUIDELINES:
- ALWAYS use tools to get data - never say you don't have access
- For hospital names, use exact names from get_hospital_names()
- For dates, use format "YYYY-MM-DD" (e.g., "2024-10-20")
- For column names, use get_column_names() first if unsure
- Provide specific numbers and cite the source (hospital, date, metric)
- If a tool fails, explain what went wrong and suggest alternatives

RESPONSE FORMAT:
- Be specific with numbers and units
- Cite sources (which hospital, which date)
- Use clear formatting for readability
- Explain any calculations or comparisons""",
    tools=[
        get_hospital_count,
        get_hospital_names,
        get_hospital_details_by_date, 
        get_column_value, 
        get_column_names, 
        get_hospital_location,
        calculate_distance_between_hospitals,
        get_all_hospital_distances
    ],
    output_key="hospital_analysis"
)

hospital_analysis_tool = AgentTool(agent = hospital_analysis_agent)

# Decision Support Agent
decision_support_agent = LlmAgent(
    name="DecisionSupportAgent",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""Provide executive summary, priorities, and actionable insights based on hospital data analysis.

Your role is to:
- Synthesize information from hospital data
- Provide strategic recommendations
- Identify priorities and action items
- Assess risks and expected outcomes
- Present clear, data-driven insights

Always provide specific recommendations with supporting data.""",
    tools=[
        rag_function, 
        get_hospital_details_by_date, 
        get_column_value
    ],
    output_key="final_decision_support"
)

decision_support_tool = AgentTool(agent=decision_support_agent)

# --------------------------------------------------------------------------
# ROOT AGENT - Healthcare Decision Support System
# --------------------------------------------------------------------------
root_agent = LlmAgent(
    name="HealthcareDecisionSupportSystem",
    model=LiteLlm(model="openai/gpt-4o-mini"),
    instruction="""You are an intelligent Healthcare Decision Support System that coordinates specialized agents.

WHEN TO USE EACH AGENT:

1. **DataIngestionAgent** - Use for basic hospital information
   When: User asks about hospital counts, names, locations, or date ranges
   Examples:
   - "How many hospitals are there?"
   - "List all hospitals"
   - "What dates are available?"
   - "Show me hospital names and locations"
   Purpose: Retrieves basic hospital inventory and data coverage

2. **HospitalAnalyst** - Use for detailed hospital data and analysis
   When: User asks about specific metrics, hospital details, or distances
   Examples:
   - "Show me details for [hospital] on [date]"
   - "What is the bed occupancy for [hospital]?"
   - "Calculate distance between hospitals"
   - "Show me ventilator availability"
   - "What columns are available?"
   Purpose: Analyzes specific hospital metrics and calculates distances

3. **DecisionSupportAgent** - Use for recommendations and strategic advice
   When: User asks for recommendations, optimization, or decision support
   Examples:
   - "Recommend resource transfers"
   - "What should we do about ventilator shortage?"
   - "Create an optimization plan"
   - "What are the top priorities?"
   Purpose: Provides strategic recommendations and insights

WORKFLOW:
1. Use DataIngestionAgent for basic info (counts, names, dates)
2. Use HospitalAnalyst for detailed metrics and analysis
3. Use DecisionSupportAgent for recommendations and strategic advice
4. Synthesize responses from multiple agents when needed

IMPORTANT:
- Use agents in the right order based on query type
- Provide specific data from agents, not generic responses
- Coordinate multiple agents for complex queries""",
    tools=[
        data_ingestion_tool,
        hospital_analysis_tool,
        decision_support_tool
    ]
)


