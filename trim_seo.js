const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();

// Trimmed descriptions — all under 160 chars
const FIXES = {
  'index.html': {
    desc: 'Launch your website with Hosterlo — cloud hosting with a free .com domain, business email, SSL, and 18 months of Gemini Pro. From $4.08/mo.',
    title: null,
  },
  'about-hosterlo/index.html': {
    desc: 'Hosterlo helps businesses launch fast, secure websites with enterprise-grade cloud infrastructure and expert 24/7 human support.',
    title: null,
  },
  'hosting/shared-hosting/index.html': {
    desc: 'Affordable shared hosting with LiteSpeed speed, free SSL, daily backups and cPanel. Perfect for blogs and small business sites.',
    title: null,
  },
  'hosting/wordpress-hosting/index.html': {
    desc: 'WordPress hosting engineered for speed — LiteSpeed cache, auto-updates, WP-CLI, free SSL and one-click install. Launch your site today.',
    title: null,
  },
  'domains/index.html': {
    desc: 'Register your perfect domain with Hosterlo. Hundreds of TLDs including .com, .net, .org with free DNS management and WHOIS privacy.',
    title: null,
  },
  'free-offer/index.html': {
    desc: 'Every Hosterlo annual plan includes a free .com domain, business email, SSL, and 18 months of Gemini Pro. Claim your free growth kit.',
    title: 'Free Hosting Growth Kit | Free Domain, Email &amp; Gemini Pro',
  },
  'ai-article-writer/index.html': {
    desc: 'Generate SEO-optimised articles instantly with Hosterlo\'s free AI writer. Perfect for bloggers and marketers who want great content fast.',
    title: null,
  },
  'blog/index.html': {
    desc: 'Expert articles on web hosting, WordPress, domains, SEO and digital marketing from the Hosterlo team. Learn how to grow your online presence.',
    title: null,
  },
  'infrastructure/index.html': {
    desc: 'Hosterlo runs on elite global data centers with 99.99% uptime, NVMe SSD, DDoS protection and enterprise-grade network redundancy.',
    title: null,
  },
  'dmarc-record-lookup/index.html': {
    desc: 'Check your domain\'s DMARC record instantly. Identify email security gaps and protect your brand from phishing with our free lookup tool.',
    title: null,
  },
  'digioverse/index.html': {
    desc: 'Digioverse is the enterprise cloud infrastructure powering Hosterlo — delivering speed, security and uptime at a global scale.',
    title: null,
  },
  'refund-policy/index.html': {
    desc: 'Hosterlo offers a 30-day money-back guarantee on all hosting plans. Learn your rights, eligibility and how to request a refund.',
    title: null,
  },
  'support/index.html': {
    desc: 'Expert help for hosting setup, domains, SSL, billing, migrations and WordPress — available 24/7 from the Hosterlo support team.',
    title: null,
  },
  'terms-conditions/index.html': {
    desc: 'Hosterlo\'s terms cover acceptable use, SLA, payments, refund rights and account responsibilities. Read before purchasing any plan.',
    title: null,
  },
};

function setMeta(content, name, value, attr = 'name') {
  const re = new RegExp(`<meta\\s+${attr}="${name}"\\s+content="[^"]*"\\s*/?>`, 'i');
  const re2 = new RegExp(`<meta\\s+content="[^"]*"\\s+${attr}="${name}"\\s*/?>`, 'i');
  const tag = `<meta ${attr}="${name}" content="${value}">`;
  if (re.test(content)) return content.replace(re, tag);
  if (re2.test(content)) return content.replace(re2, tag);
  return content.replace('</head>', `    ${tag}\n</head>`);
}

for (const [relPath, fix] of Object.entries(FIXES)) {
  const filePath = path.join(ROOT, relPath.replace(/\//g, path.sep));
  if (!fs.existsSync(filePath)) { console.log(`⚠️  Not found: ${relPath}`); continue; }

  let c = fs.readFileSync(filePath, 'utf-8');

  if (fix.desc) c = setMeta(c, 'description', fix.desc);
  if (fix.title) c = c.replace(/<title>[^<]*<\/title>/i, `<title>${fix.title}</title>`);

  fs.writeFileSync(filePath, c, 'utf-8');
  console.log(`✅ Trimmed: ${relPath} (desc: ${fix.desc ? fix.desc.length : '-'} chars)`);
}

console.log('\n🎉 All description lengths fixed!');
