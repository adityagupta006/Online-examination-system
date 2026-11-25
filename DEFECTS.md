# Defect Log

Found by the automated test suite; the application code was **not modified**. Status of all defects: **Open**.

| ID | Failed tests | Defect | Severity | Recommended fix |
|---|---|---|---|---|
| DEF-01 | TC53, TC54 | Passwords are stored in **plain text** in localStorage, sessionStorage, a cookie and `window.name`. Anyone with browser access, or a site opened later in the same tab, can read them. | High | Never store passwords in the browser. Authenticate on a server and keep only a session token; at minimum salt and hash. Remove the `window.name` and cookie copies. |
| DEF-02 | TC55 | The **answer key is readable**: typing `BANK` in the console lists every correct answer. | High | Keep questions and answers on a server, send one question at a time and check answers server-side. |
| DEF-03 | TC60 | **Reloading mid-exam loses all progress**; logging in again starts a new exam with a full 60:00 timer, so time limits can be bypassed. | High | Persist attempt start time, answers and question order (server-side, or at least sessionStorage) and compute remaining time from the saved start time. |
| DEF-04 | TC59 | **No password policy**: a 1-character password is accepted. | Medium | Enforce a minimum length (e.g. 8) and basic complexity. |
| DEF-05 | TC63 | Answer options are plain `div` elements with no `tabindex`, role or key handler, so they **cannot be chosen with the keyboard**. | Medium | Use radio inputs or buttons, or add `role="radio"`, `tabindex` and Enter/Space handlers. |
| DEF-06 | TC62 | Username and password inputs are **not linked to their labels** (no `for` attribute). | Low | Add `for`/`id` pairs or wrap inputs in their labels. |

## Additional observations
- **No Logout button on the exam screen.** The confirmation in `logout()` cannot be reached from the UI during an exam (verified by calling the function directly, TC52).
- **Unknown usernames create an account automatically**, so login is not a real identity check.
- **Unlimited attempts** per student (combined with DEF-03, a student can restart at will).
- **Timer uses a one-second interval counter** instead of wall-clock time, so background-tab throttling or device sleep can extend the exam beyond 60 minutes.
- **Cookie storage not verified**: browsers do not store cookies for local files; re-check when the app is hosted.
