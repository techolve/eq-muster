import asyncio
import logging
import os

from dotenv import load_dotenv

from eq_muster import discord
from eq_muster.client import listen

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _get_config() -> tuple[str, int, bool]:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        raise RuntimeError("DISCORD_WEBHOOK_URL が設定されていません")

    min_intensity = int(os.environ.get("MIN_INTENSITY", "3"))
    sandbox = os.environ.get("SANDBOX", "").lower() in ("1", "true", "yes")
    return webhook_url, min_intensity, sandbox


def _intensity_value(max_scale: int) -> int:
    return max_scale // 10


async def main() -> None:
    webhook_url, min_intensity, sandbox = _get_config()
    logger.info("起動: 最小震度=%s sandbox=%s", min_intensity, sandbox)

    async def on_earthquake(data: dict) -> None:
        eq = data.get("earthquake", {})
        max_scale = eq.get("maxScale", -1)

        if max_scale < 0:
            return

        if _intensity_value(max_scale) < min_intensity:
            logger.info("震度フィルタ通過せず (maxScale=%s)", max_scale)
            return

        hypo = eq.get("hypocenter", {})
        logger.info(
            "地震検知: %s M%s 深さ%skm maxScale=%s",
            hypo.get("name", "不明"),
            hypo.get("magnitude", "?"),
            hypo.get("depth", "?"),
            max_scale,
        )
        await discord.send(webhook_url, data)

    await listen(on_earthquake=on_earthquake, sandbox=sandbox)


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run()
