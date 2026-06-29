const { google } = require('googleapis');

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

module.exports = async function handler(request, response) {
  if (request.method !== 'POST') {
    response.setHeader('Allow', 'POST');
    return response.status(405).json({ error: 'Method not allowed.' });
  }

  const firstName = typeof request.body?.firstName === 'string' ? request.body.firstName.trim() : '';
  const email = typeof request.body?.email === 'string' ? request.body.email.trim().toLowerCase() : '';
  const honeypot = typeof request.body?.company === 'string' ? request.body.company.trim() : '';

  if (honeypot) return response.status(200).json({ success: true });
  if (!firstName) return response.status(400).json({ error: 'First name is required.' });
  if (!email) return response.status(400).json({ error: 'Email address is required.' });
  if (firstName.length > 80) return response.status(400).json({ error: 'First name is too long.' });
  if (email.length > 254 || !EMAIL_PATTERN.test(email)) {
    return response.status(400).json({ error: 'Please enter a valid email address.' });
  }

  const requiredVariables = [
    'GOOGLE_SHEETS_CLIENT_EMAIL',
    'GOOGLE_SHEETS_PRIVATE_KEY',
    'GOOGLE_SHEETS_SPREADSHEET_ID',
  ];

  if (requiredVariables.some((variable) => !process.env[variable])) {
    return response.status(500).json({ error: 'The waitlist is not configured yet.' });
  }

  try {
    const auth = new google.auth.GoogleAuth({
      credentials: {
        client_email: process.env.GOOGLE_SHEETS_CLIENT_EMAIL,
        private_key: process.env.GOOGLE_SHEETS_PRIVATE_KEY.replace(/\\n/g, '\n'),
      },
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    const sheets = google.sheets({ version: 'v4', auth });
    const tabName = process.env.GOOGLE_SHEETS_TAB_NAME || 'Waitlist';

    await sheets.spreadsheets.values.append({
      spreadsheetId: process.env.GOOGLE_SHEETS_SPREADSHEET_ID,
      range: `'${tabName.replace(/'/g, "''")}'!A:C`,
      valueInputOption: 'RAW',
      insertDataOption: 'INSERT_ROWS',
      requestBody: {
        values: [[new Date().toISOString(), firstName, email]],
      },
    });

    return response.status(200).json({ success: true });
  } catch (error) {
    console.error('Waitlist submission failed:', error?.code || error?.message || 'Unknown error');
    return response.status(500).json({ error: 'We couldn’t add you right now. Please try again.' });
  }
};
