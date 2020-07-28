import puppeteer from 'puppeteer';

const url='https://www.nytimes.com/crosswords/game/mini';

(async () => {
  const browser = await puppeteer.launch({ headless:false, defaultViewport: null, slowMo: 150 });
  const page = await browser.newPage();
  await page.setViewport({ width:0, height:0 });

  // Wait until no more than 2 active connections open
  await page.goto(url, {
    waitUntil: 'networkidle2'
  });
  console.log('Page loaded\n');

  await page.waitForSelector('button[aria-label="OK"]', {
    visible: true,
  });
  await page.click('button[aria-label="OK"]');
  console.log('Modal button clicked\n');

  const element = await page.$('#xwd-board');
  console.log('Crossword board loaded\n')

  const screenshotPath = 'puzzle.png'
  await element.screenshot({ path: screenshotPath });
  console.log(`Screenshot saved to ${screenshotPath}!`)

  browser.close();
})();