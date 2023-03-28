// puppeteer-extra is a drop-in replacement for puppeteer,
// it augments the installed puppeteer with plugin functionality
const puppeteer = require('puppeteer-extra')
const process = require('process');

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

admin_email = process.argv[2]
admin_password = process.argv[3]
profile_path = process.argv[4]

launch_config = {
    userDataDir : profile_path,
    headless: false,
    args: [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-setuid-sandbox",
        "--no-sandbox",
    ]
}

// puppeteer usage as normal
puppeteer.launch(launch_config).then(async browser => {
    console.log('Opening gmail..')
    const page = await browser.newPage()
    await page.goto('https://www.google.com/gmail/about')
    await page.waitForTimeout(1000)
    await page.click('body > header > div > div > div > a.button.button--medium.button--mobile-before-hero-only')
    console.log('Email entered...')
    await page.waitForTimeout(2000)
    await page.type('#identifierId',admin_email,{delay : 100})
    await page.click('#identifierNext > div > button > span')
    console.log('Password entered ')
    await page.waitForTimeout(2000)
    await page.type('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input',admin_password,{delay : 100})
    await page.click('#passwordNext > div > button > span')
    await page.waitForTimeout(5000)
    console.log('Taking snapshot..')
    await page.screenshot({ path: `/web-automation/slack-poc-vol/snapshots/gmail/${admin_email}.png`, fullPage: true })
    await page.waitForTimeout(30000)
    console.log('Login successful')
    await page.close();
    await browser.close();
})


// xvfb-run --auto-servernum node index.js