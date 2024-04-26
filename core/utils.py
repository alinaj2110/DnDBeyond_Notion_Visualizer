import sys
import os
from asyncio import sleep
from core.Singleton import *

shared_data = Singleton()

async def get_element(elementtags:str | list):
    if type(elementtags) is list:
        elementtags = list(map(lambda x: str(x).replace(" ","."), elementtags))
        elementtags = " .".join(elementtags)
    return await shared_data.page.querySelector(elementtags)

async def get_tab_button(tabstr:str):
    tabstr = tabstr.lower()
    tab_buttons = await shared_data.page.querySelectorAll('.styles_tabs__aTttL button')
    for btn in tab_buttons:
        btn_txt = await get_text_content(btn)
        if tabstr == btn_txt.lower():
            return btn
    return None

async def get_text_content(element):
    text = None
    if element:
        text = await (await element.getProperty('textContent')).jsonValue()
    return text

# Highlight the accessed element during debug mode
async def highlight_element(element):
    if element:
        await element._scrollIntoViewIfNeeded()
        await shared_data.page.evaluate('(element) => { element.style.border = "5px solid purple"; }', element)
        await sleep(2)
        await shared_data.page.evaluate('''(element) => {element.style.border = 'none'; }''', element)

async def list_all_elements():
    with open("other_info_files/all_elements_dndbeyond.csv","w") as f:
        f.write("TAG,CLASS,ID\n")
        # Select all elements on the page using the wildcard selector '*'
        if shared_data.page:
            all_elements = await shared_data.page.querySelectorAll('*')

            # Iterate over the list of elements and print their information
            for element in all_elements:
                tag_name = await (await element.getProperty('tagName')).jsonValue()
                class_name = await (await element.getProperty('className')).jsonValue()
                id_name = await (await element.getProperty('id')).jsonValue()
                if tag_name in ["DIV","SPAN"]:
                    f.write(f'{tag_name},{class_name},{id_name}\n')

def find_chrome_executable():
    # Windows
    if sys.platform.startswith('win'):
        chrome_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.getenv('PROGRAMFILES'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
        ]
    # macOS
    elif sys.platform.startswith('darwin'):
        chrome_paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary',
        ]
    # Linux
    else:
        chrome_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
        ]

    # Check if the Chrome executable exists
    for path in chrome_paths:
        if os.path.exists(path):
            return path

    # Chrome executable not found
    return None

# Example usage
if __name__ == "__main__":
    chrome_executable_path = find_chrome_executable()
    print(chrome_executable_path)