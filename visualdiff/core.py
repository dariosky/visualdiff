import logging
import os
import re
import shutil
import tempfile
from pathlib import Path

from PIL import Image, ImageChops
from pyppeteer.launcher import launch

logger = logging.getLogger(__name__)


def get_master_path(url: str, **kwargs) -> Path:
    result = Path("visualdiff_masters")
    safe_url = re.sub('[^0-9a-zA-Z]', '_', url)
    result /= safe_url + ".png"
    logger.debug(f"URL: {url} => {result}")
    return result


class VisualDiff:
    def __init__(self) -> None:
        super().__init__()
        self.browser = None

    async def get_screenshot(self, url: str, width: int, height: int) -> Path:
        if self.browser is None:
            self.browser = launch()
        page = await self.browser.newPage()

        await page.setViewport(dict(width=width, height=height))
        await page.goto(url)
        temp_file = tempfile.NamedTemporaryFile(prefix='visualdiff_',
                                                suffix='.png', delete=False)
        await page.screenshot({'path': temp_file.name})
        logger.debug(f"saved in {temp_file.name}")
        return Path(temp_file.name)

    @staticmethod
    def image_compare(a: Path, b: Path):
        with Image.open(a) as imga:
            with Image.open(b) as imgb:
                # remove the alpha layer
                imga, imgb = map(lambda img: img.convert('RGB'), [imga, imgb])
                diff = ImageChops.difference(imga, imgb)
                box = diff.getbbox()
                return box

    async def compare(self, url, width=800, height=600,
                      master_path=None):
        if master_path is None:
            master = get_master_path(url, width=width, height=height)
        else:
            master = Path(master_path)
        screenshot = await self.get_screenshot(url, width, height)
        try:
            result = None
            if master.exists():
                logger.debug(f"Comparing {master} with {screenshot}")
                result = self.image_compare(master, screenshot)
                logger.info(result)
            else:
                logger.info("Master file missing, using the current status.")
                master.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
                shutil.copy(screenshot, master)
        except Exception:
            raise
        finally:
            os.unlink(str(screenshot))  # ensure that no temp files are left
        return result
