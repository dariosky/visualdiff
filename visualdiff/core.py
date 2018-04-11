import logging
import os
import shutil
import tempfile
from pathlib import Path

from PIL import Image, ImageChops
from pyppeteer.launcher import launch

logger = logging.getLogger('visualdiff.core')


class VisualDiff:
    def __init__(self) -> None:
        super().__init__()
        self.browser = None
        if 'CI' in os.environ:
            # when in Travis CI, go in no-sandbox mode
            #  see https://github.com/miyakogi/pyppeteer/issues/60
            logger.warning("Continuous integration mode, using no-sandbox")
            self.browser_kwargs = {'args': ['--no-sandbox']}
        else:
            self.browser_kwargs = {}

    async def get_screenshot(self, url: str,
                             request_handler_func=None,
                             **kwargs) -> Path:
        if self.browser is None:
            self.browser = await launch(**self.browser_kwargs)
        page = await self.browser.newPage()

        if request_handler_func:
            await page.setRequestInterception(True)
            page.on('request', request_handler_func)

        change_viewport = {k: kwargs.pop(k) for k in list(kwargs.keys())
                           if k in ("width", "height")}
        if change_viewport:
            await page.setViewport(change_viewport)
        emulate = kwargs.pop('emulate', None)
        if emulate:
            await page.emulate(emulate)
        options = kwargs
        await page.goto(url, options)
        temp_file = tempfile.NamedTemporaryFile(prefix='visualdiff_',
                                                suffix='.png', delete=False)
        await page.screenshot({'path': temp_file.name,
                               'type': 'png'})
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

    async def compare(self, url, master_path: Path,
                      master_should_exist=False,
                      save_differences=False,
                      **kwargs):
        if not master_path.is_absolute():
            raise Exception("Please provide an absolute master_path")

        screenshot = await self.get_screenshot(url, **kwargs)
        try:
            result = None
            if master_path.exists():
                logger.debug(f"Comparing {master_path} with {screenshot}")
                result = self.image_compare(master_path, screenshot)
                if result is not None and save_differences:
                    different_path = str(master_path) + "diff.png"
                    shutil.copy(screenshot, different_path)
                    logger.warning(
                        "Copied different screeshot to %s" % different_path
                    )
                logger.info(result)
            else:
                if master_should_exist:
                    raise Exception("Missing master file: %s" % master_path)
                logger.info("Master file missing, using the current status.")
                # ensure folder exists
                master_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(screenshot, master_path)
        except Exception:
            raise
        finally:
            os.unlink(str(screenshot))  # ensure that no temp files are left
        return result
