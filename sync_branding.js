const fs = require('fs');
const path = require('path');

function findTagBounds(content, tagName, startSearch = 0) {
    const startTag = `<${tagName}`;
    const endTag = `</${tagName}>`;
    
    const startPos = content.indexOf(startTag, startSearch);
    if (startPos === -1) return [-1, -1];
    
    const endPos = content.indexOf(endTag, startPos);
    if (endPos === -1) return [-1, -1];
    
    return [startPos, endPos + endTag.length];
}

function findDivBounds(content, identifier, startSearch = 0) {
    const idPos = content.indexOf(identifier, startSearch);
    if (idPos === -1) return [-1, -1];
    
    // Find the opening <div preceding the identifier
    const startPos = content.lastIndexOf('<div', idPos);
    if (startPos === -1) return [-1, -1];
    
    let depth = 0;
    let index = startPos;
    
    while (index < content.length) {
        if (content.substring(index, index + 4) === '<div') {
            depth++;
            index += 4;
        } else if (content.substring(index, index + 6) === '</div>') {
            depth--;
            index += 6;
            if (depth === 0) {
                return [startPos, index];
            }
        } else {
            index++;
        }
    }
    
    return [-1, -1];
}

function extractPremiumBlocksFromFile(filePath) {
    if (!fs.existsSync(filePath)) {
        throw new Error(`File does not exist: ${filePath}`);
    }
    
    const content = fs.readFileSync(filePath, 'utf-8');
    
    // Find header tag bounds
    const [hStart, hEnd] = findTagBounds(content, 'header');
    if (hStart === -1 || hEnd === -1) {
        throw new Error(`Could not find <header> block in ${filePath}`);
    }
    
    // Find mobile-menu-overlay bounds
    const [oStart, oEnd] = findDivBounds(content, 'id="mobile-menu-overlay"');
    
    let zoneStart = hStart;
    let zoneEnd = hEnd;
    
    if (oStart !== -1 && oEnd !== -1) {
        zoneStart = Math.min(hStart, oStart);
        zoneEnd = Math.max(hEnd, oEnd);
    }
    
    // Backtrack to include preceding "<!-- TopNavBar -->" comment
    const commentPos = content.lastIndexOf('<!-- TopNavBar -->', zoneStart);
    if (commentPos !== -1 && (zoneStart - commentPos) < 100) {
        zoneStart = commentPos;
    }
    
    const headerBlock = content.substring(zoneStart, zoneEnd).trim();
    
    // Find footer bounds
    let [fStart, fEnd] = findTagBounds(content, 'footer');
    if (fStart === -1 || fEnd === -1) {
        throw new Error(`Could not find <footer> block in ${filePath}`);
    }
    
    // Backtrack to include preceding "<!-- Footer" comment
    const footerCommentPos = content.lastIndexOf('<!-- Footer', fStart);
    if (footerCommentPos !== -1 && (fStart - footerCommentPos) < 150) {
        fStart = footerCommentPos;
    }
    
    const footerBlock = content.substring(fStart, fEnd).trim();
    
    return { headerBlock, footerBlock };
}

function syncSubpage(filePath, headerBlock, footerBlock) {
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // Find header bounds
    const [hStart, hEnd] = findTagBounds(content, 'header');
    
    // Find all mobile menu overlays
    const overlays = [];
    let searchPos = 0;
    while (true) {
        const [oStart, oEnd] = findDivBounds(content, 'id="mobile-menu-overlay"', searchPos);
        if (oStart === -1) break;
        overlays.push([oStart, oEnd]);
        searchPos = oEnd;
    }
    
    if (overlays.length === 0) {
        const commentPos = content.indexOf('<!-- Mobile Menu Overlay -->');
        if (commentPos !== -1) {
            const [oStart, oEnd] = findDivBounds(content, 'id="mobile-menu-overlay"', commentPos);
            if (oStart !== -1) {
                overlays.push([oStart, oEnd]);
            }
        }
    }
    
    const starts = [];
    const ends = [];
    
    if (hStart !== -1) {
        starts.push(hStart);
        ends.push(hEnd);
    }
    
    for (const [oStart, oEnd] of overlays) {
        starts.push(oStart);
        ends.push(oEnd);
    }
    
    if (starts.length > 0) {
        let zoneStart = Math.min(...starts);
        const zoneEnd = Math.max(...ends);
        
        // Backtrack to include preceding comments
        const commentPos1 = content.lastIndexOf('<!-- TopNavBar -->', zoneStart);
        if (commentPos1 !== -1 && (zoneStart - commentPos1) < 100) {
            zoneStart = commentPos1;
        }
        
        const commentPos2 = content.lastIndexOf('<!-- Mobile Menu Overlay -->', zoneStart);
        if (commentPos2 !== -1 && (zoneStart - commentPos2) < 100) {
            zoneStart = commentPos2;
        }
        
        content = content.substring(0, zoneStart) + headerBlock + "\n" + content.substring(zoneEnd);
    }
    
    // Replace footer
    let [fStart, fEnd] = findTagBounds(content, 'footer');
    if (fStart !== -1) {
        // Backtrack to include preceding comment
        const footerCommentPos = content.lastIndexOf('<!-- Footer', fStart);
        if (footerCommentPos !== -1 && (fStart - footerCommentPos) < 155) {
            fStart = footerCommentPos;
        }
        
        content = content.substring(0, fStart) + footerBlock + "\n" + content.substring(fEnd);
    }
    
    // Standardize maximum layout widths
    content = content.replace(/max-w-\[1280px\]/g, 'max-w-[1440px]');
    content = content.replace(/"container-max": "1280px"/g, '"container-max": "1440px"');
    
    // Align head links & fonts
    const oldFontLinkRegex = /https:\/\/fonts\.googleapis\.com\/css2\?family=(?:Lexend|Inter)[^"']+/g;
    const newFontLink = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap';
    content = content.replace(oldFontLinkRegex, newFontLink);
    
    const cleanFontLinkRegex = /https:\/\/fonts\.googleapis\.com\/css2\?family=Inter:wght@300;400;500;600;700;800&display=swap/g;
    content = content.replace(cleanFontLinkRegex, newFontLink);

    // Update font config in inline tailwind theme
    if (content.includes('"fontFamily": {')) {
        content = content.replace(/"fontFamily":\s*\{[^}]*\}/g, 
            `"fontFamily": {
                    "h3": ["Outfit", "sans-serif"],
                    "body-sm": ["Plus Jakarta Sans", "sans-serif"],
                    "body-md": ["Plus Jakarta Sans", "sans-serif"],
                    "h1": ["Outfit", "sans-serif"],
                    "body-lg": ["Plus Jakarta Sans", "sans-serif"],
                    "label-caps": ["Plus Jakarta Sans", "sans-serif"],
                    "h2": ["Outfit", "sans-serif"]
            }`
        );
    }

    // Inject premium font styles into the <style> block if not already present
    if (!content.includes('font-family: "Plus Jakarta Sans"')) {
        content = content.replace('<style>', `<style>
        body {
            font-family: "Plus Jakarta Sans", sans-serif !important;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: "Outfit", sans-serif !important;
        }
`);
    }
    
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`Synchronized branding on page: ${filePath}`);
}

