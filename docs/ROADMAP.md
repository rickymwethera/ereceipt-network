# Roadmap: v1 receipt inbox

Goal: a pilot with 3–5 real businesses (ideally via one accountant), then the first
paying customer at KSh 1,000–1,500 a month per business.

Each step is a GitHub issue labelled `v1`. Do them roughly in order, one PR each.

| # | Step | Done when |
|---|---|---|
| 1 | Local setup and first deploy | App runs locally on Postgres, and an empty app is live on Render/Railway with `/admin` working. |
| 2 | Collect real receipt samples | 20+ real eTIMS receipts photographed; QR contents and the KRA checker page (valid, invalid, no buyer PIN) saved under `tests/fixtures/`. |
| 3 | Core data model | `Business`, `Membership` (owner / staff / accountant), `Receipt` with statuses; duplicates blocked per business; visible in admin. |
| 4 | QR decoding | `decode_receipt_qr(image) -> invoice number + URL`, tested on the fixture photos; clear error when no QR is found. |
| 5 | KRA verification | `verify_invoice(invoice_number) -> KraResult` parses supplier PIN, buyer PIN, date, total; caches results; tested on saved pages. |
| 6 | Background jobs | Pick django-q2 or Procrastinate; decoding + verification run as a job after a receipt arrives, with retries. |
| 7 | Web upload | Logged-in staff can upload a photo (camera on phone) or type an invoice number, and see the result. |
| 8 | Monthly list | Owner / accountant sees a month's receipts with totals, and flagged receipts clearly marked. |
| 9 | Spreadsheet export | One-click xlsx (and CSV) of valid expenses for the month, columns agreed with a real accountant. |
| 10 | WhatsApp intake | Webhook verified and signature-checked; sender phone mapped to a staff member; photo or text handled; reply with the result. |
| 11 | Accountant view | An accountant can switch between their client businesses and export for each. |
| 12 | Pilot hardening | Sentry, database backups, rate limits, privacy policy, ODPC registration. Pilot starts here. |
| 13 | M-Pesa billing | Subscription per business, Daraja STK Push (or Ratiba), payment callback, grace period. |

## Later (not v1)

- OCR fallback for receipts with damaged QR codes
- Email forwarding as a third intake channel
- Expense categories and accounting-software export (QuickBooks, Zoho, etc.)
- Aggregate stats on which merchants and POS systems receipts come from, to pick
  network partners
