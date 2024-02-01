import time
import psutil
import pygetwindow as gw
def get_browser_url(browser_name):
    # Iterate over all running processes
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if the process is related to the specified browser
            if browser_name.lower() in process.info['name'].lower():
                # Fetch the first window of the specified browser
                browser_window = gw.getWindowsWithTitle(browser_name)[0]

                # Extract the URL from the browser window
                browser_url = browser_window.title
                return [browser_url]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return []

# Example usage with a loop checking every 10 seconds
while True:
    browsers = ['Chrome', 'Brave', 'Firefox']

    for browser in browsers:
        browser_urls = get_browser_url(browser)

        if browser_urls:
            print(f"URL open in {browser} browser:")
            print(browser_urls[0])
        else:
            print(f"No {browser} processes found.")

    # Sleep for 10 seconds
    time.sleep(4)
