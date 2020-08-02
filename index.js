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

    const clueNumber = 'span[class^="Clue-label"]'
    const clueElement = 'span[class^="Clue-text"]'

    const clueNumberHandle = await page.waitForSelector(clueNumber);
    const clueHandle = await page.waitForSelector(clueElement);
    console.log('Clue text loaded\n')

    const clueNumValue = await (await clueNumberHandle.getProperty('textContent')).jsonValue();
    const clueValue = await (await clueHandle.getProperty('textContent')).jsonValue();

    console.log(`Clue: ${clueNumValue}: ${clueValue}`)
    const cluesFile = `${clueNumValue}: ${clueValue}`

    fs.writeFileSync('clues.txt', cluesFile);

    browser.close();

  } catch (err) {
    console.error(err);
  }
})();