import asyncio
from playwright.async_api import async_playwright, Playwright


async def run(url):
    async with async_playwright() as playwright:
        playwright.selectors.set_test_id_attribute('data-test-id')
        chromium = playwright.chromium
        
        browser = await chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto(url)
        board_title =  await page.get_by_test_id("board-title").inner_text()

        pin_count = await page.get_by_test_id("pin-count").text_content()
        pin_count = int(pin_count.strip('Pins'))

        feed = page.get_by_test_id("feed").get_by_role("list").nth(0)
        url_list = await collect_board(feed, pin_count)
      
        await browser.close()
        return url_list
 
 
                 

    
        
    #return urlList
 
async def collect_board(feed, pin_count):
    url_list = []
    i = 0
    repeats = 0
 
    while i < pin_count-2:
        
        grid_element = feed.locator(f"[data-grid-item-idx='{i}']")
         
        if await grid_element.count() > 0:        
            img_element = grid_element.locator('img') 

            if await img_element.count() > 0:      
                repeats = 0
                url = await img_element.get_attribute('src')
                url_list.append(url)
                i += 1

            else:
                i+=1
                continue
        else:
            repeats +=1
            
            if repeats > 5:            
                print("repeat")
                await feed.screenshot(path=f"viewport_screenshot{repeats}.png")
                await feed.evaluate(f"window.scrollBy(0, -100)")
            else:
                await feed.evaluate(f"window.scrollBy(0, window.innerHeight)")
            await asyncio.sleep(1)
            print("slept")
        print("i: ",i)
    return url_list  

if __name__ == "__main__":
    url = ""
    run_= asyncio.run(run(url))
