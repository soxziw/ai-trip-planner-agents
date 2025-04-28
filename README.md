# AI Trip Planner with Multi-Agent Architecture

This project implements a sophisticated trip planning system using multiple AI agents, each specializing in different aspects of travel planning.

## Architecture

The system uses a 3-layer architecture of specialized agents:

### Layer 0: Time & Seasonality
- **Time Slot Agent**: Determines optimal travel months, peak vs. off-peak seasons, and time windows
- **Time Verification Agent**: Verifies season/weather data and event timing

### Layer 1: City & Transportation
- **City Planning Agent**: Recommends cities and allocates appropriate days for each
- **Transportation Agent**: Plans flights, connections, and inter-city travel
- **City Transport Verification Agent**: Validates city and transportation plans

### Layer 2: City-Specific Activities
- **Sites Agent**: Plans attractions and creates day-by-day itineraries
- **Restaurant Agent**: Recommends dining options aligned with activities
- **Accommodation Agent**: Suggests hotels based on location and preferences
- **Local Transportation Agent**: Plans within-city movement (public transit, car, etc.)
- **Activities Verification Agent**: Validates all within-city plans

These specialists are coordinated by an **Orchestrator Agent** that ensures a cohesive planning process.

## Key Features

- Strict verification at each planning layer
- Data-backed recommendations with specific justifications
- Logical sequencing of planning activities
- Comprehensive conflict resolution
- Detailed, day-by-day final itinerary

## Requirements

- Python 3.8+
- OpenAI API key (set as environment variable `OPENAI_API_KEY`)
- Dependencies listed in `requirements.txt`

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python trip_planner_agents.py
```

Follow the prompts to specify your travel preferences and requirements.

## Extensibility

Additional API integrations can be added to enhance functionality:
- Flight booking APIs for real-time pricing
- Hotel availability APIs
- Restaurant reservation systems
- Weather data services

These would further improve the accuracy and practicality of the generated travel plans.


total budget not specific ones