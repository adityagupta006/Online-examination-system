const DURATION=60*60;
// [question, correct, wrong1, wrong2, wrong3]
const BANK=[
["Which testing examines documents and code WITHOUT executing the program?","Static testing","Dynamic testing","Load testing","Stress testing"],
["Black-box testing focuses on:","Inputs and expected outputs","Internal code structure","Compiler settings","Memory addresses"],
["Re-testing after changes to make sure existing features still work is called:","Regression testing","Smoke testing","Alpha testing","Ad-hoc testing"],
["The smallest testable part of an application is tested in:","Unit testing","System testing","Acceptance testing","Integration testing"],
["For a valid input range of 1–100, which set is chosen by Boundary Value Analysis?","0, 1, 100, 101","10, 20, 30","50, 60, 70","-100, 500, 900"],
["“Are we building the product right?” describes:","Verification","Validation","Deployment","Maintenance"],
["Alpha testing is performed by:","In-house testers/staff at the developer's site","Customers at their own site","Only the compiler","Random public users online"],
["What is the first phase of the Software Testing Life Cycle (STLC)?","Requirement analysis","Test execution","Test closure","Defect retesting"],
["Which statement about defect cost is TRUE?","Defects found later in the lifecycle cost more to fix","Defects cost the same at any stage","Late defects are cheaper to fix","Cost never depends on stage"],
["Equivalence Partitioning divides input data into:","Groups expected to behave the same way","Random values","Only invalid values","Only boundary values"],
["Statement coverage and branch coverage are examples of:","White-box techniques","Black-box techniques","Usability tests","Security audits"],
["Checking how a system behaves under heavy user load is:","Performance/Load testing","Unit testing","Smoke testing","Static review"],
["Smoke testing is done to:","Check that a new build is stable enough for further testing","Find every possible bug","Measure code size","Test only the database"],
["A test case typically contains:","ID, steps, test data and expected result","Only the bug count","Only source code","Only the release date"],
["Integration testing verifies:","Interaction between combined modules","A single function alone","Only the UI colours","Only hardware"],
["User Acceptance Testing (UAT) is performed by:","End users / clients","Compiler","Only developers","Only DBAs"],
["In the bug life cycle, a newly reported defect is in which state?","New","Closed","Reopened","Deferred"],
["Which of these is a NON-functional test?","Usability testing","Login validation test","Form submit test","Search result test"],
["Exploratory testing means:","Simultaneous learning, test design and execution","Executing only scripted tests","Testing without any tester","Reviewing only documents"],
["Decision (branch) coverage ensures that:","Every decision outcome (true and false) is executed","Every line is typed","Every user logs in","Every variable is renamed"]
];
const $=id=>document.getElementById(id),show=id=>{["login","intro","exam","res"].forEach(s=>$(s).classList.toggle("hide",s!==id));window.scrollTo(0,0)};
let user=null,Q=[],ans=[],cur=0,left=0,tick=null,done=false;
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]]}return a};
const fmt=s=>String(s/60|0).padStart(2,"0")+":"+String(s%60).padStart(2,"0");

// Req 1: valid username & password (accounts are stored in this browser)
let USERS={},pending=null,persistent=true;
const KEY="examUsers";
// Load accounts from every place they might have been saved
function loadUsers(){
  let out={};
  const merge=t=>{try{const o=JSON.parse(t);if(o&&typeof o==="object")Object.assign(out,o)}catch(e){}};
  try{merge(localStorage.getItem(KEY))}catch(e){}
  try{merge(sessionStorage.getItem(KEY))}catch(e){}
  try{const m=document.cookie.match(new RegExp("(?:^|; )"+KEY+"=([^;]*)"));if(m)merge(decodeURIComponent(m[1]))}catch(e){}
  try{if(window.name.indexOf(KEY+"=")===0)merge(window.name.slice(KEY.length+1))}catch(e){}
  return out;
}
// Save accounts to as many places as possible; returns true if at least one permanent place worked
function saveUsers(){
  const t=JSON.stringify(USERS);let ok=false;
  try{localStorage.setItem(KEY,t);ok=localStorage.getItem(KEY)===t}catch(e){}
  try{sessionStorage.setItem(KEY,t)}catch(e){}
  try{document.cookie=KEY+"="+encodeURIComponent(t)+"; max-age=31536000; path=/; SameSite=Lax";if(document.cookie.indexOf(KEY+"=")>-1)ok=true}catch(e){}
  try{window.name=KEY+"="+t}catch(e){}
  return ok;
}
USERS=loadUsers();
function enter(u){user={n:u};$("lerr").textContent="";$("name").textContent=u;$("u").value=$("pw").value="";show("intro")}
function login(){
  const u=$("u").value.trim().toLowerCase(),p=$("pw").value;
  if(!u||!p){$("lerr").textContent="Please enter username and password.";return}
  if(Object.prototype.hasOwnProperty.call(USERS,u)){
    if(USERS[u]===p)enter(u);else $("lerr").textContent="Incorrect password for this username."
  }else{
    pending={u,p};$("sat").textContent="No account found for \""+u+"\". Do you want to save it and log in?";$("sm").classList.remove("hide")
  }
}
$("syes").onclick=()=>{if(!pending)return;USERS[pending.u]=pending.p;persistent=saveUsers();$("sm").classList.add("hide");const u=pending.u;pending=null;enter(u);if(!persistent)alert("Account saved for this session only. Your browser is blocking permanent storage, so open the page through a local server (e.g. VS Code Live Server) or a different browser to keep accounts after closing it.")};
$("sno").onclick=()=>{pending=null;$("sm").classList.add("hide");$("pw").value="";$("lerr").textContent="Account was not saved. Enter a saved username to login."};
function logout(){
  if(!$("exam").classList.contains("hide")&&!done&&!confirm("Logout now? Your exam progress will be lost."))return;
  clearInterval(tick);user=null;done=false;show("login")
}
$("lbtn").onclick=login;$("pw").addEventListener("keydown",e=>{if(e.key==="Enter")login()});$("u").addEventListener("keydown",e=>{if(e.key==="Enter")$("pw").focus()});
$("out").onclick=$("rout").onclick=logout;

