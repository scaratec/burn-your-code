# Preparation — please do this before the workshop (15 minutes)

The workshop is hands-on. Venue Wi-Fi is usually slow, so install everything at home and finish with a green `make check`.

## You need

| | Version | Check |
|---|---|---|
| Laptop with macOS or Linux (Windows: use WSL2 with Ubuntu) | — | — |
| git, make, curl | any recent | `git --version`, `make --version` |
| Python | 3.11 or newer | `python3 --version` |
| Antigravity CLI (`agy`) signed in with a **personal** Google account | 1.5 or newer | `agy --version` |
| *Optional:* a second language toolchain for exercise 4 (Go, Node.js, Rust, Java …) | any | — |

No Docker, no cloud account and no paid plan are needed for the exercises.

**Which Google account?** Use a personal Google account (for example `@gmail.com`; Free, Pro or Ultra plan — `make check` tells you whether the workshop model is available to you). A work or school account signs in as a *Business account*: that only works if your organisation has already assigned you a Gemini Enterprise licence and a Google Cloud project, and its auto mode is not available (`agy` then asks before each edit or command). If that is not already set up for you, use a personal account.

## Steps

1. **Install the Antigravity CLI** following the official quickstart: <https://antigravity.google/docs/getting-started>. Open a new terminal afterwards so `agy` is on your `PATH`.
2. **Clone the repository** (a ZIP download does not work, the exercises use git):

   ```bash
   git clone https://github.com/scaratec/burn-your-code.git
   cd burn-your-code/workshop
   ```

3. **Sign in and trust the folder:** in `burn-your-code/workshop`, run `agy`. Sign in with your personal Google account in the browser, complete the sign-in and the first-run questions, and answer **"Yes, I trust this folder"**. Then exit with `/exit`.
   Trusting the folder now matters: if you trust it only during the workshop, `agy` asks before reading every single file until you restart it.

4. **Set up and self-test:**

   ```bash
   make setup
   make check
   ```

   `make check` verifies Python, git, the Antigravity CLI sign-in, the model `gemini-3.8-flash-high`, that `agy` trusts this folder, and runs the first test milestone (16 scenarios must pass).

## Expected output

```text
  OK   Python 3.12.3 (3.11 or newer)
  OK   Python test environment (.venv with behave)
  OK   git clone of the repository (checkpoints need git)
  OK   Antigravity CLI installed (agy)
  OK   Antigravity CLI signed in
  OK   model gemini-3.8-flash-high available
  OK   this folder is trusted by the Antigravity CLI
  OK   MI1 test suite green (16 scenarios passed)

All checks passed. You are ready for the workshop.
```

## If something fails

| Message | Fix |
|---|---|
| `agy: command not found` | Open a new terminal; or add `~/.local/bin` to your `PATH`. |
| `Antigravity CLI signed in` fails | Run `agy` once and finish the browser sign-in. On a remote machine, `agy` prints a URL and asks for a code. |
| `this folder is trusted` fails | Run `agy` in `burn-your-code/workshop`, answer "Yes, I trust this folder", then `/exit`. |
| `model gemini-3.8-flash-high` missing | Run `agy models`. With a business account, sign out (`/logout` inside `agy`) and sign in with a personal account. Otherwise tell the facilitator which models you see. |
| `MI1 test suite green` fails | Run `make workshop-start`, then `make check` again. |
| A checkpoint fails with "configured for Git LFS but 'git-lfs' was not found" | Install Git LFS (<https://git-lfs.com>), or delete `.git/hooks/post-checkout`. The exercises themselves do not need it. |

The exercises use a few minutes of model time each (roughly 0.5–2 million tokens per exercise, most of them cached). We have not measured whether every free plan covers all of them; if your quota runs out during the workshop, pair up with a neighbour or use the `make exN-solution` checkpoints to keep going.
