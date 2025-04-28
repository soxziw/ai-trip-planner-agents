# trip_planner.py with API integration

import os
import yaml
import autogen
from typing import Dict, List, Any, Optional
from pathlib import Path
from pprint import pprint
from api_integration import ApiManager

# Custom YAML loader with include functionality
class YamlLoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YamlLoader, self).__init__(stream)
        
    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)

YamlLoader.add_constructor('!include', YamlLoader.include)

def load_agent_config(config_path: str) -> Dict:
    """Load agent configuration from YAML file with support for !include directive."""
    with open(config_path, 'r') as file:
        return yaml.load(file, YamlLoader)

# Create API Manager for retrieving data
api_manager = ApiManager()

# Create custom function calling for agents
def site_search(city, category=None, limit=5):
    """Search for attractions in a city"""
    return api_manager.search_attractions(location=city, category=category, limit=limit)

def get_attraction_details(location_id):
    """Get detailed information about an attraction"""
    return api_manager.get_location_details(location_id=location_id)

def restaurant_search(cuisine, city):
    """Search for restaurants by cuisine in a city"""
    return api_manager.search_restaurants(cuisine=cuisine, location=city)

def hotel_search_airbnb(city, checkin, checkout, adults=2, price_max=300):
    """Search for accommodations on Airbnb"""
    return api_manager.search_hotels_airbnb(
        location=city, 
        checkin=checkin, 
        checkout=checkout,
        adults=adults,
        price_max=price_max
    )

def hotel_search_booking(city, checkin, checkout, adults=2, price_max=300):
    """Search for accommodations on Booking.com"""
    return api_manager.search_hotels_booking(
        location=city, 
        checkin=checkin, 
        checkout=checkout,
        adults=adults,
        price_max=price_max
    )

def get_travel_directions(origin, destination, mode="transit"):
    """Get directions between two locations"""
    return api_manager.get_directions(
        origin=origin,
        destination=destination,
        mode=mode
    )

# Define function schemas for agents
function_map = {
    "site_search": site_search,
    "get_attraction_details": get_attraction_details,
    "restaurant_search": restaurant_search,
    "hotel_search_airbnb": hotel_search_airbnb,
    "hotel_search_booking": hotel_search_booking,
    "get_travel_directions": get_travel_directions,
}

# Create function calling configs
rag_function_specs = [
    {
        "name": "site_search",
        "description": "Search for attractions and sites in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to search for attractions"
                },
                "category": {
                    "type": "string",
                    "description": "Optional category filter (e.g., 'museums', 'parks', 'historic')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return"
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "get_attraction_details",
        "description": "Get detailed information about a specific attraction",
        "parameters": {
            "type": "object",
            "properties": {
                "location_id": {
                    "type": "string",
                    "description": "The TripAdvisor location ID"
                }
            },
            "required": ["location_id"]
        }
    },
    {
        "name": "restaurant_search",
        "description": "Search for restaurants by cuisine type in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "cuisine": {
                    "type": "string",
                    "description": "The type of cuisine (e.g., 'Italian', 'Japanese', 'Vegetarian')"
                },
                "city": {
                    "type": "string",
                    "description": "The city to search in"
                }
            },
            "required": ["cuisine", "city"]
        }
    },
    {
        "name": "hotel_search_airbnb",
        "description": "Search for accommodations on Airbnb",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to search in"
                },
                "checkin": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format"
                },
                "checkout": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format"
                },
                "adults": {
                    "type": "integer",
                    "description": "Number of adults"
                },
                "price_max": {
                    "type": "integer",
                    "description": "Maximum price per night"
                }
            },
            "required": ["city", "checkin", "checkout"]
        }
    },
    {
        "name": "hotel_search_booking",
        "description": "Search for accommodations on Booking.com",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to search in"
                },
                "checkin": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format"
                },
                "checkout": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format"
                },
                "adults": {
                    "type": "integer",
                    "description": "Number of adults"
                },
                "price_max": {
                    "type": "integer",
                    "description": "Maximum price per night"
                }
            },
            "required": ["city", "checkin", "checkout"]
        }
    },
    {
        "name": "get_travel_directions",
        "description": "Get directions between two locations",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Starting location (address or place name)"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination location (address or place name)"
                },
                "mode": {
                    "type": "string",
                    "description": "Transportation mode (driving, walking, transit, bicycling)",
                    "enum": ["driving", "walking", "transit", "bicycling"]
                }
            },
            "required": ["origin", "destination"]
        }
    }
]

