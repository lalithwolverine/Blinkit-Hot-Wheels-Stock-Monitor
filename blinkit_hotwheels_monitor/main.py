import asyncio
import random
from pathlib import Path

from utils.browser import BrowserManager
from utils.checker import check_stock_status
from utils.logger import log_info, log_success, log_error, giant_alert
from utils.notifier import (
    send_desktop_notification,
    send_discord_notification,
    send_telegram_notification,
)
from utils.sound import start_alarm

from config import (
    PRODUCT_URLS,
    REFRESH_INTERVALS,
    CHECK_TEXT_AVAILABLE,
    CHECK_TEXT_UNAVAILABLE,
    AUTO_CLICK_ADD_TO_CART,
    SCREENSHOT_DIR,
)

RUNNING = True


async def monitor_product(page, url):
    while True:
        try:
            interval = random.choice(REFRESH_INTERVALS)

            log_info(f"[{url}] Next refresh in {interval} seconds...")
            await asyncio.sleep(interval)

            log_info(f"[{url}] Refreshing page...")

            await page.reload(wait_until="networkidle")

            is_available = await check_stock_status(
                page,
                CHECK_TEXT_AVAILABLE,
                CHECK_TEXT_UNAVAILABLE,
            )

            if is_available:
                giant_alert("HOTWHEELS AVAILABLE!")

                log_success(f"STOCK DETECTED: {url}")

                Path(SCREENSHOT_DIR).mkdir(exist_ok=True)

                screenshot_path = (
                    f"{SCREENSHOT_DIR}/stock_detected.png"
                )

                await page.screenshot(path=screenshot_path)

                send_desktop_notification(
                    "HOTWHEELS AVAILABLE!",
                    "OPEN BLINKIT NOW!"
                )

                send_telegram_notification(url)

                send_discord_notification(url)

                if AUTO_CLICK_ADD_TO_CART:
                    try:
                        await page.get_by_text(
                            CHECK_TEXT_AVAILABLE,
                            exact=True
                        ).click(timeout=5000)

                        log_success("Auto clicked Add to cart.")
                    except Exception as e:
                        log_error(f"Auto click failed: {e}")

                start_alarm()

                while True:
                    await asyncio.sleep(1)

        except Exception as e:
            log_error(f"Monitor loop error: {e}")

            await asyncio.sleep(5)


async def main():
    browser_manager = BrowserManager()

    await browser_manager.start()

    tasks = []

    for url in PRODUCT_URLS:
        page = await browser_manager.create_page(url)

        task = asyncio.create_task(
            monitor_product(page, url)
        )

        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        log_info("Shutting down monitor gracefully...")