import argparse
import asyncio
from pyppeteer import launch
from core.utils import *
from pyppeteer_stealth import stealth

#char_link = "https://www.dndbeyond.com/characters/76483006"
char_link = "https://www.dndbeyond.com/characters/120033071/U6lo2s"

async def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    
    # Add arguments
    parser.add_argument('--debug', action='store_true', help='Debug Mode')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Access the parsed arguments
    debug_mode = args.debug

    # Launch the browser
    exec_path = find_chrome_executable()
    if not exec_path:
        print("No Chrome Executable found")
        return

    headless = False if debug_mode else True
    browser = await launch(executablePath= exec_path, headless=headless, defaultViewport=None, args=['--window-size=1920,1080'])
    # Create a new page
    page = await browser.newPage()
    await stealth(page)
    # Navigate to a website
    await page.goto(char_link)
    await asyncio.sleep(5)

    combat_tags = ["#character-tools-target","ct-character-sheet__inner",
                    "ct-subsections", "ct-subsection ct-subsection--primary-box",
                    "ddbc-tab-list","ddbc-tab-options__content"]
    # #ct-actions-list__heading
    element = await get_element(combat_tags, page)
    if debug_mode: await highlight_element(element, page)

    #Get all the sections of the actions
    combat_action_list = await element.querySelectorAll(".ct-actions-list")
    for comb_action in combat_action_list:
        if debug_mode: await highlight_element(comb_action, page)
        text = await get_text_content(comb_action, page)

    # Close the browser
    await browser.close()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())




