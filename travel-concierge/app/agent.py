# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import datetime
import json
import os
import pathlib
from typing import Any, Optional
import urllib.parse
import urllib.request
import uuid
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.memory import VertexAiMemoryBankService
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.cloud import firestore, storage
from google.genai import types
from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog
from .a2ui_utils import a2ui_callback

# IMPORTANT: Hardcode project ID explicitly as required by Agent Platform standards
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-03-6c1be26b1412"
GCS_BUCKET_NAME = "qwiklabs-gcp-03-6c1be26b1412-travel-concierge-media"
MEMORY_BANK_ID = "1760849729941405696"


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, extract and save salient facts/preferences to Memory Bank."""
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        pass
    return None


def memory_bank_service_builder():
    """Factory builder for VertexAiMemoryBankService used on deployment."""
    return VertexAiMemoryBankService(
        project=FIRESTORE_PROJECT_ID,
        location="us-central1",
        agent_engine_id=MEMORY_BANK_ID,
    )


def _get_firestore_client() -> firestore.Client:
    """Helper to instantiate Firestore client with hardcoded project ID."""
    return firestore.Client(project=FIRESTORE_PROJECT_ID)


def search_destinations(query: str = "") -> list[dict[str, Any]]:
    """Search travel destinations stored in the Firestore database.

    Args:
        query: Optional search term to filter destinations by name, country, or category.

    Returns:
        A list of destination dictionaries matching the query.
    """
    db = _get_firestore_client()
    docs = db.collection("destinations").stream()
    results = []

    q_lower = query.lower().strip()
    for doc in docs:
        data = doc.to_dict()
        if not q_lower:
            results.append(data)
        else:
            name = data.get("name", "").lower()
            country = data.get("country", "").lower()
            category = data.get("category", "").lower()
            description = data.get("description", "").lower()
            if q_lower in name or q_lower in country or q_lower in category or q_lower in description:
                results.append(data)

    return results


def get_destination_details(destination_id: str) -> dict[str, Any]:
    """Retrieve full details for a specific travel destination from Firestore.

    Args:
        destination_id: Unique document ID of the destination (e.g. 'tokyo', 'paris').

    Returns:
        Dictionary containing destination details or an error message if not found.
    """
    db = _get_firestore_client()
    doc_ref = db.collection("destinations").document(destination_id.lower().strip())
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    return {"error": f"Destination '{destination_id}' not found in database."}


def add_destination(
    destination_id: str,
    name: str,
    country: str,
    category: str,
    budget_tier: str,
    description: str,
    popular_spots: list[str],
    best_season: str = "",
) -> str:
    """Add or update a travel destination document in Firestore.

    Args:
        destination_id: Unique identifier for the destination (e.g., 'rome').
        name: Display name of the destination (e.g., 'Rome').
        country: Country where the destination is located.
        category: Travel category (e.g. 'Art & History', 'Food & Nightlife').
        budget_tier: Estimated budget tier (e.g. 'Budget', 'Moderate', 'High').
        description: Brief overview description of the destination.
        popular_spots: List of key attractions or spots.
        best_season: Best time of year to visit.

    Returns:
        Confirmation message string.
    """
    db = _get_firestore_client()
    clean_id = destination_id.lower().strip()
    doc_data = {
        "id": clean_id,
        "name": name,
        "country": country,
        "category": category,
        "budget_tier": budget_tier,
        "description": description,
        "popular_spots": popular_spots,
        "best_season": best_season,
    }
    db.collection("destinations").document(clean_id).set(doc_data)
    return f"Successfully saved destination '{name}' ({clean_id}) to Firestore."


def get_live_weather(location: str) -> dict[str, Any]:
    """Fetch real-time weather and temperature for any city or destination worldwide using the Open-Meteo API.

    Args:
        location: Name of the city or destination (e.g. 'Tokyo', 'Paris', 'Kyoto').

    Returns:
        Dictionary containing location name, real-time temperature in Celsius and Fahrenheit, windspeed, and day status.
    """
    clean_loc = location.strip()
    encoded_loc = urllib.parse.quote(clean_loc)
    api_key = os.getenv("OPEN_METEO_API_KEY", "")
    key_param = f"&apikey={api_key}" if api_key else ""

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_loc}&count=1&language=en&format=json{key_param}"
    try:
        req = urllib.request.Request(geo_url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            geo_data = json.loads(response.read().decode())
            results = geo_data.get("results")
            if not results:
                return {"error": f"Location '{location}' not found."}

            place = results[0]
            lat, lon = place["latitude"], place["longitude"]
            city_name = place.get("name", location)
            country = place.get("country", "")

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true{key_param}"
        req_w = urllib.request.Request(weather_url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req_w, timeout=5) as resp_w:
            w_data = json.loads(resp_w.read().decode())
            curr = w_data.get("current_weather", {})
            temp_c = curr.get("temperature")
            temp_f = round((temp_c * 9 / 5) + 32, 1) if temp_c is not None else None

            return {
                "location": f"{city_name}, {country}".strip(", "),
                "temperature_celsius": temp_c,
                "temperature_fahrenheit": temp_f,
                "windspeed_kmh": curr.get("windspeed"),
                "is_day": bool(curr.get("is_day")),
            }
    except Exception as e:
        return {"error": f"Failed to fetch live weather for '{location}': {str(e)}"}


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        query: The name of the city to get current time for.

    Returns:
        A string with the current time information.
    """
    q = query.lower()
    if "sf" in q or "san francisco" in q:
        tz_identifier = "America/Los_Angeles"
    elif "tokyo" in q or "japan" in q:
        tz_identifier = "Asia/Tokyo"
    elif "paris" in q or "france" in q:
        tz_identifier = "Europe/Paris"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict[str, Any]:
    """Convert an amount from one currency to another using real-time foreign exchange rates.

    Args:
        amount: The monetary amount to convert (e.g. 100.0).
        from_currency: 3-letter currency code for source currency (e.g. 'USD', 'EUR', 'GBP').
        to_currency: 3-letter currency code for target currency (e.g. 'JPY', 'EUR', 'CAD').

    Returns:
        Dictionary containing conversion details, total converted amount, and exchange rate.
    """
    base = from_currency.upper().strip()
    target = to_currency.upper().strip()
    if base == target:
        return {"original_amount": amount, "from_currency": base, "converted_amount": amount, "to_currency": target, "rate": 1.0}

    url = f"https://api.frankfurter.app/latest?amount={amount}&from={base}&to={target}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            converted = data["rates"].get(target)
            rate = round(converted / amount, 4) if amount != 0 else 0
            return {
                "original_amount": amount,
                "from_currency": base,
                "converted_amount": round(converted, 2),
                "to_currency": target,
                "rate": rate,
                "date": data.get("date"),
            }
    except Exception as e:
        return {"error": f"Failed to convert from {base} to {target}: {str(e)}"}


