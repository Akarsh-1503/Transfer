# Use this agent to handle ambiguous queries

from swarm import Swarm, Agent


def transfer_to_ambiguous_query_handler_agent():
    return ambiguous_query_handler_agent



ambiguous_query_handler_agent = Agent(
    name="Ambiguous Query Handler Agent",
    instructions="You are a helpful assistant that can help with database queries and handle ambiguous questions.",
    model="gpt-4o",
)



