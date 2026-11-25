import os; os.makedirs("docs/diagrams",exist_ok=True)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, FancyArrowPatch
P="#3b5bdb"; L="#e7ecff"; G="#e6f6ea"; O="#fff3e0"; GR="#2b9a4f"; OR="#e08a00"
def fig(w=10,h=6):
    f,a=plt.subplots(figsize=(w,h)); a.set_xlim(0,w*10); a.set_ylim(0,h*10); a.axis("off"); return f,a
def box(a,x,y,w,h,t,fc=L,ec=P,fs=9,bold=False):
    a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.4,rounding_size=2",fc=fc,ec=ec,lw=1.5))
    a.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,fontweight="bold" if bold else "normal")
def arr(a,p,q,t=None,both=False,fs=8,off=(0,1.3)):
    a.add_patch(FancyArrowPatch(p,q,arrowstyle="<|-|>" if both else "-|>",mutation_scale=13,color="#444",lw=1.3))
    if t: a.text((p[0]+q[0])/2+off[0],(p[1]+q[1])/2+off[1],t,ha="center",fontsize=fs,bbox=dict(fc="white",ec="none",pad=0.5))
def save(f,n): f.savefig(f"docs/diagrams/{n}.png",dpi=160,bbox_inches="tight"); plt.close(f)

# Architecture
f,a=fig(10,6.6); a.text(50,64,"Online Examination System - Client-side Architecture",ha="center",fontsize=13,fontweight="bold")
box(a,3,44,94,16,"",fc="#f8f9ff"); a.text(5,57,"PRESENTATION  (index.html + style.css)",fontsize=9,color=P,fontweight="bold")
for i,t in enumerate(["Login\nscreen","Instructions\nscreen","Exam screen\n(question, timer,\nnavigator)","Result +\nAnswer review","Modals\n(save / submit)"]): box(a,6+i*18,45.5,16,9,t,fs=8)
box(a,3,22,94,18,"",fc="#f8fff9",ec=GR); a.text(5,37,"APPLICATION LOGIC  (script.js)",fontsize=9,color=GR,fontweight="bold")
for i,t in enumerate(["Auth\n(login / save\naccount)","Exam engine\n(shuffle, 20 MCQs,\nnavigation)","Timer\n(60:00 countdown,\nauto-submit)","Scoring &\nreview\n(40% pass)","Screen\ncontrol\nshow()"]): box(a,6+i*18,23.5,16,10,t,fc=G,ec=GR,fs=8)
box(a,3,3,94,15,"",fc="#fffaf2",ec=OR); a.text(5,15,"DATA",fontsize=9,color=OR,fontweight="bold")
box(a,6,5,40,7,"Question bank: BANK[20] in script.js\n(question, correct, 3 wrong options)",fc=O,ec=OR,fs=8)
box(a,52,5,43,7,"User accounts: localStorage, sessionStorage,\ncookie, window.name   |   Exam state: in memory",fc=O,ec=OR,fs=8)
arr(a,(50,44),(50,40),both=True); arr(a,(50,22),(50,18),both=True)
save(f,"architecture")

