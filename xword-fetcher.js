import puppeteer from 'puppeteer';
import fs from 'fs';
import wrap from 'wordwrap';

const nytMiniURL='https://www.nytimes.com/crosswords/game/mini';
const boardPath = 'xwdBoard.png';
const puzzleTextPath = 'puzzle.txt';

// DOM selectors - subject to changes on NYT xword page
const modalBtnSelector = 'button[aria-label="OK"]';
const xwdBoardSelector = '#xwd-board';
const puzzleDateSelector = '[class^="PuzzleDetails-date"]';
const clueNumSelector = 'span[class^="Clue-label"]';
const clueSelector = 'span[class^="Clue-text"]';

const acrossTitle = '\nACROSS\r\n';
const downTitle = '\nDOWN\r\n';

(async () => {
  try {
    // debug
    // const browser = await puppeteer.launch({ headless: false, slowMo: 100, defaultViewport: null });
    // use chromium-browser for rpi3
    const browser = await puppeteer.launch({ executablePath: 'chromium-browser', defaultViewport: null });
    const [page] = await browser.pages();

    await page.setViewport({ width: 800, height:1000 });

    // Wait until no more than 2 active connections open
    await page.goto(nytMiniURL, { waitUntil: 'networkidle2' });
    console.log('* Page loaded');

    await page.waitForSelector(modalBtnSelector, { visible: true });
    await page.click(modalBtnSelector);
    console.log('* Modal button clicked');

    // Retrieve xword board
    const xwdBoardElem = await page.$(xwdBoardSelector);
    const xwdBoardBoundingBox = await xwdBoardElem.boundingBox();
    console.log('* Board loaded')

    await xwdBoardElem.screenshot({
      path: boardPath,
      clip: {
        x: xwdBoardBoundingBox.x,
        y: xwdBoardBoundingBox.y,
        width: Math.min(xwdBoardBoundingBox.width, page.viewport().width),
        height: 390,
      },
    });
    console.log(`* Board screenshot saved to ${boardPath}`)

    // Retrieve puzzle date
    const puzzleDateElem = await page.$$eval(puzzleDateSelector, 
      elem => elem.map( c => c.textContent )
    )
    const puzzleDate = puzzleDateElem[0];
    console.log(`* Puzzle date found: ${puzzleDate}`)

    // Retrieve clues
    const clueNums = await page.$$eval(clueNumSelector,
      elem => elem.map( c => c.textContent )
    )
    const clues = await page.$$eval(clueSelector,
      elem => elem.map( c => c.textContent )
    )
    console.log('* Clues found')

    // Format and write date/clues to file
    let puzzleText = `${puzzleDate}\n${acrossTitle}`;
    let clueColumn = 0;
    let wrappedClue = '';

    for (let i = 0; i < clues.length; i++) {
      if (clueNums[i] == 1) clueColumn++;
      if (clueColumn == 2) {
        puzzleText += downTitle;
        clueColumn = 0;
      }
      wrappedClue = wrap(32)(`${clueNums[i]} ${clues[i]}`)
      puzzleText += `${wrappedClue}\n`;
    }

    fs.writeFileSync(puzzleTextPath, puzzleText);
    console.log(`* Puzzle text saved to ${puzzleTextPath}\n`);
    console.log(puzzleText);

    browser.close();

  } catch (err) {
    console.error(err);
  }
})();