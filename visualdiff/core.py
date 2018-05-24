import asyncio
import logging
import os
import shutil
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageColor
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

    async def get_browser(self):
        if self.browser is None:
            self.browser = await launch(**self.browser_kwargs)

    async def get_screenshot(self, url: str,
                             request_handler_func=None,
                             sleep_delay=0,
                             width=None, height=None,
                             emulate=None,
                             **kwargs) -> Path:
        await self.get_browser()
        page = await self.browser.newPage()

        if request_handler_func:
            await page.setRequestInterception(True)
            page.on('request', request_handler_func)

        if width or height:
            change_viewport = dict(width=width, height=height)
            await page.setViewport(change_viewport)
        if emulate:
            await page.emulate(emulate)
        options = kwargs
        await page.goto(url, options)
        # disable CSS animations
        await page.addStyleTag(dict(content='*{transition: none !important}'))
        await asyncio.sleep(sleep_delay)  # seconds delay for JS animations

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
                      cookies=None,
                      **kwargs):
        if not master_path.is_absolute():
            raise Exception("Please provide an absolute master_path")

        if cookies:
            await self.set_cookies(cookies)
        screenshot = await self.get_screenshot(url, **kwargs)
        try:
            differences = None
            if master_path.exists():
                logger.debug(f"Comparing {master_path} with {screenshot}")
                differences = self.image_compare(master_path, screenshot)
                if differences is not None and save_differences:
                    self.save_diff(screenshot, differences, master_path)
                logger.info(f"Differences: {differences}")
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
        return differences

    @staticmethod
    def save_diff(screenshot, differences, master_path):
        name, ext = os.path.splitext(master_path)
        differences_path = name + ".diff" + ext
        diffimg = Image.open(screenshot)
        dr = ImageDraw.Draw(diffimg)
        dr.rectangle(differences, outline=ImageColor.getrgb('red'))
        diffimg.save(differences_path)

        logger.warning(
            "Copied screenshot with differences to %s" % differences_path
        )

    def __del__(self):
        if self.browser:
            self.browser.close()
            self.browser = None

    async def set_cookies(self, cookies):
        await self.get_browser()
        page = await self.browser.newPage()
        for cookie in cookies:
            if cookie.get('value'):
                await page.setCookie(
                    cookie
                )
            else:
                await page.deleteCookie(
                    cookie
                )
