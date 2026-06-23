const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();

// ─── Extract premium blocks from homepage ───────────────────────────────────
function extractPremiumBlocks() {
    const content = fs.readFileSync('index.html', 'utf-8');
    let headerStart = content.indexOf('<!-- TopNavBar -->');
    let headerEnd   = content.indexOf('<!-- Hero Section -->');
    const headerBlock = content.substring(headerStart, headerEnd).trim();

    let footerStart = content.indexOf('<!-- Footer: Standardized White Background, Black Text -->');
    let footerEnd   = content.indexOf('</footer>') + '</footer>'.length;
    const footerBlock = content.substring(footerStart, footerEnd).trim();

    return { headerBlock, footerBlock };
}

// ─── Font injection helper ───────────────────────────────────────────────────
const OUTFIT_LINK = `<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet"/>`;
const FONT_STYLE_INJECT = `<style>
        body { font-family: "Plus Jakarta Sans", sans-serif !important; }
        h1, h2, h3, h4, h5, h6 { font-family: "Outfit", sans-serif !important; }
    </style>`;

function injectFonts(content) {
    // Replace any existing Lexend/Inter font link
    const oldFontRegex = /https:\/\/fonts\.googleapis\.com\/css2\?family=(?:Lexend|Inter)[^"']+/g;
    content = content.replace(oldFontRegex, 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap');

    // If Outfit link not present at all, inject before </head>
    if (!content.includes('Outfit')) {
        content = content.replace('</head>', `    ${OUTFIT_LINK}\n</head>`);
    }

    // Inject font style override if not present
    if (!content.includes('font-family: "Plus Jakarta Sans"') && !content.includes("font-family: 'Plus Jakarta Sans'")) {
        if (content.includes('<style>')) {
            content = content.replace('<style>', `<style>\n        body { font-family: "Plus Jakarta Sans", sans-serif !important; }\n        h1, h2, h3, h4, h5, h6 { font-family: "Outfit", sans-serif !important; }\n`);
        } else {
            content = content.replace('</head>', `    ${FONT_STYLE_INJECT}\n</head>`);
        }
    }

    return content;
}

// ─── Fix navbar for pages missing it ─────────────────────────────────────────
function fixNavbar(content, headerBlock) {
    if (!content.includes('sticky top-4') && !content.includes('TopNavBar')) {
        const bodyStart = content.indexOf('<body');
        const bodyTagEnd = content.indexOf('>', bodyStart) + 1;
        content = content.substring(0, bodyTagEnd) + '\n\n' + headerBlock + '\n\n' + content.substring(bodyTagEnd);
    }
    return content;
}

// ─── Process all pages ───────────────────────────────────────────────────────
function walk(dir, callback) {
    for (const item of fs.readdirSync(dir)) {
        const full = path.join(dir, item);
        if (['.git','node_modules','assets','.system_generated'].includes(item)) continue;
        const stat = fs.statSync(full);
        if (stat.isDirectory()) walk(full, callback);
        else if (item === 'index.html' && full !== path.join(ROOT, 'index.html')) callback(full);
    }
}

// ─── FIX 1: Homepage title (too long) ────────────────────────────────────────
let homepage = fs.readFileSync('index.html', 'utf-8');
homepage = homepage.replace(
    /<title>Hosterlo \Premium Website Bundle \| Hosting, Free \.com, Email &amp; Gemini Pro Pro<\/title>/,
    '<title>Hosterlo | Cloud Hosting, Free Domain, Email &amp; Gemini Pro</title>'
);
fs.writeFileSync('index.html', homepage, 'utf-8');
console.log('✅ Fixed homepage title length');

// ─── FIX 2: Blog posts – inject fonts ────────────────────────────────────────
const { headerBlock, footerBlock } = extractPremiumBlocks();

const blogDirs = [
    '2025/10/29/go-green-go-fast-why-eco-friendly-wordpress-hosting-isnt-just-a-trend-its-your-business-advantage',
    '2026/04/29/how-to-start-a-website-domain-hosting',
    '2026/04/30/best-web-hosting-for-websites-2026',
    '2026/05/01/checks-before-godaddy-or-hostinger-hosting',
    '2026/05/04/web-hosting-trends-2026-ai',
    '2026/05/05/where-to-purchase-a-domain-name',
];

for (const dir of blogDirs) {
    const filePath = path.join(ROOT, dir, 'index.html');
    if (!fs.existsSync(filePath)) { console.log(`⚠️  Not found: ${filePath}`); continue; }
    let c = fs.readFileSync(filePath, 'utf-8');
    c = injectFonts(c);
    fs.writeFileSync(filePath, c, 'utf-8');
    console.log(`✅ Blog fonts fixed: ${dir}`);
}

// ─── FIX 3: ai-article-writer, dmarc-record-lookup, spf-record-lookup ────────
const toolPages = ['ai-article-writer', 'dmarc-record-lookup', 'spf-record-lookup'];
for (const page of toolPages) {
    const filePath = path.join(ROOT, page, 'index.html');
    if (!fs.existsSync(filePath)) { console.log(`⚠️  Not found: ${filePath}`); continue; }
    let c = fs.readFileSync(filePath, 'utf-8');
    c = injectFonts(c);
    fs.writeFileSync(filePath, c, 'utf-8');
    console.log(`✅ Font fixed: ${page}`);
}

// ─── FIX 4: digioverse & login – inject navbar ───────────────────────────────
const navbarPages = ['digioverse', 'login'];
for (const page of navbarPages) {
    const filePath = path.join(ROOT, page, 'index.html');
    if (!fs.existsSync(filePath)) { console.log(`⚠️  Not found: ${filePath}`); continue; }
    let c = fs.readFileSync(filePath, 'utf-8');
    c = injectFonts(c);
    c = fixNavbar(c, headerBlock);
    fs.writeFileSync(filePath, c, 'utf-8');
    console.log(`✅ Navbar + fonts fixed: ${page}`);
}

console.log('\n🎉 All branding fixes applied!');
