import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
import logging
from asyncio import Semaphore
from app.core.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DaosFunService:
    def __init__(self):
        self.session_manager = SessionManager()

    async def _setup_browser(self):
        """Setup and return playwright browser"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        return browser, playwright

    async def _parse_table_row(self, row) -> Optional[Dict]:
        """Parse a single table row and return structured data"""
        try:
            cols = row.find_all('td')
            
            return {
                'dao_name': cols[0].find('p').text.strip(),
                'twitter_handle': cols[1].find('a').text.strip() if cols[1].find('a') else "N/A",
                'twitter_url': cols[1].find('a')['href'] if cols[1].find('a') else "N/A",
                'market_cap': cols[2].text.strip(),
                'market_cap_change': cols[3].text.strip(),
                'volume': cols[4].text.strip(),
                'treasury': cols[5].text.strip(),
                'treasury_change': cols[6].text.strip(),
                'multiplier': cols[7].text.strip()
            }
        except Exception as e:
            logger.error(f"Error parsing row: {e}")
            return None

    async def _scrape_page(self, page_num: int, browser, semaphore: Semaphore) -> List[Dict]:
        """Scrape a single page"""
        async with semaphore:
            try:
                page = await browser.new_page()
                url = "https://www.daos.fun" if page_num == 1 else f"https://www.daos.fun/?page={page_num}"
                logger.info(f"Scraping page {page_num}: {url}")
                
                await page.goto(url, wait_until='networkidle')
                
                tbody_content = await page.evaluate('''() => {
                    const tbody = document.querySelector('tbody');
                    return tbody ? tbody.innerHTML.trim() : '';
                }''')
                
                if not tbody_content:
                    logger.info(f"No data found on page {page_num}")
                    await page.close()
                    return []
                
                content = await page.content()
                await page.close()
                
                soup = BeautifulSoup(content, 'html.parser')
                rows = soup.find('tbody').find_all('tr')
                
                page_data = []
                for row in rows:
                    row_data = await self._parse_table_row(row)
                    if row_data:
                        page_data.append(row_data)
                
                logger.info(f"Found {len(page_data)} entries on page {page_num}")
                return page_data
                
            except Exception as e:
                logger.error(f"Error scraping page {page_num}: {e}")
                return []

    async def get_dao_data(self) -> pd.DataFrame:
        """
        Scrape DAO data from daos.fun website and return as DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame containing DAO information including name, Twitter,
                         TVL, volume, treasury, and other metrics.
        """
        browser, playwright = await self._setup_browser()
        all_data = []
        
        try:
            semaphore = Semaphore(3)  # Rate limit concurrent requests
            
            tasks = [self._scrape_page(page_num, browser, semaphore) 
                    for page_num in range(1, 5)]
            
            results = await asyncio.gather(*tasks)
            all_data = [item for sublist in results for item in sublist if sublist]
            
        except Exception as e:
            logger.error(f"Error occurred: {e}")
        finally:
            await browser.close()
            await playwright.stop()
        
        df = pd.DataFrame(all_data)
        if not df.empty:
            df.to_csv('daos_fun_data.csv', index=False)
            logger.info(f"Successfully scraped {len(df)} DAOs")
        else:
            logger.warning("No data was scraped")
        
        return df