# Use case
f,a=fig(10,6.4); a.text(50,62,"Use Case Diagram",ha="center",fontsize=13,fontweight="bold")
a.add_patch(FancyBboxPatch((25,3),52,55,boxstyle="round,pad=0.4",fc="#fbfcff",ec=P,lw=1.5)); a.text(51,55,"Online Examination System",ha="center",fontweight="bold",color=P)
ucs=["Login / save account","Read instructions","Start exam","Answer question","Navigate questions","Clear answer","Submit exam","View result","Review answers","Logout"]
pos=[]
for i,u in enumerate(ucs):
    x=39 if i%2==0 else 64; y=49-(i//2)*9.3
    a.add_patch(Ellipse((x,y),22,7.2,fc=L,ec=P)); a.text(x,y,u,ha="center",va="center",fontsize=8); pos.append((x,y))
a.text(8,32,"O",fontsize=22,ha="center"); a.plot([8,8],[28,22],"k",lw=1.5); a.plot([4,12],[26,26],"k",lw=1.5); a.plot([8,4],[22,16],"k",lw=1.5); a.plot([8,12],[22,16],"k",lw=1.5); a.text(8,11,"Student",ha="center",fontweight="bold")
for x,y in pos: a.plot([12,x-11],[26,y],color="#888",lw=0.8)
a.add_patch(Ellipse((90,30),16,10,fc=O,ec=OR)); a.text(90,30,"Timer\n(auto-submit)",ha="center",va="center",fontsize=8)
a.plot([82,50],[28,21.1],color=OR,lw=1.2,ls="--"); a.text(90,22,"System actor",ha="center",fontsize=7.5)
save(f,"usecase")

# Screen flow
f,a=fig(10,4.6); a.text(50,44,"Screen Flow / State Diagram",ha="center",fontsize=13,fontweight="bold")
for x,t in [(2,"LOGIN"),(27,"INSTRUCTIONS"),(52,"EXAM"),(77,"RESULT")]: box(a,x,17,19,10,t,fs=9.5,bold=True)
arr(a,(21.8,22),(26.6,22)); arr(a,(46.8,22),(51.6,22)); arr(a,(71.8,22),(76.6,22)); a.text(24,30.5,"valid /\nsaved",ha="center",fontsize=7.5); a.text(49,30.5,"Start",ha="center",fontsize=7.5); a.text(74,30.5,"Submit or\n60:00",ha="center",fontsize=7.5)
a.add_patch(FancyArrowPatch((87,17),(12,17),connectionstyle="arc3,rad=-0.35",arrowstyle="-|>",mutation_scale=13,color="#444",lw=1.3)); a.text(50,5.5,"Logout (from Result)",ha="center",fontsize=8)
a.add_patch(FancyArrowPatch((37,17),(10,17),connectionstyle="arc3,rad=-0.5",arrowstyle="-|>",mutation_scale=13,color="#888",lw=1.1)); a.text(23,9.2,"Logout (from Instructions)",ha="center",fontsize=7.5)
a.text(61.5,35.5,"timer 60:00, 20 questions, navigate / answer / clear",ha="center",fontsize=8,color="#444")
save(f,"screenflow")

# DFD
f,a=fig(10,5.4); a.text(50,52,"Data Flow Diagram (Level 1)",ha="center",fontsize=13,fontweight="bold")
box(a,2,22,14,10,"Student",fc="white",ec="#222",bold=True)
for t,y in [("1.0\nAuthenticate",40),("2.0\nConduct exam\n(timer, answers)",22),("3.0\nEvaluate &\nreview",4)]:
    a.add_patch(Ellipse((42,y+5),24,11,fc=L,ec=P)); a.text(42,y+5,t,ha="center",va="center",fontsize=8.5)
box(a,72,38,24,9,"D1  User accounts",fc=O,ec=OR); box(a,72,19,24,9,"D2  Question bank",fc=O,ec=OR); box(a,72,2,24,9,"D3  Attempt (memory)",fc=O,ec=OR)
arr(a,(16,29),(30,44),"username, password",fs=7.5,off=(-4,2)); arr(a,(54,45),(72,43),"verify / save",fs=7.5,both=True)
arr(a,(16,27),(30,27),"answers",fs=7.5); arr(a,(54,27),(72,24),"load questions",fs=7.5,off=(0,2.5))
arr(a,(54,12),(72,8),"answers",fs=7.5,off=(0,-2.5),both=True); arr(a,(30,9),(16,23),"score, review",fs=7.5,off=(-1,-2))
save(f,"dfd")

# Data model
f,a=fig(10,5)
a.text(50,47,"Data Model (as implemented)",ha="center",fontsize=13,fontweight="bold")
def ent(x,t,fields,w=29):
    a.add_patch(FancyBboxPatch((x,3),w,35,boxstyle="round,pad=0.3",fc="white",ec=P,lw=1.8))
    a.add_patch(FancyBboxPatch((x,32),w,6,boxstyle="round,pad=0.3",fc=P,ec=P)); a.text(x+w/2,35,t,color="white",ha="center",va="center",fontweight="bold",fontsize=9)
    for i,fl in enumerate(fields): a.text(x+1.5,28-i*4.2,fl,fontsize=8)
ent(1,"USER (stored)",["PK  username (lower-case)","password (plain text)","","Stored in localStorage /","sessionStorage / cookie /","window.name"])
ent(36,"QUESTION (BANK)",["text","correct answer","wrong option 1","wrong option 2","wrong option 3","(20 questions)"])
ent(71,"ATTEMPT (memory)",["user","Q[20] shuffled","ans[20] (index/null)","current question","time left (3600 s)","result: c / w / s, %"],w=28)
arr(a,(30.5,20),(35.5,20),"takes",fs=7.5,off=(0,2)); arr(a,(65.5,20),(70.5,20),"records",fs=7.5,off=(0,2))
save(f,"datamodel")
