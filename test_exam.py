"""Automated tests for the Online Examination System (index.html + script.js + style.css).
Run from the repository root:  python tests/test_exam.py
Writes tests/results.json and docs/screenshots/
The application files are NOT modified; tests drive the real UI with Playwright.
"""
import json, time, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
URL = (ROOT / "index.html").resolve().as_uri()
SHOTS = ROOT / "docs" / "screenshots"; SHOTS.mkdir(parents=True, exist_ok=True)
RES = []

def rec(tid, module, ttype, desc, inp, expected, actual, ok):
    RES.append(dict(id=tid, module=module, type=ttype, desc=desc, input=inp,
                    expected=expected, actual=str(actual), status="Pass" if ok else "Fail"))

def newpage(b, w=1100, h=800, clock=False, scheme=None):
    ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme or "light")
    pg = ctx.new_page()
    pg.dialogs, pg.errors, pg.accept = [], [], True
    def on_dialog(d):
        pg.dialogs.append((d.type, d.message))
        d.accept() if pg.accept else d.dismiss()
    pg.on("dialog", on_dialog)
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    if clock: pg.clock.install()
    pg.goto(URL)
    return ctx, pg

def vis(pg, sel): return pg.is_visible(sel)
def txt(pg, sel): return pg.inner_text(sel).strip()
def try_login(pg, u, p):
    pg.fill("#u", u); pg.fill("#pw", p); pg.click("#lbtn")
def register(pg, u="student1", p="Pass@123"):
    try_login(pg, u, p); pg.click("#syes"); pg.wait_for_selector("#intro:not(.hide)")
def start(pg): pg.click("#start"); pg.wait_for_selector("#exam:not(.hide)")
def to_exam(pg, **kw): register(pg, **kw); start(pg)
def correct_idx(pg, i): return pg.evaluate("i=>Q[i].o.indexOf(Q[i].c)", i)
def pick(pg, i, idx):
    pg.click(f"#pal button:nth-child({i+1})"); pg.click(f"#opts .opt:nth-child({idx+1})")
def answer(pg, n_correct, n_wrong):
    for i in range(n_correct): pick(pg, i, correct_idx(pg, i))
    for i in range(n_correct, n_correct + n_wrong): pick(pg, i, (correct_idx(pg, i) + 1) % 4)
def submit(pg): pg.click("#sub"); pg.click("#cyes"); pg.wait_for_selector("#res:not(.hide)")
def result(pg): return dict(score=txt(pg, "#rs"), badge=txt(pg, "#rb"), c=txt(pg, "#rc"), w=txt(pg, "#rw"), s=txt(pg, "#ru"), p=txt(pg, "#rp"))

