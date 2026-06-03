const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const TODAY = '2026-06-03';

// ─── SEO Data per page ────────────────────────────────────────────────────────
const SEO = {
  'index.html': {
    title: 'Hosterlo | Cloud Hosting, Free Domain, Email &amp; Gemini Pro',
    desc: 'Launch your website with Hosterlo — premium cloud hosting with a free .com domain, free business email, free SSL, and Gemini Pro included for 18 months. Just $59/year.',
    ogTitle: 'Hosterlo | Cloud Hosting, Free Domain, Email &amp; Gemini Pro',
    ogDesc: 'Premium hosting bundle — free .com domain, business email, SSL, and 18 months of Gemini Pro. Everything your business needs, starting at $59/year.',
    keywords: 'cloud hosting, web hosting, free domain, business email hosting, Gemini Pro hosting, cheap hosting, hosterlo, wordpress hosting',
  },
  'about-hosterlo/index.html': {
    title: 'About Hosterlo | Cloud Hosting Company &amp; Infrastructure Team',
    desc: 'Meet Hosterlo — a cloud hosting company built to help businesses launch fast, secure, and reliable websites with enterprise-grade infrastructure and expert 24/7 support.',
    ogTitle: 'About Hosterlo | Cloud Hosting Company &amp; Infrastructure Team',
    ogDesc: 'Hosterlo is a cloud hosting company built for speed, security and reliability. Meet our team and discover our global infrastructure.',
    keywords: 'about hosterlo, hosting company, cloud infrastructure, web hosting team, hosterlo company',
  },
  'hosting/index.html': {
    title: 'Web Hosting Plans | Fast Cloud Hosting by Hosterlo',
    desc: 'Explore Hosterlo\'s cloud hosting plans with LiteSpeed servers, NVMe SSD storage, free SSL, cPanel, and 99.9% uptime. Plans starting from just $59/year.',
    ogTitle: 'Web Hosting Plans | Fast Cloud Hosting by Hosterlo',
    ogDesc: 'High-performance cloud hosting with LiteSpeed, NVMe SSD, free SSL, and cPanel. Start your website today with Hosterlo.',
    keywords: 'web hosting, cloud hosting, litespeed hosting, cpanel hosting, nvme ssd hosting, cheap hosting plans',
  },
  'hosting/shared-hosting/index.html': {
    title: 'Shared Hosting | Affordable Fast Hosting Plans by Hosterlo',
    desc: 'Hosterlo\'s shared hosting plans deliver LiteSpeed speed, free SSL, daily backups, and cPanel at the most affordable price. Perfect for blogs and small business sites.',
    ogTitle: 'Shared Hosting | Affordable Fast Hosting by Hosterlo',
    ogDesc: 'Affordable shared hosting with LiteSpeed, free SSL, cPanel and daily backups. Get started with Hosterlo today.',
    keywords: 'shared hosting, affordable hosting, cheap hosting, litespeed shared hosting, cpanel hosting',
  },
  'hosting/wordpress-hosting/index.html': {
    title: 'WordPress Hosting | Optimised WP Hosting by Hosterlo',
    desc: 'Hosterlo\'s WordPress hosting is engineered for speed — LiteSpeed cache, automatic updates, WP-CLI, free SSL, and one-click install. Launch your WordPress site today.',
    ogTitle: 'WordPress Hosting | Optimised WP Hosting by Hosterlo',
    ogDesc: 'Fully optimised WordPress hosting with LiteSpeed cache, automatic updates, free SSL and expert support. Start your WP site with Hosterlo.',
    keywords: 'wordpress hosting, managed wordpress, litespeed wordpress, wp hosting, wordpress ssl, wordpress cpanel',
  },
  'domains/index.html': {
    title: 'Domain Names | Register, Transfer &amp; Manage Domains | Hosterlo',
    desc: 'Search and register your perfect domain name with Hosterlo. Get .com, .net, .org and hundreds more TLDs with free DNS management, privacy protection and easy transfers.',
    ogTitle: 'Domain Names | Register &amp; Transfer Domains | Hosterlo',
    ogDesc: 'Find and register your domain name with Hosterlo. Hundreds of TLDs available with free DNS management and WHOIS privacy protection.',
    keywords: 'domain names, register domain, buy domain, domain transfer, cheap domain, .com domain, domain search',
  },
  'contact-us/index.html': {
    title: 'Contact Hosterlo | 24/7 Hosting &amp; Domain Support',
    desc: 'Get in touch with the Hosterlo support team — available 24/7 for hosting questions, domain transfers, billing help, and technical assistance. We respond fast.',
    ogTitle: 'Contact Hosterlo | 24/7 Hosting &amp; Domain Support',
    ogDesc: 'Need help? Contact Hosterlo\'s expert support team 24/7 for hosting, domains, billing or technical issues. Fast, friendly and reliable.',
    keywords: 'contact hosterlo, hosting support, domain support, billing support, web hosting help',
  },
  'free-offer/index.html': {
    title: 'Free Hosting Growth Kit | Free Domain, Email &amp; Gemini Pro | Hosterlo',
    desc: 'Claim your free growth kit with every Hosterlo annual plan — includes a free .com domain, free business email setup, free SSL certificate, and 18 months of Gemini Pro.',
    ogTitle: 'Free Hosting Growth Kit | Free Domain, Email &amp; Gemini Pro',
    ogDesc: 'Every Hosterlo annual plan includes a free .com domain, business email, SSL, and 18 months of Gemini Pro. Claim your free growth kit today.',
    keywords: 'free domain hosting, free business email, free ssl, gemini pro free, hosting free offer, hosterlo free',
  },
  'ai-article-writer/index.html': {
    title: 'Free AI Article Writer | SEO Content Generator by Hosterlo',
    desc: 'Generate SEO-optimised blog posts and articles instantly with Hosterlo\'s free AI article writer. Perfect for bloggers, marketers and website owners who want great content fast.',
    ogTitle: 'Free AI Article Writer | SEO Content Generator by Hosterlo',
    ogDesc: 'Write SEO-ready blog posts instantly with Hosterlo\'s free AI article writer tool. No sign-up needed — start generating content right now.',
    keywords: 'free ai article writer, seo content generator, ai blog writer, free content tool, ai writing tool hosterlo',
  },
  'blog/index.html': {
    title: 'Hosterlo Blog | Web Hosting Tips, Domain Guides &amp; SEO Insights',
    desc: 'Read expert articles on web hosting, WordPress, domains, SEO and digital marketing from the Hosterlo team. Learn how to build, grow and secure your online presence.',
    ogTitle: 'Hosterlo Blog | Hosting Tips, Domain Guides &amp; SEO Insights',
    ogDesc: 'Expert guides on web hosting, WordPress, domains, and digital growth from the Hosterlo team. Read, learn and level up your online presence.',
    keywords: 'web hosting blog, domain guides, seo tips, wordpress hosting tips, hosterlo blog, website tips',
  },
  'services/index.html': {
    title: 'Web Design &amp; SEO Services | Hosterlo Professional Services',
    desc: 'Hosterlo offers professional web design, SEO, and digital marketing services to help businesses build a strong online presence and grow organic traffic.',
    ogTitle: 'Web Design &amp; SEO Services | Hosterlo Professional Services',
    ogDesc: 'Professional web design, SEO, and digital marketing by Hosterlo. Build your online presence with expert support.',
    keywords: 'web design services, seo services, digital marketing, website design, hosterlo services',
  },
  'infrastructure/index.html': {
    title: 'Global Data Centers &amp; Infrastructure | Hosterlo Network',
    desc: 'Hosterlo runs on elite global data centers with 99.99% uptime, NVMe SSD storage, DDoS protection, and enterprise-grade network redundancy across multiple continents.',
    ogTitle: 'Global Data Centers &amp; Network Infrastructure | Hosterlo',
    ogDesc: 'Hosterlo\'s global infrastructure delivers 99.99% uptime with elite data centers, NVMe SSD, DDoS protection and enterprise redundancy.',
    keywords: 'data centers, hosting infrastructure, global network, ddos protection, nvme hosting, 99.9 uptime hosting',
  },
  'dmarc-record-lookup/index.html': {
    title: 'Free DMARC Record Lookup | Check Domain Email Security | Hosterlo',
    desc: 'Use Hosterlo\'s free DMARC record lookup tool to instantly check your domain\'s DMARC policy, identify email security gaps and protect your brand from phishing attacks.',
    ogTitle: 'Free DMARC Record Lookup Tool | Hosterlo',
    ogDesc: 'Check your domain\'s DMARC record instantly with our free lookup tool. Identify email security gaps and protect against phishing and spoofing.',
    keywords: 'dmarc lookup, dmarc record check, email security tool, domain dmarc, free dmarc checker',
  },
  'spf-record-lookup/index.html': {
    title: 'Free SPF Record Lookup | Check Domain Email DNS | Hosterlo',
    desc: 'Verify your domain\'s SPF record with Hosterlo\'s free SPF lookup tool. Instantly check email DNS settings, diagnose delivery issues and prevent email spoofing.',
    ogTitle: 'Free SPF Record Lookup Tool | Hosterlo',
    ogDesc: 'Check your domain\'s SPF record instantly with our free tool. Diagnose email delivery issues and prevent spoofing with a single lookup.',
    keywords: 'spf record lookup, spf check, email dns check, domain spf, free spf checker, email deliverability',
  },
  'free-tools/index.html': {
    title: 'Free Web &amp; Domain Tools | DNS, SEO &amp; Email Tools | Hosterlo',
    desc: 'Explore Hosterlo\'s suite of free tools — DMARC lookup, SPF checker, AI article writer, and more. Free tools for website owners, developers and marketers.',
    ogTitle: 'Free Web &amp; Domain Tools | Hosterlo',
    ogDesc: 'DMARC lookup, SPF checker, AI writer and more — completely free tools from Hosterlo for website owners, developers and digital marketers.',
    keywords: 'free web tools, dns tools, dmarc lookup, spf checker, seo tools, free domain tools, hosterlo tools',
  },
  'support/index.html': {
    title: 'Hosterlo Support Centre | 24/7 Help for Hosting &amp; Domains',
    desc: 'Get fast, expert help from the Hosterlo support centre. Browse guides for hosting setup, domain management, SSL, billing, migrations and WordPress troubleshooting.',
    ogTitle: 'Hosterlo Support Centre | 24/7 Hosting &amp; Domain Help',
    ogDesc: 'Expert help for hosting, domains, SSL, billing and WordPress — 24/7 from the Hosterlo support team.',
    keywords: 'hosterlo support, hosting help, domain support, ssl support, wordpress help, billing support',
  },
  'privacy-policy/index.html': {
    title: 'Privacy Policy | Hosterlo Data &amp; Cookie Policy',
    desc: 'Read Hosterlo\'s privacy policy to understand how we collect, use and protect your personal data, cookies and account information in line with GDPR requirements.',
    ogTitle: 'Privacy Policy | Hosterlo',
    ogDesc: 'Hosterlo\'s privacy policy explains how we handle your personal data, cookies and account information. Read our full GDPR-compliant policy.',
    keywords: 'hosterlo privacy policy, data protection, gdpr, cookie policy, personal data',
  },
  'terms-conditions/index.html': {
    title: 'Terms &amp; Conditions | Hosterlo Service Agreement',
    desc: 'Review Hosterlo\'s full terms and conditions including acceptable use policy, service level agreements, payment terms, refund rights and account responsibilities.',
    ogTitle: 'Terms &amp; Conditions | Hosterlo Service Agreement',
    ogDesc: 'Hosterlo\'s terms and conditions cover acceptable use, SLA, payments, refunds and account responsibilities. Read before purchasing.',
    keywords: 'hosterlo terms, terms and conditions, service agreement, hosting terms, acceptable use policy',
  },
  'refund-policy/index.html': {
    title: '30-Day Money Back Guarantee | Hosterlo Refund Policy',
    desc: 'Hosterlo offers a 30-day money-back guarantee on all hosting plans. Read our full refund policy to understand your rights, eligibility and how to request a refund.',
    ogTitle: '30-Day Money Back Guarantee | Hosterlo Refund Policy',
    ogDesc: 'Hosterlo\'s 30-day money-back guarantee gives you confidence to try our hosting. Learn how to request a refund and what\'s covered.',
    keywords: 'hosterlo refund policy, money back guarantee, hosting refund, 30 day refund, hosting cancellation',
  },
  'legal/index.html': {
    title: 'Legal Notices &amp; Policies | Hosterlo',
    desc: 'View all Hosterlo legal notices, policies and compliance documents including privacy policy, terms of service, cookie policy and acceptable use policy.',
    ogTitle: 'Legal Notices &amp; Policies | Hosterlo',
    ogDesc: 'All Hosterlo legal documents in one place — privacy policy, terms of service, cookie policy and acceptable use guidelines.',
    keywords: 'hosterlo legal, terms of service, privacy policy, legal notices, compliance',
  },
  'login/index.html': {
    title: 'Client Login | Hosterlo Hosting Portal',
    desc: 'Log in to your Hosterlo client portal to manage your hosting plans, domains, billing, SSL certificates, email accounts and support tickets securely.',
    ogTitle: 'Client Login | Hosterlo Hosting Portal',
    ogDesc: 'Access your Hosterlo client portal to manage hosting, domains, billing and support. Secure login for existing customers.',
    keywords: 'hosterlo login, client portal, hosting login, billing login, domain management',
  },
  'digioverse/index.html': {
    title: 'Digioverse | Cloud Infrastructure Partner of Hosterlo',
    desc: 'Digioverse is the enterprise cloud infrastructure powering Hosterlo. Learn how our parent infrastructure delivers the speed, security and uptime that Hosterlo customers rely on.',
    ogTitle: 'Digioverse | Cloud Infrastructure Behind Hosterlo',
    ogDesc: 'Digioverse powers Hosterlo\'s global hosting infrastructure with enterprise-grade cloud, network and security technology.',
    keywords: 'digioverse, hosterlo infrastructure, cloud infrastructure company, enterprise hosting infrastructure',
  },
};