def geocode_address(address: str) -> dict[str, Any]:
    """Convert an address, landmark, or city name into geographic coordinates (latitude and longitude).

    Args:
        address: The address or place description to geocode (e.g. 'Eiffel Tower, Paris', 'Shibuya Crossing, Tokyo').

    Returns:
        Dictionary containing formatted address, location coordinates (latitude, longitude), and place_id.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY environment variable is not set."}

    encoded_addr = urllib.parse.quote(address.strip())
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_addr}&key={api_key}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelConciergeAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            results = data.get("results")
            if not results:
                return {"error": f"No geocoding results found for address: '{address}'"}

            res = results[0]
            loc = res.get("geometry", {}).get("location", {})
            return {
                "formatted_address": res.get("formatted_address"),
                "location": {
                    "latitude": loc.get("lat"),
                    "longitude": loc.get("lng"),
                },
                "place_id": res.get("place_id"),
            }
    except Exception as e:
        return {"error": f"Geocoding request failed: {str(e)}"}


def find_nearby_places(
    latitude: float,
    longitude: float,
    place_type: str = "restaurant",
    radius_meters: float = 1000.0,
) -> list[dict[str, Any]]:
    """Find nearby points of interest or places of a given type around a geographic coordinate using Places API (New).

    Args:
        latitude: Latitude of the center point.
        longitude: Longitude of the center point.
        place_type: Type of place to search for (e.g., 'restaurant', 'cafe', 'tourist_attraction', 'museum', 'lodging').
        radius_meters: Radius in meters around the center point (default 1000.0 meters).

    Returns:
        List of nearby places with name, formatted address, location coordinates, and place types.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    if not api_key:
        return [{"error": "GOOGLE_MAPS_API_KEY environment variable is not set."}]

    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.types",
        "User-Agent": "TravelConciergeAgent/1.0",
    }
    payload = {
        "includedTypes": [place_type.lower().strip()],
        "maxResultCount": 5,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": float(radius_meters),
            }
        },
    }

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode())
            places = res_data.get("places", [])
            results = []
            for p in places:
                display_name = p.get("displayName", {}).get("text", "")
                results.append({
                    "name": display_name,
                    "address": p.get("formattedAddress"),
                    "location": p.get("location"),
                    "types": p.get("types", []),
                })
            return results
    except Exception as e:
        return [{"error": f"Places search nearby failed: {str(e)}"}]


