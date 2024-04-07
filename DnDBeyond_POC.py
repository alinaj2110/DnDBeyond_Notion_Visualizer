import asyncio
from pyppeteer import launch
from core.utils import *

char_link = "https://www.dndbeyond.com/characters/76483006"


async def main():
    # Launch the browser
    exec_path = find_chrome_executable()
    if not exec_path:
        print("No Chrome Executable found")
        return
    browser = await launch(executablePath= exec_path, headless=False, defaultViewport=None, args=['--start-fullscreen'])  # Set headless to True if you don't want to see the browser window

    # Create a new page
    page = await browser.newPage()

    # Navigate to a website
    await page.goto(char_link)


    combat_tags = ["#character-tools-target",".ct-character-sheet__inner",
                    ".ct-subsections" , ".ct-subsection.ct-subsection--primary-box",
                    ".ddbc-tab-list",".ddbc-tab-list__content",".ddbc-tab-options__body"]
    element = await get_element(combat_tags, page)
    await highlight_element(element, page)
    text = await get_text_content(element, page)
    # Close the browser
    await browser.close()

# Run the main function
asyncio.run(main())




