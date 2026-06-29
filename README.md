# Somni Systems Website

A calm, responsive landing page for Somni Systems with a private Google Sheets waitlist integration powered by Google Apps Script.

## Local development

The waitlist uses a Vercel serverless API route, so run the site with Vercel rather than opening `index.html` directly:

```bash
cp .env.example .env.local
npx vercel dev
```

Real `.env` files, spreadsheets, and CSV exports are ignored by Git. Never place customer data in this repository.

## Google Sheets and Apps Script setup

1. Create a Google Sheet and name one tab `Waitlist`.
2. Add the headings `Submitted at`, `First name`, and `Email` to cells A1–C1.
3. Open **Extensions → Apps Script** and add the waitlist `doPost` handler.
4. Add a private `WAITLIST_SECRET` under **Project Settings → Script Properties**.
5. Deploy the script as a web app that executes as the owner and is accessible to anyone.
6. Copy `.env.example` to `.env.local`, set the `/exec` deployment URL, and use the same secret value.

## Deployment

GitHub Pages can host the static design, but it cannot run `/api/waitlist`. Deploy this directory to Vercel so the secure API route and the page share the same domain.

In the Vercel project settings, add these environment variables:

```text
APPS_SCRIPT_URL
APPS_SCRIPT_SECRET
```

Redeploy after saving the variables. The Vercel API validates each submission and forwards it securely to Apps Script, which appends timestamp, first name, and email to the `Waitlist` tab.

## Main files

- `index.html` — landing-page content and accessible waitlist modal
- `styles.css` — responsive visual design
- `script.js` — modal, validation, and submission behavior
- `api/waitlist.js` — server-side Google Sheets submission route
- `assets/somni-hero.svg` — lightweight hero illustration
- `.env.example` — safe environment-variable template
- `vercel.json` — deployment and security-header configuration
