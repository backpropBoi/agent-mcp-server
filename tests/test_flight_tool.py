from unittest.mock import patch
from app.main import top_mcp, register_tools, register_proxy
from fastmcp import Client
import pytest


@pytest.fixture
def get_mcp_server():
    register_tools(top_mcp)
    register_proxy(top_mcp)
    return top_mcp



# Mock API responses


MOCK_LIVE_FLIGHTS = {
    "time": 1743465600,
    "states": [
        ["a808c2", "EK569", "United Arab Emirates", 1743465600, 1743465600,
         55.3657, 25.2513, 10972.8, False, 250.0, 90.0, 0.0, None, 11277.6, "2000", False, 0]
    ]
}

MOCK_DEPARTURE_FLIGHTS = [
    {
        "icao24": "a808c2",
        "firstSeen": 1743465600,
        "estDepartureAirport": "VOBL",
        "lastSeen": 1743480000,
        "estArrivalAirport": "OMDB",
        "callsign": "EK569",
    }
]

MOCK_ARRIVAL_FLIGHTS = [
    {
        "icao24": "a808c2",
        "firstSeen": 1743465600,
        "estDepartureAirport": "VOBL",
        "lastSeen": 1743480000,
        "estArrivalAirport": "OMDB",
        "callsign": "EK569",
    }
]

MOCK_AIRCRAFT_FLIGHTS = [
    {
        "icao24": "a808c2",
        "firstSeen": 1743465600,
        "estDepartureAirport": "VOBL",
        "lastSeen": 1743480000,
        "estArrivalAirport": "OMDB",
        "callsign": "EK569",
    }
]

MOCK_AIRCRAFT_POSITION = {
    "time": 1743465600,
    "states": [
        ["a808c2", "EK569", "United Arab Emirates", 1743465600, 1743465600,
         55.3657, 25.2513, 10972.8, False, 250.0, 90.0, 0.0, None, 11277.6, "2000", False, 0]
    ]
}


# Tests


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_name, params, mock_return, expected",
    [
        (
            "get_live_flights",
            {},
            MOCK_LIVE_FLIGHTS,
            "EK569",
        ),
        (
            "get_flights_by_departure_airport",
            {"airport_icao": "VOBL", "begin": 1743465600, "end": 1743552000},
            MOCK_DEPARTURE_FLIGHTS,
            "VOBL",
        ),
        (
            "get_flights_by_arrival_airport",
            {"airport_icao": "OMDB", "begin": 1743465600, "end": 1743552000},
            MOCK_ARRIVAL_FLIGHTS,
            "OMDB",
        ),
        (
            "get_flights_by_aircraft",
            {"icao24": "a808c2", "begin": 1743465600, "end": 1743552000},
            MOCK_AIRCRAFT_FLIGHTS,
            "a808c2",
        ),
        (
            "get_aircraft_position",
            {"icao24": "a808c2"},
            MOCK_AIRCRAFT_POSITION,
            "EK569",
        ),
    ],
)
async def test_flight_tools(get_mcp_server, tool_name, params, mock_return, expected):
    server = get_mcp_server
    with patch("app.tools.flight_tool._get", return_value=mock_return):
        async with Client(server) as client:
            tools = await client.list_tools()
            tool_names = [t.name for t in tools]
            assert tool_name in tool_names, f"Tool '{tool_name}' not registered"

            result = await client.call_tool(tool_name, params)
            assert expected in result[0].text


@pytest.mark.asyncio
async def test_all_flight_tools_are_registered(get_mcp_server):
    """Ensure all 5 flight tools are discoverable by the MCP server."""
    expected_tools = {
        "get_live_flights",
        "get_flights_by_departure_airport",
        "get_flights_by_arrival_airport",
        "get_flights_by_aircraft",
        "get_aircraft_position",
    }
    server = get_mcp_server
    async with Client(server) as client:
        tools = await client.list_tools()
        registered = {t.name for t in tools}
        assert expected_tools.issubset(registered), (
            f"Missing tools: {expected_tools - registered}"
        )