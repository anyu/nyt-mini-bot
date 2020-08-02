import puppeteer from 'puppeteer';
import fs from 'fs';

const url='https://www.nytimes.com/crosswords/game/mini';

(async () => {
  try {
    const browser = await puppeteer.launch({ defaultViewport: null });
    const [page] = await browser.pages();

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
    console.log(`Screenshot saved to ${screenshotPath}!\n`)

    const clueNumElement = 'span[class^="Clue-label"]'
    const clueElement = 'span[class^="Clue-text"]'

    console.log('Clues loaded\n')

    const clueNums = await page.$$eval(clueNumElement,
      elem => elem.map( c => c.textContent)
    )
    const clues = await page.$$eval(clueElement,
      elem => elem.map( c => c.textContent)
    )

    for (const c of clues) {
      console.log(`${c}\n`);
      fs.appendFileSync('clues.txt', c + '\r\n');

    }

    browser.close();

  } catch (err) {
    console.error(err);
  }
})();