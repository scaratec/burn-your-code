// Export the workshop deck to PDF via Chrome DevTools Protocol.
// Usage: python3 -m http.server 8765 (in this folder), then
//        node export-pdf.mjs http://127.0.0.1:8765/index.html deck.pdf   (Node 22+, google-chrome)
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const [url, out] = process.argv.slice(2);
const chrome = spawn('google-chrome', ['--headless=new', '--disable-gpu', '--remote-debugging-port=9333',
  `--user-data-dir=${fs.mkdtempSync(path.join(os.tmpdir(), 'deck-pdf-'))}`, 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch('http://127.0.0.1:9333/json')).json()).find((t) => t.type === 'page'); } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pending = new Map();
ws.addEventListener('message', (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: `${url}?print-pdf` });
await sleep(4000);
const pages = await send('Runtime.evaluate', { expression: "document.querySelectorAll('.pdf-page').length", returnByValue: true });
const pdf = await send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true, marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0 });
fs.writeFileSync(out, Buffer.from(pdf.result.data, 'base64'));
console.log(`pdf-pages in DOM: ${pages.result.result.value}`);
ws.close(); chrome.kill();