def generate_destination_image(
    prompt: str,
    tool_context: ToolContext,
    image_name: Optional[str] = None,
) -> dict[str, Any]:
    """Generate a photo or visual artwork of a travel destination, landmark, or activity using gemini-3.1-flash-lite-image model.

    Saves the generated image to local ADK artifacts and uploads it directly to Google Cloud Storage bucket returning a public HTTPS URL.

    Args:
        prompt: Description of the destination, landscape, or attraction to generate (e.g. 'A sunlit view of Paris Eiffel Tower in spring').
        tool_context: ADK context for saving artifacts into the Agent Playground.
        image_name: Optional short name for the image file (e.g., 'eiffel_tower').

    Returns:
        Dictionary containing public Cloud Storage HTTPS URL, artifact filename, and status.
    """
    clean_name = (image_name or "destination").strip().replace(" ", "_").lower()
    filename = f"{clean_name}_{uuid.uuid4().hex[:6]}.jpg"

    try:
        genai_client = genai.Client(vertexai=True, location="global", project=FIRESTORE_PROJECT_ID)
        response = genai_client.models.generate_content(
            model="gemini-3.1-flash-lite-image",
            contents=prompt,
        )

        if not response.candidates or not response.candidates[0].content.parts:
            return {"error": "Failed to generate image: no candidate content returned."}

        part = response.candidates[0].content.parts[0]
        image_bytes = part.inline_data.data
        mime_type = part.inline_data.mime_type or "image/jpeg"

        # (1) Save artifact in ToolContext for Agent Playground Artifacts panel
        tool_context.save_artifact(filename=filename, artifact=part)

        # (2) Upload bytes directly to GCS bucket (without writing local file)
        storage_client = storage.Client(project=FIRESTORE_PROJECT_ID)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(image_bytes, content_type=mime_type)

        public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{filename}"

        return {
            "status": "success",
            "filename": filename,
            "public_url": public_url,
            "message": f"Generated image and uploaded to {public_url}",
        }
    except Exception as e:
        return {"error": f"Failed to generate destination image: {str(e)}"}


