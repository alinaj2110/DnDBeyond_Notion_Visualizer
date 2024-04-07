import sys
import os
from pyppeteer import page

async def get_element(elementtags:str | list, page: page):
    if elementtags is list:
        elementtags = " ".join(elementtags)
    return await page.querySelector(" ".join(elementtags))

async def get_text_content(element, page):
    value = None
    if element:
        value = await page.evaluate("(el) => el.textContent", element)
    return value

async def highlight_element(element, page: page):
    if element:
        await page.evaluate('(element) => { element.style.border = "10px solid purple"; }', element)


async def list_all_elements(page: page):
    with open("other_info_files/all_elements_dndbeyond.csv","w") as f:
        f.write("TAG,CLASS,ID\n")
        # Select all elements on the page using the wildcard selector '*'
        all_elements = await page.querySelectorAll('*')

        # Iterate over the list of elements and print their information
        for element in all_elements:
            tag_name = await (await element.getProperty('tagName')).jsonValue()
            class_name = await (await element.getProperty('className')).jsonValue()
            id_name = await (await element.getProperty('id')).jsonValue()
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