const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const results = [];

function walk(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const full = path.join(dir, item);
        if (['.git','node_modules','assets','.system_generated'].includes(item)) continue;
        const stat = fs.statSync(full);
        if (stat.isDirectory()) walk(full);
        else if (item === 'index.html') results.push(full);
    }
}

walk(ROOT);

const report = [];

for (const file of results) {
    const rel = path.relative(ROOT, file);
    const c = fs.readFileSync(file, 'utf-8');

    const issues = [];

    // --- BRANDING ---
    if (!c.includes('Outfit')) issues.push('❌ Missing Outfit font');
    if (!c.includes('Plus Jakarta Sans')) issues.push('❌ Missing Plus Jakarta Sans font');
    if (!c.includes('TopNavBar') && !c.includes('sticky top-4')) issues.push('❌ Missing floating navbar');
    if (!c.includes('hosterlo') || !c.includes('watermark') && !c.includes('opacity-[0.06]')) issues.push('⚠️  Possible missing watermark footer');
    if (!c.includes('/assets/logo.png')) issues.push('❌ Missing logo');

    // --- SEO ---
    const titleMatch = c.match(/<title>(.*?)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '';
    if (!title) issues.push('❌ Missing <title>');
    else if (title.length < 30) issues.push(`⚠️  Title too short (${title.length} chars): "${title}"`);
    else if (title.length > 70) issues.push(`⚠️  Title too long (${title.length} chars)`);

    const descMatch = c.match(/<meta\s+name="description"\s+content="([^"]+)"/i) ||
                      c.match(/<meta\s+content="([^"]+)"\s+name="description"/i);
    const desc = descMatch ? descMatch[1].trim() : '';
    if (!desc) issues.push('❌ Missing meta description');
    else if (desc.length < 100) issues.push(`⚠️  Meta description too short (${desc.length} chars)`);
    else if (desc.length > 160) issues.push(`⚠️  Meta description too long (${desc.length} chars)`);

    if (!c.includes('og:title')) issues.push('❌ Missing og:title');
    if (!c.includes('og:description')) issues.push('❌ Missing og:description');
    if (!c.includes('og:image')) issues.push('❌ Missing og:image');
    if (!c.includes('og:url')) issues.push('❌ Missing og:url');
    if (!c.includes('twitter:card')) issues.push('❌ Missing twitter:card');
    if (!c.includes('rel="canonical"')) issues.push('❌ Missing canonical link');
    if (!c.includes('application/ld+json')) issues.push('❌ Missing JSON-LD structured data');

    // H1 check
    const h1Matches = c.match(/<h1[\s>]/gi) || [];
    if (h1Matches.length === 0) issues.push('❌ Missing H1 tag');
    else if (h1Matches.length > 1) issues.push(`⚠️  Multiple H1 tags (${h1Matches.length})`);

    // Robots
    if (!c.includes('name="robots"')) issues.push('⚠️  Missing robots meta');

    report.push({ file: rel, title, issues });
}

console.log('\n======= HOSTERLO SITE AUDIT =======\n');
for (const r of report) {
    if (r.issues.length === 0) {
        console.log(`✅ ${r.file}`);
    } else {
        console.log(`\n📄 ${r.file}`);
        console.log(`   Title: "${r.title}"`);
        for (const i of r.issues) console.log(`   ${i}`);
    }
}

const total = report.length;
const clean = report.filter(r => r.issues.length === 0).length;
console.log(`\n======= SUMMARY: ${clean}/${total} pages fully clean =======\n`);
