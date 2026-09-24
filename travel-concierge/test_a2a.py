import asyncio
import os
import httpx
from a2a.client import ClientConfig, ClientFactory
from a2a.types import (
    AgentCard,
    FilePart,
    Message,
    Part,
    Role,
    TaskArtifactUpdateEvent,
    TextPart,
    TransportProtocol,
)
from google.auth import default
from google.auth.transport.requests import Request as AuthRequest

async def main():
    credentials, _ = default()
    credentials.refresh(AuthRequest())
    headers = {"Authorization": f"Bearer {credentials.token}"}
    
    async with httpx.AsyncClient(headers=headers, timeout=120) as client:
        resp = await client.get("http://localhost:8000/api/a2a/app/.well-known/agent-card.json")
        resp.raise_for_status()
        card = AgentCard(**resp.json())
        card.url = "http://localhost:8000/api/a2a/app"
        
        factory = ClientFactory(ClientConfig(supported_transports=[TransportProtocol.jsonrpc, TransportProtocol.http_json], httpx_client=client))
        a2a_client = factory.create(card)
        
        msg = Message(
            message_id="test1234",
            role=Role.user,
            parts=[Part(root=TextPart(text="Calculate total cost for 4 people at $2,450 USD each with a 12% discount and 8% tax using python."))]
        )
        
        async for event in a2a_client.send_message(msg):
            print(event)

asyncio.run(main())