// Req 2,3,4: start only after login; 60 min; 20 MCQs
$("start").onclick=()=>{
  if(!user){show("login");return}
  Q=shuffle(BANK).slice(0,20).map(r=>({q:r[0],o:shuffle(r.slice(1)),c:r[1]}));
  ans=Array(20).fill(null);cur=0;left=DURATION;done=false;
  $("who").textContent=user.n;show("exam");render();
  clearInterval(tick);
  tick=setInterval(()=>{left--;paintTimer();if(left<=0)finish(true)},1000);paintTimer();
};
function paintTimer(){const t=$("timer");t.textContent=fmt(Math.max(left,0));t.classList.toggle("low",left<=300)}

// Req 5: navigation between questions
function render(){
  const q=Q[cur];
  $("qn").textContent=`Question ${cur+1} of 20`;$("qt").textContent=q.q;
  $("opts").innerHTML="";
  q.o.forEach((t,i)=>{const d=document.createElement("div");d.className="opt"+(ans[cur]===i?" sel":"");
    d.innerHTML=`<b>${"ABCD"[i]}</b><span></span>`;d.lastChild.textContent=t;
    d.onclick=()=>{ans[cur]=i;render()};$("opts").appendChild(d)});
  $("prev").disabled=cur===0;$("next").disabled=cur===19;
  $("prog").textContent=`${ans.filter(a=>a!==null).length}/20 answered`;
  $("pal").innerHTML="";
  Q.forEach((_,i)=>{const b=document.createElement("button");b.textContent=i+1;
    b.className=(ans[i]!==null?"ans ":"")+(i===cur?"cur":"");b.onclick=()=>{cur=i;render()};$("pal").appendChild(b)});
}
$("prev").onclick=()=>{if(cur>0){cur--;render()}};
$("next").onclick=()=>{if(cur<19){cur++;render()}};
$("clr").onclick=()=>{ans[cur]=null;render()};

// Req 6: manual submit before time expires
$("sub").onclick=()=>{
  const un=ans.filter(a=>a===null).length;
  $("cmt").textContent=un?`You have ${un} unanswered question(s). Time left: ${fmt(left)}.`:`All questions answered. Time left: ${fmt(left)}.`;
  $("cm").classList.remove("hide")};
$("cno").onclick=()=>$("cm").classList.add("hide");
$("cyes").onclick=()=>finish(false);

// Req 7: auto-submit at 60 min  |  Req 8: result after submission
function finish(auto){
  if(done)return;done=true;clearInterval(tick);$("cm").classList.add("hide");
  let c=0,w=0,s=0;
  Q.forEach((q,i)=>{if(ans[i]===null)s++;else if(q.o[ans[i]]===q.c)c++;else w++});
  const pct=Math.round(c/20*100),pass=pct>=40;
  $("rmsg").textContent=auto?"⏰ Time is up — your exam was submitted automatically.":"✅ Exam submitted successfully.";
  $("rs").textContent=`${c} / 20`;
  $("rb").textContent=pass?"PASS":"FAIL";$("rb").style.background=pass?"var(--ok)":"var(--bad)";
  $("rc").textContent=c;$("rw").textContent=w;$("ru").textContent=s;$("rp").textContent=pct+"%";
  $("rt").textContent=`Time taken: ${fmt(DURATION-Math.max(left,0))} · Passing mark: 40%`;
  $("rev").innerHTML="";
  Q.forEach((q,i)=>{const d=document.createElement("div"),a=ans[i],ok=a!==null&&q.o[a]===q.c;
    d.className="rv "+(a===null?"s":ok?"c":"w");
    const h=document.createElement("b");h.textContent=`Q${i+1}. ${q.q}`;d.appendChild(h);
    const y=document.createElement("div");y.className="tag "+(ok?"ok":"no");
    y.textContent="Your answer: "+(a===null?"Not answered":q.o[a]);d.appendChild(y);
    if(!ok){const g=document.createElement("div");g.className="tag ok";g.textContent="Correct answer: "+q.c;d.appendChild(g)}
    $("rev").appendChild(d)});
  show("res");
}