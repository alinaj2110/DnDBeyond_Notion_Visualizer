import asyncio
from pyppeteer import launch
from core.utils import find_chrome_executable,list_all_elements

char_link = "https://www.dndbeyond.com/characters/76483006"


async def main():
    # Launch the browser
    exec_path = find_chrome_executable()
    if not exec_path:
        print("No Chrome Executable found")
        return
    browser = await launch(executablePath= exec_path, headless=False)  # Set headless to True if you don't want to see the browser window

    # Create a new page
    page = await browser.newPage()

    # Navigate to a website
    await page.goto(char_link)

   # List all elements on the page
    await list_all_elements(page)

    # Close the browser
    await browser.close()

# Run the main function
asyncio.run(main())




