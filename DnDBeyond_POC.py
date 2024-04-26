import argparse
import asyncio
from pyppeteer import launch
from core.utils import *
from core.AllActions import *
from core.Singleton import *
from pyppeteer_stealth import stealth

# char_link = "https://www.dndbeyond.com/characters/76483006"
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

    action_button = await get_tab_button("Actions")
    spells_button = await get_tab_button("Spells")
    
    all_actions = AllActions(action_button)
    await all_actions.extract_all_stat_elements()

    all_spells = Spells(spells_button)
    await all_spells.extract_all_spells()

    # Close the browser
    await browser.close()

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())