def create_agents(config: Dict, llm_config: Dict) -> Dict[str, autogen.AssistantAgent]:
    """Create all agents defined in the configuration."""
    agents = {}
    
    # Create the user proxy agent with function calling capability
    agents["user_proxy"] = autogen.UserProxyAgent(
        name="User",
        human_input_mode="ALWAYS",
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
        function_map=function_map
    )
    
    # Create base LLM config with function calling
    base_llm_config = {
        **llm_config,
        "functions": rag_function_specs
    }
    
    # Create area layer agents
    area_layer = config["travel_planner_agents"]["area_layer"]
    time_agent_config = area_layer["agent_0_month_time"]
    agents[time_agent_config["name"]] = autogen.AssistantAgent(
        name=time_agent_config["name"],
        system_message=time_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    time_verification_config = area_layer["verification_agent"]
    agents[time_verification_config["name"]] = autogen.AssistantAgent(
        name=time_verification_config["name"],
        system_message=time_verification_config["system_message"],
        llm_config=base_llm_config
    )
    
    # Create city layer agents
    city_layer = config["travel_planner_agents"]["city_layer"]
    city_agent_config = city_layer["agent_0_days_cities"]
    agents[city_agent_config["name"]] = autogen.AssistantAgent(
        name=city_agent_config["name"],
        system_message=city_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    flight_agent_config = city_layer["agent_1_flight_lookup"]
    agents[flight_agent_config["name"]] = autogen.AssistantAgent(
        name=flight_agent_config["name"],
        system_message=flight_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    transport_agent_config = city_layer["agent_2_transport"]
    agents[transport_agent_config["name"]] = autogen.AssistantAgent(
        name=transport_agent_config["name"],
        system_message=transport_agent_config["system_message"],
        llm_config=base_llm_config
    )
    city_verification_config = city_layer["verification_agent"]
    agents[city_verification_config["name"]] = autogen.AssistantAgent(
        name=city_verification_config["name"],
        system_message=city_verification_config["system_message"],
        llm_config=base_llm_config
    )
    
    # Create within-city layer agents
    within_city_layer = config["travel_planner_agents"]["within_city_layer"]
    
    site_agent_config = within_city_layer["agent_0_sites"]
    agents[site_agent_config["name"]] = autogen.AssistantAgent(
        name=site_agent_config["name"],
        system_message=site_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    food_agent_config = within_city_layer["agent_1_restaurants"]
    agents[food_agent_config["name"]] = autogen.AssistantAgent(
        name=food_agent_config["name"],
        system_message=food_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    hotel_agent_config = within_city_layer["agent_2_hotel"]
    agents[hotel_agent_config["name"]] = autogen.AssistantAgent(
        name=hotel_agent_config["name"],
        system_message=hotel_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    transport_agent_config = within_city_layer["agent_3_transport"]
    agents[transport_agent_config["name"]] = autogen.AssistantAgent(
        name=transport_agent_config["name"],
        system_message=transport_agent_config["system_message"],
        llm_config=base_llm_config
    )
    
    activity_verification_config = within_city_layer["verification_agent"]
    agents[activity_verification_config["name"]] = autogen.AssistantAgent(
        name=activity_verification_config["name"],
        system_message=activity_verification_config["system_message"],
        llm_config=base_llm_config
    )
    
    # Create orchestrator agent
    orchestrator_config = config["travel_planner_agents"]["orchestrator"]
    agents[orchestrator_config["name"]] = autogen.AssistantAgent(
        name=orchestrator_config["name"],
        system_message=orchestrator_config["system_message"],
        llm_config=base_llm_config
    )
    
    return agents

def create_group_chat(agents: Dict[str, autogen.Agent]) -> autogen.GroupChat:
    """Create a group chat with all agents."""
    agent_list = list(agents.values())
    
    return autogen.GroupChat(
        agents=agent_list,
        messages=[],
        max_round=50
    )

def handle_function_call(agent_name, func_call: Dict[str, Any]) -> Any:
    """Handle function calls made by agents"""
    func_name = func_call.get("name")
    func_args = func_call.get("arguments", {})

    print(f"\n[API Call] {agent_name} is calling {func_name} with args: {func_args}\n")
    
    if func_name not in function_map:
        return {"error": f"Function {func_name} not found"}
    
    try:
        result = function_map[func_name](**func_args)
        return result
    except Exception as e:
        return {"error": f"Error executing {func_name}: {str(e)}"}

def register_function_callbacks(agents: Dict[str, autogen.Agent]):
    """Register function callbacks for agents that support function calling."""
    for name, agent in agents.items():
        if isinstance(agent, autogen.AssistantAgent):
            def trigger(message, sender=None):
                """Trigger only if the message contains a function_call."""
                return isinstance(message, dict) and "function_call" in message

            def reply_func(sender, message, agent_name=name):
                """Handle the actual function call."""
                function_call = message.get("function_call")
                if function_call:
                    return handle_function_call(agent_name, function_call)
                return None

            agent.register_reply(trigger, reply_func)


def main():
    # Create configs directory path
    configs_dir = Path("configs")
    
    # Load agent configuration
    config = load_agent_config(configs_dir / "agent_config_main.yaml")
    
    # LLM configuration
    llm_config = {
        "model": "gpt-4.1-nano",  # Specify the model you want to use
        "temperature": 0.7,
        "api_key": os.environ.get("OPENAI_API_KEY"),  # Make sure to set your API key as an environment variable
    }
    
    # Create agents
    agents = create_agents(config, llm_config)
    
    # Register function callbacks
    register_function_callbacks(agents)
    
    # Create group chat
    groupchat = create_group_chat(agents)
    
    # Create chat manager
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    # Start the trip planning process
    agents["user_proxy"].initiate_chat(
        manager,
        message="""
        I'd like to plan a trip. Please help me create a detailed itinerary by asking me
        relevant questions about my preferences, destination interests, time frame, budget,
        and any special requirements.
        
        The planning should follow the layered approach:
        1. First determine timing and seasonality
        2. Then select cities and inter-city transportation
        3. Finally plan specific activities within each city
        
        Each recommendation should be verified by the appropriate verification agent before proceeding.
        Each agent should use relevant APIs to retrieve real data when needed.
        """
    )

if __name__ == "__main__":
    main()