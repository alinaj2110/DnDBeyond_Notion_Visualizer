import argparse
import asyncio
from pyppeteer import launch
from core.utils import *
from core.AllActions import *
from core.Singleton import *
from pyppeteer_stealth import stealth

#char_link = "https://www.dndbeyond.com/characters/76483006"
char_link = "https://www.dndbeyond.com/characters/120033071/U6lo2s"

async def main():

    shared_data = Singleton()
    parser = argparse.ArgumentParser(description='Description of your program')
    
    # Add arguments
    parser.add_argument('--debug', action='store_true', help='Debug Mode')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Access the parsed arguments
    shared_data.debug_enabled = args.debug

    # Launch the browser
    exec_path = find_chrome_executable()
    if not exec_path:
        print("No Chrome Executable found")
        return

    headless = False if shared_data.debug_enabled else True
    browser = await launch(executablePath= exec_path, headless=headless, defaultViewport=None, args=['--window-size=1920,1080'])
    # Create a new page
    shared_data.page = await browser.newPage()
    await stealth(shared_data.page)
    # Navigate to a website
    await shared_data.page.goto(char_link)
    await asyncio.sleep(5)

    combat_tags = ["#character-tools-target","ct-character-sheet__inner",
                    "ct-subsections", "ct-subsection ct-subsection--primary-box",
                    "ddbc-tab-list","ddbc-tab-options__content"]
    # #ct-actions-list__heading
    element = await get_element(combat_tags)
    if shared_data.debug_enabled: await highlight_element(element)

    all_actions = AllActions()
    await all_actions.extract_all_stat_elements(combat_stats_element=element)

    # Close the browser
    await browser.close()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())




