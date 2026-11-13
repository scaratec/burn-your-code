# Preparation — please do this before the workshop (15 minutes)

The workshop is hands-on. Venue Wi-Fi is usually slow, so install everything at home and finish with a green `make check`.

## You need

| | Version | Check |
|---|---|---|
| Laptop with macOS or Linux (Windows: use WSL2 with Ubuntu) | — | — |
| git, make, curl | any recent | `git --version`, `make --version` |
| Python | 3.11 or newer | `python3 --version` |
| Antigravity CLI (`agy`) with your Google account | 1.5 or newer | `agy --version` |
| *Optional:* a second language toolchain for exercise 4 (Go, Node.js, Rust, Java …) | any | — |

No Docker, no cloud account and no paid plan are needed for the exercises.

## Steps

1. **Install the Antigravity CLI** following the official quickstart: <https://antigravity.google/docs/getting-started>. Open a new terminal afterwards so `agy` is on your `PATH`.
2. **Sign in once:** run `agy`, choose *Google OAuth* and complete the sign-in in your browser. Exit with `/exit`.
3. **Clone the repository** (a ZIP download does not work, the exercises use git):

   ```bash
   git clone https://github.com/scaratec/burn-your-code.git
   cd burn-your-code/workshop
   ```

4. **Set up and self-test:**

   ```bash
   make setup
   make check
   ```

   `make check` verifies Python, git, the Antigravity CLI sign-in, the model `gemini-3.8-flash-high`, and runs the first test milestone (16 scenarios must pass).

## Expected output

```text
  OK   Python 3.12.3 (3.11 or newer)
  OK   Python test environment (.venv with behave)
  OK   git clone of the repository (checkpoints need git)
  OK   Antigravity CLI installed (agy)
  OK   Antigravity CLI signed in
  OK   model gemini-3.8-flash-high available
  OK   MI1 test suite green (16 scenarios passed)

All checks passed. You are ready for the workshop.
```

## If something fails

| Message | Fix |
|---|---|
| `agy: command not found` | Open a new terminal; or add `~/.local/bin` to your `PATH`. |
| `Antigravity CLI signed in` fails | Run `agy` once and finish the browser sign-in. On a remote machine, `agy` prints a URL and asks for a code. |
| `model gemini-3.8-flash-high` missing | Run `agy models` and check your plan; tell the facilitator which models you see. |
| `MI1 test suite green` fails | Run `make workshop-start`, then `make check` again. |

The exercises use a few minutes of model time each. If your daily quota runs out during the workshop, every exercise has a `make exN-solution` checkpoint so you can keep going.
