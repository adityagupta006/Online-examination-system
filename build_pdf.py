import json, collections, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import *
from PIL import Image as PI
R=json.load(open("tests/results.json"))
PRI=colors.HexColor("#3b5bdb")
ss=getSampleStyleSheet()
B=ParagraphStyle("B",parent=ss["BodyText"],fontSize=10,leading=14.5,spaceAfter=6)
H1=ParagraphStyle("H1",parent=ss["Heading1"],fontSize=17,textColor=PRI,spaceBefore=6,spaceAfter=8,keepWithNext=1)
H2=ParagraphStyle("H2",parent=ss["Heading2"],fontSize=12.5,textColor=colors.HexColor("#1d2433"),spaceBefore=8,spaceAfter=5,keepWithNext=1)
C=ParagraphStyle("C",parent=B,fontSize=8.5,leading=11,textColor=colors.grey,alignment=1)
T=ParagraphStyle("T",parent=B,fontSize=7.3,leading=9,spaceAfter=0)
TH=ParagraphStyle("TH",parent=T,textColor=colors.white,fontName="Helvetica-Bold")
BL=ParagraphStyle("BL",parent=B,leftIndent=14,bulletIndent=4,spaceAfter=2)
def P(t,s=B): return Paragraph(t,s)
def bullets(items): return [Paragraph(i,BL,bulletText="\u2022") for i in items]
esc=lambda s:str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def tbl(rows,widths,head=True,fs=T):
    data=[[Paragraph(str(c),TH if (head and i==0) else fs) for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1 if head else 0)
    st=[("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#c9d1e6")),("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]
    if head: st.append(("BACKGROUND",(0,0),(-1,0),PRI))
    for i in range(1,len(rows)):
        if i%2==0: st.append(("BACKGROUND",(0,i),(-1,i),colors.HexColor("#f6f8fd")))
    t.setStyle(TableStyle(st)); return t
def img(path,w):
    iw,ih=PI.open(path).size; return Image(path,width=w,height=w*ih/iw)
def fig(path,cap,w=15*cm): return KeepTogether([img(path,w),P(cap,C),Spacer(1,6)])
def footer(c,d):
    c.saveState(); c.setFont("Helvetica",8); c.setFillColor(colors.grey)
    c.drawString(1.8*cm,1.1*cm,"Online Examination System - Software Testing, Unit 5"); c.drawRightString(A4[0]-1.8*cm,1.1*cm,f"Page {d.page}"); c.restoreState()

passed=sum(r["status"]=="Pass" for r in R); failed=[r for r in R if r["status"]=="Fail"]
S=[]
S+=[Spacer(1,3.3*cm),P('<font size=28 color="#3b5bdb"><b>Online Examination System</b></font>',ParagraphStyle("x",alignment=1,leading=34)),
 P('<font size=14>System Design, Prototype and Test Case Design</font>',ParagraphStyle("x2",alignment=1,leading=20,spaceAfter=24)),
 P('<b>Software Testing - Unit 5: Emerging Trends in Software Technologies</b>',ParagraphStyle("x3",alignment=1,fontSize=12,leading=18,spaceAfter=40)),
 tbl([["Student name","[Your name]"],["Roll / Enrolment no.","[Your roll number]"],["Course / Semester","[Course, semester]"],["Submitted to","[Faculty name]"],["Date","13 November 2026"],["GitHub repository","[Paste your GitHub link here]"],["Live prototype","[Paste your hosted link here]"]],[5*cm,10*cm],head=False,fs=ParagraphStyle("tt",parent=T,fontSize=9.5,leading=13)),PageBreak()]

S+=[P("Contents",H1)]+bullets(["1. Introduction and problem statement","2. Requirements","3. System design and architecture","4. Prototype and screenshots","5. Test plan and strategy","6. Test cases and execution results","7. Defect report and analysis","8. Limitations, conclusion and future scope","9. Links and project files"])+[Spacer(1,8)]
S+=[P("1. Introduction and Problem Statement",H1),
 P("Online assessment is one of the fastest-growing technology trends in education: schools, colleges and certification bodies increasingly conduct timed tests in the browser instead of on paper. A browser-based exam must handle identity, strict timing, fair question delivery, instant evaluation and a clear review of answers."),
 P("The <b>Online Examination System</b> is a responsive, single-page web application built with HTML, CSS and JavaScript. A student logs in, reads the instructions, takes a <b>60-minute, 20-question MCQ test on Software Testing</b>, can move freely between questions, submits manually or is auto-submitted when the timer ends, and immediately sees a score with a detailed answer review. The interface also adapts to mobile screens and to dark mode."),
 P("Objectives",H2)]+bullets(["Allow only logged-in students to start the exam.","Deliver 20 randomised MCQs with a 60-minute countdown and automatic submission.","Support free navigation, changing and clearing answers, with a live question navigator.","Evaluate instantly (40% pass mark) and show a per-question review.","Design and run a comprehensive test suite and report every defect found in the application."])
S+=[P("2. Requirements",H1),P("Functional requirements (taken from the requirement notes in the source code)",H2),
 tbl([["ID","Requirement"],["FR1","Student logs in with a valid username and password (accounts are saved in the browser)."],["FR2","The exam can be started only after login."],["FR3","Exam duration is 60 minutes with a visible countdown."],["FR4","Exam contains 20 MCQs, 1 mark each, no negative marking; questions and options are shuffled."],["FR5","Student can navigate to any question, change an answer or clear it."],["FR6","Student can submit manually before time ends, after a confirmation prompt."],["FR7","Exam is auto-submitted when the 60 minutes are over."],["FR8","Result (score, pass/fail at 40%, correct/wrong/skipped, percent) and an answer review are shown after submission."]],[1.6*cm,16*cm]),Spacer(1,6),
 P("Non-functional requirements",H2)]+bullets(["<b>Security:</b> credentials protected; user-entered text cannot execute scripts; exam answers not exposed.","<b>Reliability:</b> timer accuracy; exam state should not be lost accidentally.","<b>Usability and accessibility:</b> responsive layout, keyboard and screen-reader support, dark mode.","<b>Performance:</b> fast load and instant question switching."])

S+=[P("3. System Design and Architecture",H1),
 P("The application is a <b>client-side single-page application</b>. One HTML file contains five screens (login, instructions, exam, result and two modal dialogs); only one screen is visible at a time and <font name=Courier>show()</font> switches between them. <font name=Courier>script.js</font> holds all logic and data: the question bank, authentication, the exam engine, the timer and the scoring/review module. <font name=Courier>style.css</font> provides the responsive layout and dark-mode theme."),
 fig("docs/diagrams/architecture.png","Figure 1: Architecture of the Online Examination System",14.5*cm),
 P("Technology stack",H2),
 tbl([["Layer","Technology","Purpose"],["Structure","HTML5","Screens, forms, modals"],["Styling","CSS3 (grid, flexbox, CSS variables, media queries)","Responsive layout, dark mode, timer warning animation"],["Logic","Vanilla JavaScript (ES6)","Auth, exam engine, timer, scoring, review"],["Storage","localStorage, sessionStorage, cookie, window.name","Saved accounts; exam state is kept in memory only"],["Testing","Python + Playwright (Chromium) with a fake clock","Automated UI tests, screenshots, timer simulation"]],[2.6*cm,7.2*cm,7.8*cm]),Spacer(1,6),
 P("Key design decisions",H2)]+bullets(["<b>Screen state machine:</b> Login, Instructions, Exam and Result, so the exam cannot be reached without passing through login (Figure 3).","<b>Randomisation:</b> a Fisher-Yates shuffle orders both the questions and the four options for every attempt; the correct answer is tracked by its text.","<b>Safe rendering:</b> question text, usernames and review lines are inserted with <font name=Courier>textContent</font>, which prevents HTML/script injection.","<b>Timer:</b> a one-second interval decrements the remaining seconds, turns red at 5 minutes and calls the submit function with an <i>auto</i> flag at zero; a <i>done</i> flag prevents double submission.","<b>Resilient account storage:</b> accounts are written to four browser stores to survive restrictive browser settings."])
S+=[fig("docs/diagrams/usecase.png","Figure 2: Use case diagram",13*cm),fig("docs/diagrams/screenflow.png","Figure 3: Screen flow / state diagram",14*cm),fig("docs/diagrams/dfd.png","Figure 4: Data flow diagram (Level 1)",14*cm),fig("docs/diagrams/datamodel.png","Figure 5: Data model as implemented",14.5*cm)]

S+=[P("4. Prototype and Screenshots",H1),
 P("The prototype is the submitted application itself (<font name=Courier>index.html</font>, <font name=Courier>script.js</font>, <font name=Courier>style.css</font>), tested without any modification. All screenshots below were captured automatically from the running application by the test suite."),
 fig("docs/screenshots/01_login.png","Figure 6: Login screen",8.5*cm),fig("docs/screenshots/02_save_modal.png","Figure 7: 'Save this account?' dialog for a new username",8.5*cm),
 fig("docs/screenshots/03_intro.png","Figure 8: Instructions screen shown only after login",12*cm),fig("docs/screenshots/05_exam.png","Figure 9: Exam screen with question, countdown timer and question navigator",14*cm),
 fig("docs/screenshots/06_exam_answered.png","Figure 10: Answered questions turn green in the navigator (TC31)",14*cm),fig("docs/screenshots/07_timer_low.png","Figure 11: Timer in warning state at 05:00 remaining (TC34)",14*cm),
 fig("docs/screenshots/09_submit_modal.png","Figure 12: Submit confirmation showing unanswered count and time left (TC38)",14*cm),fig("docs/screenshots/08_autosubmit.png","Figure 13: Automatic submission when the timer reaches 00:00 (TC36)",11*cm),
 fig("docs/screenshots/10_result_pass.png","Figure 14: Result page for a PASS (20/20, TC42)",11*cm),fig("docs/screenshots/11_result_fail.png","Figure 15: Result page for a FAIL (7/20, TC46)",11*cm),
 fig("docs/screenshots/14_mobile_exam.png","Figure 16: Responsive exam screen at 375 px width (TC61)",6*cm),fig("docs/screenshots/15_dark.png","Figure 17: Automatic dark mode (TC64)",9*cm),
 P("How to run",H2)]+bullets(["Open <font name=Courier>index.html</font> in any modern browser, or host the three files on GitHub Pages / Netlify.","To run the automated tests: <font name=Courier>pip install playwright; playwright install chromium; python tests/test_exam.py</font>."])

mods=collections.OrderedDict()
for r in R: mods.setdefault(r["module"],[]).append(r)
cnt=collections.Counter(r["type"] for r in R)
S+=[PageBreak(),P("5. Test Plan and Strategy",H1),
 tbl([["Item","Details"],["Objective","Verify requirements FR1 to FR8 and the non-functional requirements; find and document defects in the application."],["Scope","Login and account saving, access control, instructions, exam engine and question bank, navigation, answering, timer, auto-submit, submit dialog, scoring, review, session handling, security, UI, accessibility, performance."],["Out of scope","Server-side components (none exist), cross-browser matrix, real-device testing, load testing with many simultaneous users."],["Approach","Black-box testing through the real UI, fully automated with Playwright on Chromium. Each test group starts with clean browser storage."],["Time simulation","Playwright's fake clock fast-forwards the 60-minute exam, so the 05:00 warning and the auto-submit are tested in seconds without waiting an hour."],["Environment","Chromium on Linux; viewports 1100x800 and 375x760; light and dark colour schemes; the application opened as a local file."],["Entry criteria","All three source files available and the application opens without errors."],["Exit criteria","All test cases executed; every failure analysed, logged with severity and a recommended fix."],["Application changes","None. The code was tested exactly as submitted, so every failure is a genuine finding."]],[3.2*cm,14.4*cm]),Spacer(1,8),
 P("Test design techniques used",H2)]+bullets(["<b>Boundary value analysis:</b> timer at 05:00, 00:01 and 00:00; pass mark at 8/20 (40%) versus 7/20 (35%); first/last question navigation; password length.","<b>Equivalence partitioning:</b> valid, invalid and empty credentials; case sensitivity of username and password; correct, wrong and skipped answers.","<b>State-transition testing:</b> Login to Instructions to Exam to Result flow, access control and logout.","<b>Negative and security testing:</b> empty or whitespace input, XSS and SQL-injection strings, reserved names such as <font name=Courier>__proto__</font>, credential storage, answer-key exposure, reload during exam.","<b>Usability, accessibility and performance testing:</b> responsive layout, labels, keyboard access, dark mode, load time and response time."])
S+=[Spacer(1,6),tbl([["Test type","Count"]]+[[k,v] for k,v in sorted(cnt.items())]+[["<b>Total</b>",f"<b>{len(R)}</b>"]],[7*cm,3*cm])]

S+=[PageBreak(),P("6. Test Cases and Execution Results",H1),P("The columns <i>Actual</i> and <i>Status</i> show what was observed when the automated suite ran against the application. Test cases are grouped by module.")]
W=[1.1*cm,2.0*cm,3.4*cm,2.9*cm,3.2*cm,3.8*cm,1.2*cm]
for m,rs in mods.items():
    rows=[["TC ID","Type","Description","Input","Expected","Actual","Status"]]
    for r in rs:
        col="#2b9a4f" if r["status"]=="Pass" else "#d64545"
        act=esc(r["actual"]); act=act if len(act)<260 else act[:257]+"..."
        rows.append([r["id"],r["type"],esc(r["desc"]),esc(r["input"]),esc(r["expected"]),act,f'<font color="{col}"><b>{r["status"]}</b></font>'])
    S+=[P(f"Module: {m}",H2),tbl(rows,W),Spacer(1,4)]

labels=list(mods); pv=[sum(x["status"]=="Pass" for x in mods[m]) for m in labels]; fv=[len(mods[m])-pv[i] for i,m in enumerate(labels)]
f,a=plt.subplots(figsize=(8.4,3.4)); a.bar(labels,pv,color="#2b9a4f",label="Pass"); a.bar(labels,fv,bottom=pv,color="#d64545",label="Fail")
a.set_ylabel("Test cases"); a.set_title("Results by module"); a.legend(); plt.xticks(rotation=35,ha="right",fontsize=7.5); plt.tight_layout(); f.savefig("docs/diagrams/results.png",dpi=160); plt.close(f)
S+=[PageBreak(),P("7. Defect Report and Analysis",H1),
 tbl([["Executed","Passed","Failed","Pass rate"],[len(R),passed,len(failed),f"{passed/len(R)*100:.1f}%"]],[4*cm,4*cm,4*cm,4*cm]),Spacer(1,6),
 fig("docs/diagrams/results.png","Figure 18: Pass/fail by module",14.5*cm),
 P(f"The suite found <b>{len(failed)} failing test cases, which map to 6 distinct defects</b> in the application. Each failure was cross-checked against the source code to confirm it reflects real behaviour of the application and not a test error. The defects are listed in order of severity. All are currently <b>open</b> (the code was deliberately not changed) and each has a recommended fix."),
 P("Defect log",H2),
 tbl([["ID","Failed TC","Defect","Severity","Impact","Recommended fix"],
  ["DEF-01","TC53, TC54","Passwords are stored in <b>plain text</b> in localStorage, sessionStorage, a cookie and <font name=Courier>window.name</font> (e.g. {\"student1\":\"Pass@123Secret\"}).","High","Anyone with access to the browser, or any site opened later in the same tab (window.name), can read every saved password.","Never store passwords in the browser. Authenticate on a server and keep only a session token; at minimum, salt and hash. Remove the window.name and cookie copies."],
  ["DEF-02","TC55","The <b>answer key is readable</b>: typing BANK in the console shows every correct answer.","High","A student can open the developer tools and read all correct answers, defeating the purpose of the exam.","Keep questions and answers on a server; send one question at a time and check answers server-side."],
  ["DEF-03","TC60","<b>Reloading the page during an exam loses all progress</b> and logs the student out. Logging in again starts a brand-new exam with a full 60:00 timer.","High","Reload resets the clock and the answers, so time limits can be bypassed and a student can restart to retry.","Persist attempt start time, answers and question order (server-side or at least sessionStorage); compute remaining time from the saved start time."],
  ["DEF-04","TC59","<b>No password policy</b>: a one-character password is accepted when creating an account.","Medium","Weak credentials; combined with auto-creation of accounts, login does not really verify identity.","Enforce a minimum length (for example 8) and basic complexity; show clear error messages."],
  ["DEF-05","TC63","<b>Answer options cannot be selected with the keyboard</b>: they are plain div elements with no tabindex, role or key handler.","Medium","Keyboard-only and screen-reader users cannot take the exam (accessibility failure).","Use radio inputs or buttons (or add role='radio', tabindex and Enter/Space handlers)."],
  ["DEF-06","TC62","The username and password inputs are <b>not linked to their labels</b> (labels have no <font name=Courier>for</font> attribute).","Low","Clicking a label does not focus the field and screen readers do not announce the field names.","Add for/id pairs or wrap inputs inside labels."]],
  [1.4*cm,1.5*cm,4.6*cm,1.4*cm,4.3*cm,4.4*cm]),
 Spacer(1,8),P("Additional observations from testing and code review",H2)]+bullets([
 "<b>No Logout button on the exam screen.</b> The logout confirmation (\"Your exam progress will be lost\") exists in code but cannot be reached from the UI during an exam; it was verified by calling <font name=Courier>logout()</font> directly (TC52). This may be intentional, but the dead code should either be exposed or removed.",
 "<b>Unknown usernames create an account automatically.</b> Entering any new username and password offers to save it, so anyone can register; the login is not an identity check. A real system needs registration and server-side verification.",
 "<b>Unlimited attempts.</b> There is no limit on the number of attempts per student; combined with DEF-03 a student can restart at will.",
 "<b>Timer relies on a one-second interval.</b> The countdown decrements a counter each tick instead of comparing with the wall-clock start time, so a throttled background tab or a sleeping device can make the exam last longer than 60 minutes. Saving the start timestamp (see DEF-03) fixes this too.",
 "<b>Cookie storage could not be verified.</b> Browsers do not store cookies for local files, so TC53-54 covered localStorage and window.name; the cookie copy should be re-checked when the app is hosted."])
S+=[Spacer(1,6),P("What worked well",H2)]+bullets(["Access control, validation messages, login rules (case handling) and the three-screen flow all behaved correctly.","Timer, warning state and auto-submit were exact at the boundaries 05:00, 00:01 and 00:00.","Scoring was correct at every boundary (0, 7, 8 and 20 correct) and counts always summed to 20.","Randomisation, review output, XSS-safe rendering, resistance to SQL-injection-style input and reserved names, responsive layout, dark mode and performance all passed."])

S+=[P("8. Limitations, Conclusion and Future Scope",H1),P("Limitations of this testing",H2)]+bullets(["Black-box UI testing on Chromium only; Firefox, Safari and real mobile devices were not tested.","Timer behaviour was verified with a simulated clock, not by waiting a real hour; background-tab throttling was assessed by code review only.","The application has no server, so network, concurrency and database testing were not applicable."])
S+=[P("Conclusion",H2),P(f"The Online Examination System meets its core functional requirements: login flow, 60-minute timer, auto-submit, navigation, scoring and review all passed {passed} of {len(R)} automated test cases, including every boundary check. Testing also exposed six genuine defects, three of them high severity and all related to security and exam integrity (plain-text credentials, exposed answer key, and loss of the exam on reload), plus two accessibility problems and a missing password policy. These are typical limits of a client-only prototype, and the report gives a concrete fix for each. This shows why systematic test design matters even for an application that appears to work correctly during manual use."),
 P("Future scope",H2)]+bullets(["Add a back end (Node.js/Express or Django) with a database, hashed passwords, JWT sessions and server-side scoring.","Store the attempt start time and answers to survive reloads and enforce one attempt per student.","Admin panel to add questions, set time limits and view analytics; question randomisation from a larger bank.","AI-assisted proctoring (tab-switch and face detection) and plagiarism analytics.","Accessibility improvements, Progressive Web App support and CI that runs the Playwright suite on every commit."])
S+=[P("9. Links and Project Files",H1),tbl([["Item","Link / file"],["GitHub repository","[Paste your GitHub repository link here]"],["Live prototype","[Paste your GitHub Pages / Netlify link here]"],["Application source","index.html, script.js, style.css (unchanged)"],["Automated tests","tests/test_exam.py (writes tests/results.json and docs/screenshots/)"],["Raw results","tests/results.json"],["Diagram generator","tools/diagrams.py"]],[4*cm,13.6*cm])]

doc=SimpleDocTemplate("docs/Online_Examination_System_Software_Testing_Assignment.pdf",pagesize=A4,leftMargin=1.8*cm,rightMargin=1.8*cm,topMargin=1.6*cm,bottomMargin=1.8*cm,title="Online Examination System - Software Testing Assignment (Unit 5)",author="Student")
doc.build(S,onFirstPage=lambda c,d:None,onLaterPages=footer); print("built")
