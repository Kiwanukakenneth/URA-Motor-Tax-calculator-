# Uganda Car Import Tax Calculator (URA Standard)

A premium, high-performance car tax estimator for Uganda, powered by the **URA Motor Vehicle Value Guide** database.

## Features
- **Accurate VAT Logic**: Calculates VAT on the landed value (CIF + Import Duty) as per URA standards.
- **Reliability Database**: Includes Uganda-specific reliability ratings and engine breakdowns for popular brands.
- **Liquid Glass UI**: Modern, responsive design with glassmorphism and real-time calculations.
- **Offline Capable**: Standalone HTML/JS architecture.

## External Use & Embedding
To embed this calculator as a widget on your dealership or logistics website, use the following snippet:

```html
<iframe 
  src="YOUR_HOSTED_URL_HERE" 
  width="100%" 
  height="800px" 
  style="border:none; border-radius:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);"
  title="Uganda Car Tax Calculator">
</iframe>
```

## Setup for Development
1. Clone this repository.
2. Open `uganda-car-tax-standalone ultimate.html` in any modern browser.
3. Assets are located in `/Js` and `/Css` folders.

## Data Maintenance
The `Js/script.js` contains the compiled database. For raw data updates, refer to the Python scripts in the root directory (excluded from production via `.gitignore`).

---
*Disclaimer: This tool is for informational purposes. Always verify final figures with a licensed clearing agent or the Uganda Revenue Authority.*
