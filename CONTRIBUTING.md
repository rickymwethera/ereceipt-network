# How we work

1. Pick the next issue from the roadmap (`docs/ROADMAP.md`, and the GitHub issues
   labelled `v1`). Work on them roughly in order; later steps build on earlier ones.
2. Create a branch named after it: `git switch -c 03-qr-decoding`.
3. Keep PRs small. One issue per PR. If a PR grows past ~400 lines of real code
   (not counting migrations or fixtures), split it.
4. Write tests as you go. Anything that parses outside data (QR contents, KRA pages,
   WhatsApp webhooks, M-Pesa callbacks) must have tests that use saved real samples
   from `tests/fixtures/`.
5. Run `make fmt && make test` before pushing.
6. Open a PR using the template and write `Closes #N`. CI must be green.
7. Ask for a review. Fix or reply to every comment before merging.

## Rules that save pain later

- **Secrets** go in `.env` (local) or the host's environment settings (production). Never
  commit them. If one leaks, rotate it immediately.
- **Personal data**: phone numbers, KRA PINs and receipt photos are personal data under
  the Kenya Data Protection Act. Don't log them in full, and don't copy production data
  to your laptop.
- **KRA code stays in `apps/kra/`**. KRA can change their page at any time; when that
  happens we want to fix one module, not hunt through the codebase.
- **Slow or flaky work runs in background jobs**, never inside a web request or the
  WhatsApp webhook. The webhook must answer Meta within a few seconds.
- **Money is stored as integer cents** (`amount_cents`), never floats.
