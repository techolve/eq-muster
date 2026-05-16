import asyncio
import json
import logging

import websockets

logger = logging.getLogger(__name__)

WS_URL_PROD = "wss://api.p2pquake.net/v2/ws"
WS_URL_SANDBOX = "wss://api-realtime-sandbox.p2pquake.net/v2/ws"

CODE_EARTHQUAKE = 551
CODE_TSUNAMI = 552
CODE_USERQUAKE = 554
CODE_USERQUAKE_EVAL = 556


async def listen(on_earthquake=None, sandbox: bool = False):
    url = WS_URL_SANDBOX if sandbox else WS_URL_PROD
    logger.info("P2P地震情報 WebSocket に接続中: %s", url)
    async for ws in websockets.connect(url):
        try:
            async for raw in ws:
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    logger.warning("JSON パース失敗: %s", raw)
                    continue

                code = data.get("code")
                logger.debug("受信 code=%s", code)

                if code == CODE_EARTHQUAKE and on_earthquake:
                    await on_earthquake(data)

        except websockets.ConnectionClosed as e:
            logger.warning("接続が切れました (%s)、再接続します...", e)
            await asyncio.sleep(5)