// ─── Helper: replace/inject meta tag ─────────────────────────────────────────
function setMeta(content, name, value, attr = 'name') {
  // Try to replace existing
  const re = new RegExp(`<meta\\s+${attr}="${name}"\\s+content="[^"]*"\\s*/?>`, 'i');
  const re2 = new RegExp(`<meta\\s+content="[^"]*"\\s+${attr}="${name}"\\s*/?>`, 'i');
  const tag = `<meta ${attr}="${name}" content="${value}">`;

  if (re.test(content)) return content.replace(re, tag);
  if (re2.test(content)) return content.replace(re2, tag);
  // Inject before </head>
  return content.replace('</head>', `    ${tag}\n</head>`);
}

function setTitle(content, title) {
  return content.replace(/<title>[^<]*<\/title>/i, `<title>${title}</title>`);
}

function setKeywords(content, keywords) {
  if (content.includes('name="keywords"')) {
    return content.replace(/<meta\s+name="keywords"\s+content="[^"]*"\s*\/?>/i, `<meta name="keywords" content="${keywords}">`);
  }
  return content.replace('</head>', `    <meta name="keywords" content="${keywords}">\n</head>`);
}

// ─── Apply SEO to all pages ───────────────────────────────────────────────────
for (const [relPath, seo] of Object.entries(SEO)) {
  const filePath = path.join(ROOT, relPath.replace(/\//g, path.sep));
  if (!fs.existsSync(filePath)) { console.log(`⚠️  Not found: ${relPath}`); continue; }

  let c = fs.readFileSync(filePath, 'utf-8');

  // Title
  c = setTitle(c, seo.title);

  // Meta description
  c = setMeta(c, 'description', seo.desc);

  // OG tags
  c = setMeta(c, 'og:title', seo.ogTitle, 'property');
  c = setMeta(c, 'og:description', seo.ogDesc, 'property');

  // Twitter tags
  c = setMeta(c, 'twitter:title', seo.ogTitle);
  c = setMeta(c, 'twitter:description', seo.ogDesc);

  // Keywords
  c = setKeywords(c, seo.keywords);

  // dateModified in JSON-LD
  c = c.replace(/"dateModified":"[^"]+"/g, `"dateModified":"${TODAY}"`);

  fs.writeFileSync(filePath, c, 'utf-8');
  console.log(`✅ SEO updated: ${relPath}`);
}

// ─── Update sitemap lastmod dates ─────────────────────────────────────────────
for (const sitemapFile of ['sitemap.xml', 'page-sitemap.xml']) {
  const sitemapPath = path.join(ROOT, sitemapFile);
  if (!fs.existsSync(sitemapPath)) continue;
  let s = fs.readFileSync(sitemapPath, 'utf-8');
  s = s.replace(/<lastmod>[^<]+<\/lastmod>/g, `<lastmod>${TODAY}</lastmod>`);
  fs.writeFileSync(sitemapPath, s, 'utf-8');
  console.log(`✅ Sitemap updated: ${sitemapFile}`);
}

console.log('\n🎉 All SEO updates applied!');
