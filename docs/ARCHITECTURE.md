# Architecture (v1: receipt inbox)

## The flow

```
 Staff phone ──WhatsApp──▶ Meta Cloud API ──webhook──▶ intake ─┐
 Staff phone ──web page (photo or invoice no.)──────▶ intake ─┤
                                                               ▼
                                                    Receipt (status=pending)
                                                               │  background job
                                                               ▼
                                     decode QR ──▶ invoice number + KRA link
                                                               │
                                                               ▼
                                  kra: fetch KRA invoice checker, parse result
                                                               │
                                                               ▼
                Receipt status: valid / invalid / missing buyer PIN / wrong buyer PIN
                                                               │
                         ┌─────────────────────────────────────┴───────────┐
                         ▼                                                 ▼
             reply to staff on WhatsApp                 monthly list + xlsx export
                                                         (owner / accountant)
```

## Stack and why

| Piece | Choice | Why |
|---|---|---|
| Language / framework | Python 3.13, Django 6.1 | Admin, auth, ORM and migrations out of the box; best libraries for QR and spreadsheets. |
| Frontend | Django templates + HTMX | No separate JS app to build and deploy. Mobile-friendly forms are enough for v1. |
| Database | PostgreSQL (Neon or Supabase in production, Docker locally) | Reliable, free tier to start, also serves as the job queue. |
| Background jobs | django-q2 or Procrastinate (Postgres-backed) | No Redis to run or pay for. Decide when you reach roadmap step 6. |
| File storage | Cloudflare R2 via django-storages | 10 GB free, no egress fees. Local disk in development. |
| QR decoding | zxing-cpp (Python bindings), Pillow | Better than pyzbar on blurry, angled phone photos. Add OpenCV preprocessing only if needed. |
| KRA check | httpx + selectolax (or BeautifulSoup) | Fetch and parse the same page the QR code opens. Isolated in `apps/kra/`. |
| WhatsApp | Meta WhatsApp Cloud API, direct | No reseller markup. Staff message first, so replies fall in the free service window. |
| Export | openpyxl (xlsx) + csv | Formatted spreadsheet accountants can file from. |
| Billing | Safaricom Daraja: STK Push (or M-Pesa Ratiba standing orders) | Needs your own Paybill/Till. Last step; invoice early customers by hand. |
| Hosting | Render or Railway (~$7/mo), or a Hetzner VPS | Cheap, git-push deploys. |
| Errors | Sentry (free tier) | Know when KRA parsing breaks before customers tell you. |
| Tooling | uv, ruff, pytest-django, GitHub Actions | Fast, one tool each, CI matches local `make lint test`. |

Expected running cost before real volume: roughly $10–20 a month.

## Key risks

1. **KRA's verification page is not an official API.** It can change layout, add a
   captcha, or rate-limit us. Mitigations: keep all KRA code in `apps/kra/` behind one
   function (e.g. `verify_invoice(invoice_number) -> KraResult`), save real response
   samples as test fixtures, cache results so each invoice is checked once, rate-limit
   requests, alert via Sentry on parse failures, and apply for proper API access once
   there are paying customers.
2. **QR photos are bad.** Always let staff type the invoice number instead, and keep the
   original photo so an accountant can check by eye.
3. **Personal data.** Register with the Office of the Data Protection Commissioner
   (ODPC) before taking paying customers. Publish a privacy policy.

## Decisions log

Record significant decisions here (date, decision, why) so reviews have context.

- 2026-11-12: Initial stack chosen as above.
