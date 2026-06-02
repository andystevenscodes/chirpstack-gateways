import grpc
import json
import os
from chirpstack_api import api

SERVER = "lora.surfiot.nl:443"
TENANT_ID = "675ed13f-9483-4d40-8add-fb5d494b67b0"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}


def save_config(data: dict):
    existing = load_config()
    existing.update(data)
    with open(CONFIG_PATH, "w") as f:
        json.dump(existing, f, indent=2)


def get_api_token() -> str | None:
    return load_config().get("api_token")


def get_gateway_state(gw) -> str:
    state_map = {0: "unknown", 1: "online", 2: "offline"}
    return state_map.get(gw.state, "unknown")


def list_all_gateways() -> list[dict]:
    """Fetch all gateways for the tenant, handling pagination."""
    api_token = get_api_token()
    if not api_token:
        raise RuntimeError("Geen API token geconfigureerd. Ga naar /config.")

    auth_token = [("authorization", f"Bearer {api_token}")]
    channel = grpc.secure_channel(SERVER, grpc.ssl_channel_credentials())
    gtw_client = api.GatewayServiceStub(channel)

    gateways = []
    limit = 100
    offset = 0

    while True:
        req = api.ListGatewaysRequest(
            tenant_id=TENANT_ID,
            limit=limit,
            offset=offset,
        )
        try:
            resp = gtw_client.List(req, metadata=auth_token)
        except grpc.RpcError as e:
            raise RuntimeError(f"gRPC error [{e.code()}]: {e.details()}")

        for gw in resp.result:
            gateways.append({
                "id": gw.gateway_id,
                "name": gw.name,
                "description": gw.description,
                "state": get_gateway_state(gw),
                "last_seen": gw.last_seen_at.ToDatetime().isoformat() if gw.last_seen_at.seconds else None,
            })

        if offset + limit >= resp.total_count:
            break
        offset += limit

    channel.close()
    return gateways