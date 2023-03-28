// puppeteer-extra is a drop-in replacement for puppeteer,
// it augments the installed puppeteer with plugin functionality
const puppeteer = require('puppeteer-extra')
const process = require('process');

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

workspace_name = process.argv[2]
profile_path = process.argv[3]

console.log(profile_path)

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
    const page = await browser.newPage()
    console.log(`https://${workspace_name}.slack.com/admin`)
    await page.goto(`https://${workspace_name}.slack.com/admin`)
    await page.waitForTimeout(4000)
    console.log("click login with Google")
    await page.click('#google_login_button')
    await page.waitForTimeout(2000)
    //await page.screenshot({ path: '/web-automation/slack-poc-vol/snapshots/slack/issue.png', fullPage: true })
    await page.click('#view_container > div > div > div.pwWryf.bxPAYd > div > div.WEQkZc > div > form > span > section > div > div > div > div > ul > li.JDAKTe.ibdqA.W7Aapd.zpCp3.SmR8 > div > div.d2laFc > div > div.WBW9sf')
    console.log('Logged In')
    console.log('Taking snapshot')
    await page.waitForTimeout(10000)
    await page.screenshot({ path: `/web-automation/slack-poc-vol/snapshots/slack/${workspace_name}.png`, fullPage: true })
    console.log('All done')
    await page.close();
    await browser.close();
})


// xvfb-run --auto-servernum node index.js