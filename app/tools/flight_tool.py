import os
import httpx
from fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("FlightTools")

# ---------------------------------------------------------------------------
# OpenSky Network API — completely free, no API key required
# Docs: https://openskynetwork.github.io/opensky-api/
# Optional: set OPENSKY_USERNAME and OPENSKY_PASSWORD for higher rate limits
# ---------------------------------------------------------------------------
OPENSKY_BASE_URL = "https://opensky-network.org/api"
OPENSKY_USERNAME = os.getenv("OPENSKY_USERNAME", "")
OPENSKY_PASSWORD = os.getenv("OPENSKY_PASSWORD", "")


def _get(endpoint: str, params: dict | None = None) -> dict:
    """GET request to OpenSky API — works without credentials."""
    url  = f"{OPENSKY_BASE_URL}{endpoint}"
    auth = (OPENSKY_USERNAME, OPENSKY_PASSWORD) if OPENSKY_USERNAME else None
    with httpx.Client(timeout=15) as client:
        response = client.get(url, params=params or {}, auth=auth)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def get_live_flights() -> dict:
    """Get all live flights currently in the air worldwide.

    Returns:
        A dict with a list of all active flights including position,
        altitude, speed, and callsign.
    """
    return _get("/states/all")


@mcp.tool()
def get_flights_by_departure_airport(
    airport_icao: str,
    begin: int,
    end: int,
) -> list:
    """Get all flights that departed from a specific airport in a time range.

    Args:
        airport_icao: ICAO code of the departure airport
                      (e.g. "VOBL" for Bangalore, "OMDB" for Dubai, "EGLL" for London Heathrow).
        begin:        Start of time range as Unix timestamp (e.g. 1743465600).
        end:          End of time range as Unix timestamp (e.g. 1743552000).

    Returns:
        A list of flights that departed from the airport in the given time range.
    """
    return _get(
        "/flights/departure",
        params={"airport": airport_icao, "begin": begin, "end": end},
    )


@mcp.tool()
def get_flights_by_arrival_airport(
    airport_icao: str,
    begin: int,
    end: int,
) -> list:
    """Get all flights that arrived at a specific airport in a time range.

    Args:
        airport_icao: ICAO code of the arrival airport
                      (e.g. "VOBL" for Bangalore, "OMDB" for Dubai, "EGLL" for London Heathrow).
        begin:        Start of time range as Unix timestamp (e.g. 1743465600).
        end:          End of time range as Unix timestamp (e.g. 1743552000).

    Returns:
        A list of flights that arrived at the airport in the given time range.
    """
    return _get(
        "/flights/arrival",
        params={"airport": airport_icao, "begin": begin, "end": end},
    )


@mcp.tool()
def get_flights_by_aircraft(
    icao24: str,
    begin: int,
    end: int,
) -> list:
    """Get all flights made by a specific aircraft in a time range.

    Args:
        icao24: Unique ICAO 24-bit transponder address of the aircraft (e.g. "a808c2").
        begin:  Start of time range as Unix timestamp.
        end:    End of time range as Unix timestamp.

    Returns:
        A list of flights made by the aircraft in the given time range.
    """
    return _get(
        "/flights/aircraft",
        params={"icao24": icao24, "begin": begin, "end": end},
    )


@mcp.tool()
def get_aircraft_position(icao24: str) -> dict:
    """Get the current live position of a specific aircraft.

    Args:
        icao24: Unique ICAO 24-bit transponder address of the aircraft (e.g. "a808c2").

    Returns:
        A dict with the aircraft's current position, altitude, speed, and heading.
    """
    return _get(
        "/states/all",
        params={"icao24": icao24},
    )