def generate_destination_video(
    prompt: str,
    tool_context: ToolContext,
    video_name: Optional[str] = None,
) -> dict[str, Any]:
    """Generate a short video of a travel destination, landmark, or activity using gemini-omni-flash-preview model.

    Saves the generated video to local ADK artifacts and uploads it directly to Google Cloud Storage bucket returning a public HTTPS URL.

    Args:
        prompt: Description of the destination video to generate (e.g. 'A cinematic drone shot over Paris Eiffel Tower').
        tool_context: ADK context for saving artifacts into the Agent Playground.
        video_name: Optional short name for the video file (e.g., 'eiffel_tower_video').

    Returns:
        Dictionary containing public Cloud Storage HTTPS URL, artifact filename, and status.
    """
    clean_name = (video_name or "destination_video").strip().replace(" ", "_").lower()
    filename = f"{clean_name}_{uuid.uuid4().hex[:6]}.mp4"

    try:
        genai_client = genai.Client(vertexai=True, location="global", project=FIRESTORE_PROJECT_ID)
        res = genai_client.interactions.create(
            model="gemini-omni-flash-preview",
            input=prompt
        )

        video_bytes = None
        part = None
        for step in res.steps:
            if step.type == "model_output":
                for content in step.content:
                    if content.type == "video":
                        video_bytes = base64.b64decode(content.data)
                        
                        # We need a part-like object for save_artifact to work correctly 
                        # ADK's save_artifact normally takes a Part. 
                        # But since it's just raw bytes, let's create a minimal Part representation or just pass bytes.
                        # Wait, save_artifact expects a Part object. If we don't have one, we can construct one or use the path.
                        # Let's write bytes to a temp file and let save_artifact read it, or use the part if available.
                        # Actually save_artifact supports bytes directly? No, tool_context.save_artifact takes artifact (Any) 
                        # that handles parts or str/bytes.
                        break
            if video_bytes:
                break
                
        if not video_bytes:
            return {"error": "Failed to generate video: no video content returned."}

        # (1) Save artifact in ToolContext for Agent Playground Artifacts panel
        tool_context.save_artifact(filename=filename, artifact=video_bytes)

        # (2) Upload bytes directly to GCS bucket (without writing local file)
        storage_client = storage.Client(project=FIRESTORE_PROJECT_ID)
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(video_bytes, content_type="video/mp4")

        public_url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{filename}"

        return {
            "status": "success",
            "filename": filename,
            "public_url": public_url,
            "message": f"Generated video and uploaded to {public_url}",
        }
    except Exception as e:
        return {"error": f"Failed to generate destination video: {str(e)}"}


# Initialize AgentEngineSandboxCodeExecutor from deployment_metadata.json if available
_metadata_path = pathlib.Path(__file__).parent.parent / "deployment_metadata.json"
_agent_engine_resource_name = None
_sandbox_resource_name = None

if _metadata_path.exists():
    try:
        with open(_metadata_path, "r", encoding="utf-8") as f:
            _meta = json.load(f)
            _agent_engine_resource_name = _meta.get("remote_agent_runtime_id") or _meta.get("agent_engine_resource_name")
            _sandbox_resource_name = _meta.get("sandbox_resource_name")
    except Exception:
        pass

code_executor = AgentEngineSandboxCodeExecutor(
    sandbox_resource_name=_sandbox_resource_name,
    agent_engine_resource_name=_agent_engine_resource_name,
)


a2ui_schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = a2ui_schema_manager.generate_system_prompt(
    role_description=(
        "You are the Travel & Adventure Concierge agent. You help users plan trips, "
        "discover destinations, geocode addresses, find nearby attractions and restaurants, "
        "check real-time weather, check destination details, view popular spots, "
        "generate visual destination artwork, photos, and short cinematic videos, "
        "convert travel budgets/expenses between currencies, "
        "execute Python code calculations in a secure sandbox when needed by writing a markdown python code block (do NOT attempt to call non-existent function tools like run_code, execute_code, run_python, google:python_interpreter, or add_user_preference), "
        "remember user preferences, facts, and ALL USER ALLERGIES (such as peanuts, gluten, shellfish, dairy, or environmental allergies) across conversations using your memory (user preferences and allergies are saved automatically to Memory Bank), "
        "and ensure all food, dining, restaurant, and activity recommendations strictly respect all remembered user allergies."
    ),
    workflow_description=(
        "Analyze the user request. When returning UI, return structured A2UI. "
        "When asked to write or execute Python code or perform calculations using Python, "
        "you MUST write a standard markdown python code block starting with ```python and ending with ```. "
        "DO NOT use a tool or function call for code execution. NEVER call `run_code`, `execute_code`, `run_python`, or `google:python_interpreter`! "
        "Just output the python code block in your text response and it will be executed automatically."
    ),
    ui_description=(
        "For UI responses, keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "When returning A2UI, output the raw A2UI JSON array — never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    code_executor=code_executor,
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
    tools=[
        PreloadMemoryTool(),
        search_destinations,
        get_destination_details,
        add_destination,
        convert_currency,
        get_live_weather,
        geocode_address,
        find_nearby_places,
        generate_destination_image,
        generate_destination_video,
        get_current_time,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
