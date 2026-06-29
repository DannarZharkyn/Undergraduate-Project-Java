# Somni Systems Website

A calm, responsive landing page for Somni Systems with a private Google Sheets waitlist integration.

## Local development

The waitlist uses a Vercel serverless API route, so run the site with Vercel rather than opening `index.html` directly:

```bash
npm install
cp .env.example .env.local
npm run preview
```

Real `.env` files, spreadsheets, and CSV exports are ignored by Git. Never place customer data in this repository.

## Google Sheets setup

1. Create a Google Sheet and name one tab `Waitlist`.
2. Add the headings `Submitted at`, `First name`, and `Email` to cells A1–C1.
3. In Google Cloud, create or select a project and enable the Google Sheets API.
4. Create a service account and generate a JSON key.
5. Share the Google Sheet with the service account's `client_email` as an **Editor**.
6. Copy `.env.example` to `.env.local` and add the service account email, private key, spreadsheet ID, and tab name.

The spreadsheet ID is the value between `/d/` and `/edit` in the Google Sheet URL. Preserve the `\n` characters in the private key environment variable.

## Deployment

GitHub Pages can host the static design, but it cannot run `/api/waitlist`. Deploy this directory to Vercel so the secure API route and the page share the same domain.

In the Vercel project settings, add these environment variables:

```text
GOOGLE_SHEETS_CLIENT_EMAIL
GOOGLE_SHEETS_PRIVATE_KEY
GOOGLE_SHEETS_SPREADSHEET_ID
GOOGLE_SHEETS_TAB_NAME
```

Redeploy after saving the variables. The API appends timestamp, first name, and email to columns A–C of the configured tab.

## Main files

- `index.html` — landing-page content and accessible waitlist modal
- `styles.css` — responsive visual design
- `script.js` — modal, validation, and submission behavior
- `api/waitlist.js` — server-side Google Sheets submission route
- `assets/somni-hero.svg` — lightweight hero illustration
- `.env.example` — safe environment-variable template
- `vercel.json` — deployment and security-header configuration
