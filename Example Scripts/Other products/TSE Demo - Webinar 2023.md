TSE Demo

Developer Playground & Sage Demo

Sage Search
WS: Grocery Sales
Recap/Overview
What were the best selling bakery items for young customers?
Advanced Keywords
Growth - show me month over month growth of pharmacy sales last year?
%, formula - What is the percentage of sales for each state?

I’m the technical product marketing manager for ThoughtSpot, I’m based in Vancouver canada.

















OLD SCRIPT





Playground:


Embedded Natural Language Search
Click on Developer Tab
Select Feature to Embed: Natural Language Search
Select Datasource: Healthcare Denial Management
User Customizations:
Disable changing worksheet
Hide worksheet selector
Apply Custom styles
Deleted customizations section (line 18 - 42) (above style section)
Insert:
customizations: {
content: {
strings: {'Ask Sage any data question': 'Ask any question about MDAudit'
}
},
style: {
customCSSUrl: "https://cdn.jsdelivr.net/gh/thoughtspot/custom-css-demo/css-variables.css", // location of your style sheet

// To apply overrides for your style sheet in this init, provide variable values below, eg
customCSS: {
variables: {
"--ts-var-button--secondary-background": "#E5F4EF",
"--ts-var-button--secondary--hover-background": "#9AD3BF",
"--ts-var-root-background": "#F7F5FF",
"--ts-var-sage-bar-header-background-color" : "#049160",
"--ts-var-source-selector-background-color": "white",
"--ts-var-sage-search-box-font-color": "#1C2330",
"--ts-var-sage-search-box-background-color": "white",
"--ts-var-sage-embed-background-color": "white",
"--ts-var-sage-seed-questions-background": "white",
"--ts-var-sage-seed-questions-font-color": "#2770ef",
"--ts-var-sage-seed-questions-hover-background": "rd-color('gray', 'tint-5')",
"--ts-var-sage-bar-img-url" : "url(/resources/img/sage-homepage-search.svg)",
"--ts-var-sage-bar-img-color" : "#f2f3f5",
"--ts-var-sage-bar-img-visibility" : "hidden",
},
},
},
},