with sync_playwright() as p:
    b = p.chromium.launch()

    # ============ LOGIN ============
    ctx, pg = newpage(b); pg.screenshot(path=str(SHOTS / "01_login.png"))
    try_login(pg, "", ""); a = txt(pg, "#lerr")
    rec("TC01", "Login", "Negative", "Login with both fields empty", "username='', password=''", "Error: Please enter username and password.", a, a == "Please enter username and password.")
    try_login(pg, "student1", ""); a = txt(pg, "#lerr")
    rec("TC02", "Login", "Negative", "Login with empty password", "student1 / ''", "Error: Please enter username and password.", a, a == "Please enter username and password.")
    try_login(pg, "   ", "abc"); a = txt(pg, "#lerr")
    rec("TC03", "Login", "Negative", "Whitespace-only username", "'   ' / abc", "Error: Please enter username and password.", a, a == "Please enter username and password.")
    pg.fill("#u", "student1"); pg.fill("#pw", "Pass@123"); pg.click("#lbtn")
    m = vis(pg, "#sm"); t = txt(pg, "#sat")
    pg.screenshot(path=str(SHOTS / "02_save_modal.png"))
    rec("TC04", "Login", "Functional", "Unknown username triggers 'Save account' dialog", "student1 / Pass@123 (new)", "Dialog 'Save this account?' shown", t, m and "No account found" in t)
    pg.click("#sno"); a = txt(pg, "#lerr")
    rec("TC05", "Login", "Functional", "Choose 'No' in save dialog", "Click No", "Stay on login; message says account not saved", a, vis(pg, "#login") and "not saved" in a)
    pg.fill("#u", "student1"); pg.fill("#pw", "Pass@123"); pg.click("#lbtn"); pg.click("#syes"); pg.wait_for_selector("#intro:not(.hide)")
    pg.screenshot(path=str(SHOTS / "03_intro.png"))
    a = txt(pg, "#name"); rec("TC06", "Login", "Functional", "Choose 'Yes' saves account and logs in", "Click Yes, save & login", "Instructions page, greeting shows username", a, vis(pg, "#intro") and a == "student1")
    pg.click("#out"); a = vis(pg, "#login"); rec("TC07", "Login", "Functional", "Logout from instructions page", "Click Logout", "Login screen shown", "Login screen" if a else "Not shown", a)
    try_login(pg, "student1", "Pass@123"); ok = vis(pg, "#intro")
    rec("TC08", "Login", "Functional", "Login with saved valid credentials", "student1 / Pass@123", "Instructions page opens (no save dialog)", "Intro visible" if ok else "Not visible", ok and not vis(pg, "#sm"))
    pg.click("#out"); try_login(pg, "student1", "WrongPass"); a = txt(pg, "#lerr"); pg.screenshot(path=str(SHOTS / "04_login_error.png"))
    rec("TC09", "Login", "Negative", "Existing user with wrong password", "student1 / WrongPass", "Error: Incorrect password for this username.", a, a == "Incorrect password for this username.")
    try_login(pg, "student1", "pass@123"); a = txt(pg, "#lerr")
    rec("TC10", "Login", "Equivalence", "Password is case-sensitive", "student1 / pass@123", "Incorrect password error", a, a == "Incorrect password for this username.")
    try_login(pg, "STUDENT1", "Pass@123"); ok = vis(pg, "#intro"); n = txt(pg, "#name") if ok else ""
    rec("TC11", "Login", "Equivalence", "Username is case-insensitive", "STUDENT1 / Pass@123", "Login succeeds as 'student1'", f"intro={ok}, name={n}", ok and n == "student1")
    pg.click("#out"); pg.fill("#u", "student1"); pg.fill("#pw", "Pass@123"); pg.press("#pw", "Enter"); ok = vis(pg, "#intro")
    rec("TC12", "Login", "Usability", "Enter key in password field submits login", "Press Enter", "Logs in", "Intro visible" if ok else "Not logged in", ok)
    pg.click("#out"); pg.fill("#u", "student1"); pg.press("#u", "Enter"); f = pg.evaluate("document.activeElement.id")
    rec("TC13", "Login", "Usability", "Enter in username moves focus to password", "Press Enter in username", "Focus moves to password", f"focus on #{f}", f == "pw")
    ctx.close()

    ctx, pg = newpage(b)
    pg.evaluate("user=null"); pg.evaluate("document.getElementById('start').click()"); a = vis(pg, "#login") and not vis(pg, "#exam")
    rec("TC14", "Access Control", "Security", "Exam cannot be started without logging in", "Trigger Start while not logged in", "Redirected to login; exam hidden", "Login shown, exam hidden" if a else "Exam reachable", a)
    ok = (not vis(pg, "#exam")) and (not vis(pg, "#intro")) and (not vis(pg, "#res"))
    rec("TC15", "Access Control", "Security", "Only login screen visible on first load", "Open app", "Intro, exam, result hidden", "Only login visible" if ok else "Other screens visible", ok)
    ctx.close()

    # ============ INSTRUCTIONS / START ============
    ctx, pg = newpage(b); register(pg); t = txt(pg, "#intro")
    rec("TC16", "Instructions", "Functional", "Instructions show duration, question count and auto-submit rule", "Open instructions", "60 minutes, 20 MCQs, auto-submit text present", "60 minutes" in t and "20 MCQs" in t and "automatically" in t, "60 minutes" in t and "20 MCQs" in t and "automatically" in t)
    start(pg); pg.screenshot(path=str(SHOTS / "05_exam.png"))
    qn, tm = txt(pg, "#qn"), txt(pg, "#timer")
    rec("TC17", "Exam", "Functional", "Start exam shows Q1 of 20 and a 60:00 timer", "Click Start Examination", "'Question 1 of 20', timer 60:00", f"{qn}; {tm}", qn == "Question 1 of 20" and tm == "60:00")
    n = pg.evaluate("Q.length"); pal = pg.locator("#pal button").count()
    rec("TC18", "Exam", "Functional", "Exam has exactly 20 questions and 20 navigator buttons", "Inspect exam", "20 questions, 20 buttons", f"{n} questions, {pal} buttons", n == 20 and pal == 20)
    nb = pg.evaluate("BANK.length"); uniq = pg.evaluate("new Set(BANK.map(r=>r[0])).size")
    rec("TC19", "Question Bank", "Functional", "All bank questions are unique", "Inspect question bank", "No duplicate questions", f"{uniq} unique of {nb}", uniq == nb)
    bad = pg.evaluate("BANK.filter(r=>new Set(r.slice(1)).size!==4).length")
    rec("TC20", "Question Bank", "Functional", "Each question has 4 distinct options", "Inspect all questions", "0 questions with duplicate options", f"{bad} problem question(s)", bad == 0)
    shown = pg.evaluate("Q.every(x=>x.o.includes(x.c))")
    rec("TC21", "Question Bank", "Functional", "Correct answer is always among the displayed options", "Inspect exam questions", "True for all 20", str(shown), shown)
    first = pg.evaluate("Q.map(x=>x.q).join('|')"); pg.reload(); pg.fill("#u", "student1"); pg.fill("#pw", "Pass@123"); pg.click("#lbtn"); start(pg)
    second = pg.evaluate("Q.map(x=>x.q).join('|')")
    rec("TC22", "Question Bank", "Functional", "Question order is randomised between attempts", "Start two exams", "Different order each time", "Different" if first != second else "Same order", first != second)
    ctx.close()

    # ============ NAVIGATION & ANSWERS ============
    ctx, pg = newpage(b); to_exam(pg)
    rec("TC23", "Navigation", "Boundary Value", "Previous disabled on question 1", "Open Q1", "Previous disabled", "disabled" if pg.is_disabled("#prev") else "enabled", pg.is_disabled("#prev"))
    pg.click("#next"); a = txt(pg, "#qn")
    rec("TC24", "Navigation", "Functional", "Next moves to question 2", "Click Next", "Question 2 of 20", a, a == "Question 2 of 20")
    pg.click("#pal button:nth-child(20)"); d = pg.is_disabled("#next")
    rec("TC25", "Navigation", "Boundary Value", "Next disabled on question 20", "Jump to Q20", "Next disabled", "disabled" if d else "enabled", d)
    pg.click("#pal button:nth-child(10)"); a = txt(pg, "#qn")
    rec("TC26", "Navigation", "Functional", "Navigator jumps to chosen question", "Click button 10", "Question 10 of 20", a, a == "Question 10 of 20")
    pg.click("#pal button:nth-child(1)"); pg.click("#opts .opt:nth-child(2)"); pg.click("#next"); pg.click("#prev")
    sel = pg.evaluate("[...document.querySelectorAll('#opts .opt')].findIndex(o=>o.classList.contains('sel'))")
    rec("TC27", "Navigation", "Functional", "Answer is remembered when moving away and back", "Pick option B, Next, Previous", "Option B still selected", f"selected index {sel}", sel == 1)
    pg.click("#opts .opt:nth-child(3)"); n = pg.locator("#opts .opt.sel").count(); sel = pg.evaluate("[...document.querySelectorAll('#opts .opt')].findIndex(o=>o.classList.contains('sel'))")
    rec("TC28", "Answering", "Functional", "Changing answer keeps only one option selected", "Pick B, then C", "Only C selected", f"{n} selected, index {sel}", n == 1 and sel == 2)
    pr = txt(pg, "#prog"); cls = pg.get_attribute("#pal button:nth-child(1)", "class")
    rec("TC29", "Answering", "Functional", "Answered question is marked in navigator and progress", "Answer Q1", "'1/20 answered', button turns green", f"{pr}; class='{cls}'", pr == "1/20 answered" and "ans" in cls)
    pg.click("#clr"); pr = txt(pg, "#prog"); n = pg.locator("#opts .opt.sel").count()
    rec("TC30", "Answering", "Functional", "Clear answer removes selection", "Click Clear answer", "No option selected, '0/20 answered'", f"{n} selected; {pr}", n == 0 and pr == "0/20 answered")
    pick(pg, 0, 0); pick(pg, 5, 1); pick(pg, 19, 2); pr = txt(pg, "#prog")
    pg.screenshot(path=str(SHOTS / "06_exam_answered.png"))
    rec("TC31", "Answering", "Functional", "Progress counter tracks several answers", "Answer Q1, Q6, Q20", "'3/20 answered'", pr, pr == "3/20 answered")
    ctx.close()

    # ============ TIMER ============
    ctx, pg = newpage(b, clock=True); to_exam(pg)
    pg.clock.run_for(5000); a = txt(pg, "#timer")
    rec("TC32", "Timer", "Functional", "Timer counts down every second", "Wait 5 seconds", "59:55", a, a == "59:55")
    pg.click("#next"); pg.click("#next"); pg.clock.run_for(5000); a = txt(pg, "#timer")
    rec("TC33", "Timer", "Functional", "Timer is not reset by navigating questions", "Next twice, wait 5 s", "59:50", a, a == "59:50")
    pg.clock.run_for(3300000 - 10000); a = txt(pg, "#timer"); low = "low" in (pg.get_attribute("#timer", "class") or "")
    pg.screenshot(path=str(SHOTS / "07_timer_low.png"))
    rec("TC34", "Timer", "Boundary Value", "Timer turns red at 05:00 remaining", "Advance to 55 minutes", "05:00 with warning style", f"{a}, low={low}", a == "05:00" and low)
    pg.clock.run_for(299000); a = txt(pg, "#timer")
    rec("TC35", "Timer", "Boundary Value", "One second before time-up exam is still running", "Advance to 59:59", "00:01, exam visible", f"{a}, exam visible={vis(pg, '#exam')}", a == "00:01" and vis(pg, "#exam"))
    pg.clock.run_for(1000)
    msg = txt(pg, "#rmsg"); pg.screenshot(path=str(SHOTS / "08_autosubmit.png"))
    rec("TC36", "Auto-submit", "Boundary Value", "Exam auto-submits at 00:00", "Advance to 60:00", "Result page with 'Time is up' message", msg, vis(pg, "#res") and "Time is up" in msg)
    t1 = txt(pg, "#rt"); pg.clock.run_for(120000); t2 = txt(pg, "#rt")
    rec("TC37", "Auto-submit", "Functional", "Timer stops after submission (time taken stays fixed)", "Wait 2 more minutes", "Time taken unchanged: 60:00", f"{t1} -> {t2}", t1 == t2 and "60:00" in t1)
    ctx.close()

    # ============ SUBMIT ============
    ctx, pg = newpage(b); to_exam(pg); pg.click("#sub"); t = txt(pg, "#cmt"); pg.screenshot(path=str(SHOTS / "09_submit_modal.png"))
    rec("TC38", "Submit", "Functional", "Submit asks confirmation and shows unanswered count", "Click Submit with no answers", "Dialog: 20 unanswered + time left", t, vis(pg, "#cm") and "20 unanswered" in t and "Time left" in t)
    pg.click("#cno"); ok = vis(pg, "#exam") and not vis(pg, "#cm")
    rec("TC39", "Submit", "Functional", "'Continue exam' closes the dialog and keeps exam", "Click Continue exam", "Exam still visible", "Exam continues" if ok else "Exam lost", ok)
    answer(pg, 20, 0); pg.click("#sub"); t = txt(pg, "#cmt")
    rec("TC40", "Submit", "Functional", "Dialog says all answered when none are skipped", "Answer all, Submit", "'All questions answered'", t, "All questions answered" in t)
    pg.click("#cyes"); msg = txt(pg, "#rmsg")
    rec("TC41", "Submit", "Functional", "Manual submit shows success message", "Click Yes, submit", "'Exam submitted successfully'", msg, "submitted successfully" in msg)
    ctx.close()

    # ============ SCORING (boundary values) ============
    cases = [("TC42", 20, 0, "20 / 20", "PASS", "100%", "All 20 correct"),
             ("TC43", 0, 20, "0 / 20", "FAIL", "0%", "All 20 wrong"),
             ("TC44", 0, 0, "0 / 20", "FAIL", "0%", "No answers (all skipped)"),
             ("TC45", 8, 12, "8 / 20", "PASS", "40%", "8 correct = 40% (pass boundary)"),
             ("TC46", 7, 13, "7 / 20", "FAIL", "35%", "7 correct = 35% (just below pass mark)")]
    for tid, c, w, sc, badge, pct, d in cases:
        ctx, pg = newpage(b); to_exam(pg); answer(pg, c, w); submit(pg); r = result(pg)
        if tid == "TC42": pg.screenshot(path=str(SHOTS / "10_result_pass.png"))
        if tid == "TC46": pg.screenshot(path=str(SHOTS / "11_result_fail.png"))
        rec(tid, "Scoring", "Boundary Value", d, f"{c} correct, {w} wrong, {20-c-w} skipped", f"{sc}, {badge}, {pct}", f"{r['score']}, {r['badge']}, {r['p']}", r["score"] == sc and r["badge"] == badge and r["p"] == pct)
        ctx.close()
    ctx, pg = newpage(b); to_exam(pg); answer(pg, 5, 5); submit(pg); r = result(pg)
    rec("TC47", "Scoring", "Functional", "Correct + wrong + skipped always equals 20", "5 correct, 5 wrong, 10 skipped", "5 / 5 / 10", f"{r['c']} / {r['w']} / {r['s']}", (r["c"], r["w"], r["s"]) == ("5", "5", "10"))
    n = pg.locator("#rev .rv").count(); cc, ww, ss = (pg.locator(f"#rev .rv.{k}").count() for k in "cws")
    pg.screenshot(path=str(SHOTS / "12_review.png"), full_page=True)
    rec("TC48", "Review", "Functional", "Answer review lists all 20 questions with correct status", "Open review after mixed attempt", "20 items: 5 correct, 5 wrong, 10 skipped", f"{n} items: {cc}/{ww}/{ss}", n == 20 and (cc, ww, ss) == (5, 5, 10))
    wrong_ok = pg.evaluate("[...document.querySelectorAll('#rev .rv.w')].every(d=>d.textContent.includes('Correct answer:'))")
    rec("TC49", "Review", "Functional", "Wrong answers display the correct answer", "Inspect wrong items", "Each shows 'Correct answer:'", str(wrong_ok), wrong_ok)
    rec("TC50", "Review", "Functional", "Time taken and pass mark shown on result", "Inspect result footer", "'Time taken' and 'Passing mark: 40%'", txt(pg, "#rt"), "Time taken" in txt(pg, "#rt") and "40%" in txt(pg, "#rt"))
    pg.click("#rout"); ok = vis(pg, "#login")
    rec("TC51", "Result", "Functional", "Logout from result page", "Click Logout", "Login screen shown", "Login shown" if ok else "Not shown", ok)
    ctx.close()

    # ============ LOGOUT DURING EXAM ============
    ctx, pg = newpage(b); to_exam(pg); hasbtn = vis(pg, "#out")
    pg.accept = False; pg.evaluate("logout()")
    stay = vis(pg, "#exam"); pg.accept = True; pg.evaluate("logout()"); gone = vis(pg, "#login")
    rec("TC52", "Session", "Functional", "logout() asks confirmation during an exam (called via console, no Logout button exists on exam screen)", "logout(): Cancel, then OK", "Cancel stays in exam; OK returns to login", f"after cancel exam={stay}; after OK login={gone}; logout button visible on exam screen={hasbtn}", stay and gone)
    ctx.close()

    # ============ SECURITY ============
    ctx, pg = newpage(b); register(pg, "student1", "Pass@123Secret")
    raw = pg.evaluate("localStorage.getItem('examUsers')")
    rec("TC53", "Security", "Security", "Password is not stored in plain text", "Inspect localStorage 'examUsers'", "Plain password absent (hashed)", raw, "Pass@123Secret" not in raw)
    wn = pg.evaluate("window.name")
    rec("TC54", "Security", "Security", "Credentials are not exposed in window.name", "Inspect window.name", "No credentials in window.name", wn, "Pass@123Secret" not in wn)
    exposed = pg.evaluate("typeof BANK!=='undefined' && BANK[0].length===5")
    rec("TC55", "Security", "Security", "Answer key is not readable from the browser console", "Evaluate BANK in console", "Answer key inaccessible", "BANK readable: correct answers exposed" if exposed else "Not accessible", not exposed)
    ctx.close()
    ctx, pg = newpage(b); register(pg, "<img src=x onerror=alert(1)>", "xss12345")
    imgs = pg.locator("#name img").count(); t = txt(pg, "#name")
    rec("TC56", "Security", "Security", "XSS payload in username is escaped", "<img src=x onerror=alert(1)>", "Shown as text; no script runs", f"img={imgs}, alerts={[d for d in pg.dialogs if d[0]=='alert']}, text={t}", imgs == 0 and not [d for d in pg.dialogs if d[0] == 'alert'])
    ctx.close()
    ctx, pg = newpage(b); try_login(pg, "' OR '1'='1' --", "' OR '1'='1"); m = vis(pg, "#sm"); intro = vis(pg, "#intro")
    rec("TC57", "Security", "Security", "SQL-injection style input does not bypass login", "' OR '1'='1' --", "Treated as plain new username; no access without confirm", f"save dialog={m}, intro={intro}", m and not intro)
    pg.click("#sno"); try_login(pg, "__proto__", "abc"); m = vis(pg, "#sm")
    try_login_ok = m; pg.click("#syes") if m else None
    rec("TC58", "Security", "Security", "Reserved JS names like '__proto__' do not crash or bypass login", "__proto__ / abc", "Handled as ordinary username; no JS error", f"dialog={m}; errors={pg.errors}", m and not pg.errors)
    ctx.close()
    ctx, pg = newpage(b); try_login(pg, "weakuser", "1"); m = vis(pg, "#sm")
    rec("TC59", "Security", "Boundary Value", "1-character password is rejected by password policy", "weakuser / '1'", "Rejected (minimum length enforced)", "Accepted - account creation offered" if m else "Rejected", not m)
    ctx.close()
    ctx, pg = newpage(b); to_exam(pg); answer(pg, 3, 0)
    pg.reload(); pg.wait_for_load_state(); loginv = vis(pg, "#login")
    try_login(pg, "student1", "Pass@123"); pg.click("#start"); tm = txt(pg, "#timer"); pr = txt(pg, "#prog")
    rec("TC60", "Session", "Functional", "Exam progress and remaining time survive a page reload", "Answer 3, wait, reload", "Exam resumes with answers and remaining time", f"login shown={loginv}; new exam timer={tm}, {pr}", False if (loginv and tm == "60:00") else True)
    ctx.close()

    # ============ UI / ACCESSIBILITY / PERFORMANCE ============
    ctx, pg = newpage(b, 375, 760)
    sw = [pg.evaluate("document.documentElement.scrollWidth")]
    pg.screenshot(path=str(SHOTS / "13_mobile_login.png"))
    to_exam(pg); answer(pg, 3, 0); sw.append(pg.evaluate("document.documentElement.scrollWidth")); pg.screenshot(path=str(SHOTS / "14_mobile_exam.png"), full_page=True)
    submit(pg); sw.append(pg.evaluate("document.documentElement.scrollWidth"))
    rec("TC61", "UI", "Usability", "No horizontal scrolling on mobile (375 px) for login, exam, result", "Viewport 375x760", "scrollWidth <= 375 on all screens", f"login/exam/result = {sw}", max(sw) <= 375)
    ctx.close()
    ctx, pg = newpage(b); n = pg.evaluate("[...document.querySelectorAll('input')].filter(i=>i.labels.length===0).length")
    rec("TC62", "Accessibility", "Usability", "Every input is programmatically linked to a label", "Inspect login form", "0 inputs without a label link", f"{n} input(s) without linked label", n == 0)
    register(pg); start(pg); ti = pg.evaluate("[...document.querySelectorAll('#opts .opt')].filter(o=>o.tabIndex<0).length")
    rec("TC63", "Accessibility", "Usability", "Answer options can be reached with the keyboard", "Check option elements", "All 4 options focusable (tabindex >= 0)", f"{ti} of 4 not focusable", ti == 0)
    ctx.close()
    ctx, pg = newpage(b, scheme="dark"); bg = pg.evaluate("getComputedStyle(document.body).backgroundColor"); pg.screenshot(path=str(SHOTS / "15_dark.png"))
    rec("TC64", "UI", "Usability", "Dark mode is applied automatically", "prefers-color-scheme: dark", "Dark background", bg, bg == "rgb(16, 20, 31)")
    ctx.close()
    ctx = b.new_context(); pg = ctx.new_page(); t0 = time.time(); pg.goto(URL); pg.wait_for_selector("#login"); dt = (time.time() - t0) * 1000
    rec("TC65", "Performance", "Performance", "Initial page load time", "Open index.html", "Under 1000 ms", f"{dt:.0f} ms", dt < 1000)
    ctx.close()
    ctx, pg = newpage(b); to_exam(pg)
    ms = pg.evaluate("()=>{const t=performance.now();for(let i=0;i<20;i++)document.querySelector('#pal button:nth-child('+(i+1)+')').click();return (performance.now()-t)/20}")
    rec("TC66", "Performance", "Performance", "Average question switch time", "Switch through 20 questions", "Under 50 ms per switch", f"{ms:.1f} ms", ms < 50)
    answer(pg, 10, 10); t0 = time.time(); submit(pg); dt = (time.time() - t0) * 1000
    rec("TC67", "Performance", "Performance", "Result and review generated quickly", "Submit full exam", "Under 1000 ms", f"{dt:.0f} ms", dt < 1000)
    ctx.close()
    b.close()

json.dump(RES, open(HERE / "results.json", "w"), indent=1)
ps = sum(r["status"] == "Pass" for r in RES); print(f"{ps}/{len(RES)} passed")
for r in RES:
    if r["status"] != "Pass": print("FAIL", r["id"], r["desc"], "->", r["actual"][:140])
