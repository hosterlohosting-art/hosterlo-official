const fs = require('fs');
const path = require('path');

function extractPremiumBlocks() {
    const content = fs.readFileSync('index.html', 'utf-8');
    
    // Extract header block
    let headerStart = content.indexOf('<!-- TopNavBar -->');
    let headerEnd = content.indexOf('<!-- Hero Section -->');
    
    if (headerStart === -1 || headerEnd === -1) {
        headerStart = content.indexOf('<header');
        headerEnd = content.indexOf('</header>') + '</header>'.length;
    }
    
    const headerBlock = content.substring(headerStart, headerEnd).trim();
    
    // Extract footer block
    let footerStart = content.indexOf('<!-- Footer: Standardized White Background, Black Text -->');
    let footerEnd = content.indexOf('</footer>') + '</footer>'.length;
    
    if (footerStart === -1 || footerEnd === -1) {
        footerStart = content.indexOf('<footer');
        footerEnd = content.indexOf('</footer>') + '</footer>'.length;
    }
    
    const footerBlock = content.substring(footerStart, footerEnd).trim();
    
    return { headerBlock, footerBlock };
}

function findOverlayEnd(content, startIndex) {
    let depth = 0;
    let index = startIndex;
    
    // Find the first opening <div of the overlay
    const overlayDivStart = content.indexOf('<div', startIndex);
    if (overlayDivStart === -1) return -1;
    
    index = overlayDivStart;
    
    while (index < content.length) {
        if (content.substring(index, index + 4) === '<div') {
            depth++;
            index += 4;
        } else if (content.substring(index, index + 6) === '</div>') {
            depth--;
            index += 6;
            if (depth === 0) {
                return index; // Found the matching closing tag!
            }
        } else {
            index++;
        }
    }
    return -1;
}

function syncSubpage(filePath, headerBlock, footerBlock) {
    let content = fs.readFileSync(filePath, 'utf-8');
    
    // Replace header
    const subHeaderStart = content.indexOf('<header');
    let subHeaderEnd = content.indexOf('</header>') + '</header>'.length;
    
    // Check if there is a mobile menu overlay block inside or near the header segment
    const subOverlayStart = content.indexOf('<!-- Mobile Menu Overlay -->');
    if (subOverlayStart !== -1) {
        const overlayEnd = findOverlayEnd(content, subOverlayStart);
        if (overlayEnd !== -1) {
            subHeaderEnd = overlayEnd;
        }
    }
    
    if (subHeaderStart !== -1 && subHeaderEnd !== -1) {
        content = content.substring(0, subHeaderStart) + headerBlock + "\n" + content.substring(subHeaderEnd);
    }
    
    // Replace footer
    const subFooterStart = content.indexOf('<footer');
    const subFooterEnd = content.indexOf('</footer>') + '</footer>'.length;
    
    if (subFooterStart !== -1 && subFooterEnd !== -1) {
        content = content.substring(0, subFooterStart) + footerBlock + "\n" + content.substring(subFooterEnd);
    }
    
    // Standardize maximum layout widths
    content = content.replace(/max-w-\[1280px\]/g, 'max-w-[1440px]');
    content = content.replace(/"container-max": "1280px"/g, '"container-max": "1440px"');
    
    // Align head links & fonts (Lexend/Inter -> Outfit/Plus Jakarta Sans)
    const oldFontLinkRegex = /https:\/\/fonts\.googleapis\.com\/css2\?family=(?:Lexend|Inter)[^"']+/g;
    const newFontLink = 'https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap';
    
    content = content.replace(oldFontLinkRegex, newFontLink);
    
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

function walkDir(dir, headerBlock, footerBlock) {
    console.log(`Walking directory: ${dir}`);
    try {
        const list = fs.readdirSync(dir);
        list.forEach(file => {
            const filePath = path.join(dir, file);
            try {
                const stat = fs.statSync(filePath);
                if (stat.isDirectory()) {
                    if (file !== '.git' && file !== 'node_modules' && file !== 'assets' && file !== '.system_generated' && file !== 'scratch') {
                        console.log(` -> Subdirectory found: ${file}`);
                        walkDir(filePath, headerBlock, footerBlock);
                    }
                } else if (file.endsWith('.html') && filePath !== path.join(process.cwd(), 'index.html') && !filePath.includes('node_modules')) {
                    console.log(` -> HTML File found: ${file} at ${filePath}`);
                    syncSubpage(filePath, headerBlock, footerBlock);
                }
            } catch (e) {
                console.error(`Error statting ${filePath}: ${e.message}`);
            }
        });
    } catch (err) {
        console.error(`Error reading directory ${dir}: ${err.message}`);
    }
}

function main() {
    const { headerBlock, footerBlock } = extractPremiumBlocks();
    console.log("Extracted premium header and footer blocks successfully!");
    
    walkDir(process.cwd(), headerBlock, footerBlock);
    console.log("\nCompleted! Fully synchronized branding across subpages.");
}

main();