function walkDir(dir, usHeader, usFooter, ukHeader, ukFooter, pkHeader, pkFooter) {
    try {
        const list = fs.readdirSync(dir);
        list.forEach(file => {
            const filePath = path.join(dir, file);
            try {
                const stat = fs.statSync(filePath);
                if (stat.isDirectory()) {
                    if (file !== '.git' && file !== 'node_modules' && file !== 'assets' && file !== '.system_generated' && file !== 'scratch') {
                        walkDir(filePath, usHeader, usFooter, ukHeader, ukFooter, pkHeader, pkFooter);
                    }
                } else if (file.endsWith('.html')) {
                    const normPath = path.relative(process.cwd(), filePath);
                    const normPathLower = normPath.toLowerCase();
                    
                    // Skip templates source files
                    if (normPath === 'index.html' || normPath === path.join('uk', 'index.html') || normPath === path.join('pk', 'index.html')) {
                        return;
                    }
                    
                    // Choose market blocks
                    let hBlock = usHeader;
                    let fBlock = usFooter;
                    
                    if (normPathLower.includes(`${path.sep}uk${path.sep}`) || normPathLower.startsWith(`uk${path.sep}`)) {
                        hBlock = ukHeader || usHeader;
                        fBlock = ukFooter || usFooter;
                    } else if (normPathLower.includes(`${path.sep}pk${path.sep}`) || normPathLower.startsWith(`pk${path.sep}`)) {
                        hBlock = pkHeader || usHeader;
                        fBlock = pkFooter || usFooter;
                    }
                    
                    syncSubpage(filePath, hBlock, fBlock);
                }
            } catch (e) {
                console.error(`Error processing ${filePath}: ${e.message}`);
            }
        });
    } catch (err) {
        console.error(`Error reading directory ${dir}: ${err.message}`);
    }
}

function main() {
    console.log("Extracting US premium blocks...");
    const { headerBlock: usHeader, footerBlock: usFooter } = extractPremiumBlocksFromFile('index.html');
    
    let ukHeader = null;
    let ukFooter = null;
    if (fs.existsSync(path.join('uk', 'index.html'))) {
        try {
            const ukBlocks = extractPremiumBlocksFromFile(path.join('uk', 'index.html'));
            ukHeader = ukBlocks.headerBlock;
            ukFooter = ukBlocks.footerBlock;
            console.log("Extracted UK premium blocks.");
        } catch (e) {
            console.warn(`Warning: Could not extract UK blocks: ${e.message}`);
        }
    }
    
    let pkHeader = null;
    let pkFooter = null;
    if (fs.existsSync(path.join('pk', 'index.html'))) {
        try {
            const pkBlocks = extractPremiumBlocksFromFile(path.join('pk', 'index.html'));
            pkHeader = pkBlocks.headerBlock;
            pkFooter = pkBlocks.footerBlock;
            console.log("Extracted PK premium blocks.");
        } catch (e) {
            console.warn(`Warning: Could not extract PK blocks: ${e.message}`);
        }
    }
    
    console.log("Walking and syncing files...");
    walkDir(process.cwd(), usHeader, usFooter, ukHeader, ukFooter, pkHeader, pkFooter);
    console.log("\nCompleted! Fully synchronized branding across subpages.");
}

main();
