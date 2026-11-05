const {chromium}=require('/Users/chenguagnghui/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/Users/chenguagnghui/Library/Caches/ms-playwright/chromium-1228/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing',headless:true});
 const page=await browser.newPage({viewport:{width:1100,height:1100}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file:///Users/chenguagnghui/tutor/Physics11/forces-review.html');
 await page.locator('#page-1').screenshot({path:'tmp/forces-review-qa/page-1-screen.png'});
 await page.emulateMedia({media:'print'});
 console.log('Print layout:', await page.locator('main > section').evaluateAll(ss=>ss.map(s=>({page:s.id,height:s.getBoundingClientRect().height,lastContent:s.lastElementChild.getBoundingClientRect().bottom-s.getBoundingClientRect().top}))));
 await page.pdf({path:'output/pdf/forces-review.pdf',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false});
 await page.emulateMedia({media:'screen'});
 await page.setViewportSize({width:390,height:844});
 console.log('Mobile:',await page.evaluate(()=>({viewport:innerWidth,content:document.documentElement.scrollWidth,questions:document.querySelectorAll('.question').length,anchors:[...document.querySelectorAll('a[href^="#"]')].every(a=>document.querySelector(a.getAttribute('href')))})));
 await page.screenshot({path:'tmp/forces-review-qa/mobile.png'});
 console.log('Page errors:',errors);
 if(errors.length)throw Error(errors.join('; '));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
