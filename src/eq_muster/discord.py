import logging

import httpx

logger = logging.getLogger(__name__)

SCALE_LABEL = {
    10: "1",
    20: "2",
    30: "3",
    40: "4",
    45: "5弱",
    50: "5強",
    55: "6弱",
    60: "6強",
    70: "7",
}

SCALE_COLOR = {
    10: 0x00BFFF,
    20: 0x00BFFF,
    30: 0xFFFF00,
    40: 0xFF8C00,
    45: 0xFF4500,
    50: 0xFF4500,
    55: 0xFF0000,
    60: 0xFF0000,
    70: 0x8B0000,
}


def _build_embed(data: dict) -> dict:
    eq = data.get("earthquake", {})
    hypo = eq.get("hypocenter", {})
    max_scale = eq.get("maxScale", -1)

    name = hypo.get("name", "不明")
    magnitude = hypo.get("magnitude", "?")
    depth = hypo.get("depth", "?")
    intensity = SCALE_LABEL.get(max_scale, f"不明({max_scale})")
    color = SCALE_COLOR.get(max_scale, 0x808080)

    occurred_at = eq.get("time", "不明")

    return {
        "title": f"地震情報：震度 {intensity}",
        "color": color,
        "fields": [
            {"name": "震源地", "value": name, "inline": True},
            {"name": "マグニチュード", "value": str(magnitude), "inline": True},
            {"name": "深さ", "value": f"{depth}km", "inline": True},
            {"name": "最大震度", "value": intensity, "inline": True},
            {"name": "発生時刻", "value": occurred_at, "inline": True},
        ],
        "footer": {"text": "情報元: P2P地震情報"},
    }


async def send(webhook_url: str, data: dict) -> None:
    embed = _build_embed(data)
    payload = {"embeds": [embed]}

    async with httpx.AsyncClient() as client:
        resp = await client.post(webhook_url, json=payload)

    if resp.status_code in (200, 204):
        logger.info("Discord通知送信完了")
    else:
        logger.error("Discord通知失敗: %s %s", resp.status_code, resp.text)
