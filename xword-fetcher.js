import puppeteer from 'puppeteer';
import fs from 'fs';

const NYT_MINI_URL='https://www.nytimes.com/crosswords/game/mini';
const BOARD_PATH = 'puzzle.png';
const CLUES_PATH = 'clues.txt';

(async () => {
  try {
    // debug
    // const browser = await puppeteer.launch({ headless: false, slowMo: 100, defaultViewport: null });
    // rpi3
    // const browser = await puppeteer.launch({ , defaultViewport: null });
    const browser = await puppeteer.launch({ executablePath: 'chromium-browser', defaultViewport: null });
    const [page] = await browser.pages();

    await page.setViewport({ width: 800, height:1000 });

    // Wait until no more than 2 active connections open
    await page.goto(NYT_MINI_URL, {
      waitUntil: 'networkidle2'
    });
    console.log('Page loaded\n');

    await page.waitForSelector('button[aria-label="OK"]', {
      visible: true,
    });
    await page.click('button[aria-label="OK"]');
    console.log('Modal button clicked\n');

    const element = await page.$('#xwd-board');
    const bounding_box = await element.boundingBox();
    console.log('Crossword board loaded\n')

    await element.screenshot({
      path: BOARD_PATH,
      clip: {
        x: bounding_box.x,
        y: bounding_box.y,
        width: Math.min(bounding_box.width, page.viewport().width),
        height: 390,
      },
    });

    console.log(`Screenshot saved to ${BOARD_PATH}!\n`)

    const clueNumElement = 'span[class^="Clue-label"]'
    const clueElement = 'span[class^="Clue-text"]'

    console.log('Clues loaded\n')

    const clueNums = await page.$$eval(clueNumElement,
      elem => elem.map( c => c.textContent )
    )
    const clues = await page.$$eval(clueElement,
      elem => elem.map( c => c.textContent )
    )

    let cluesFileData = 'ACROSS\r\n'
    let counter = 0;

    for (let i = 0; i < clues.length; i++) {
      if (clueNums[i] == 1) counter++;
      if (counter == 2) {
        cluesFileData += '\nDOWN\r\n';
        counter = 0;
      }
      cluesFileData += `${clueNums[i]} ${clues[i]} \r\n`;
    }

    console.log(cluesFileData);
    fs.writeFileSync(CLUES_PATH, cluesFileData);
    console.log(`Clues saved to ${CLUES_PATH}!`);

    browser.close();

  } catch (err) {
    console.error(err);
  }
})();