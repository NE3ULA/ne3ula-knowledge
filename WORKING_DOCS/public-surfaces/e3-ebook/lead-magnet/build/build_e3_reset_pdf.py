from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, HRFlowable, Flowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
ASSET_DIR = PACKAGE_ROOT / "visual-assets"
OUT = PACKAGE_ROOT / "release/v1/THE_E3_RESET_LEAD_MAGNET_V1.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE = (6*inch, 9*inch)
W, H = PAGE
PAPER = colors.HexColor("#FBF9F5")
INK = colors.HexColor("#17131F")
DARK = colors.HexColor("#0A0812")
MUTED = colors.HexColor("#766E82")
VIOLET = colors.HexColor("#9857FF")
CYAN = colors.HexColor("#25D9D0")
GOLD = colors.HexColor("#D8A63B")
PINK = colors.HexColor("#F26B9B")
LAV = colors.HexColor("#B8AEC7")
LINE = colors.HexColor("#DED7E5")

pdfmetrics.registerFont(TTFont("NE3ULA", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("NE3ULA-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Kicker", fontName="NE3ULA-Bold", fontSize=8, leading=10,
    textColor=VIOLET, spaceAfter=9, tracking=2))
styles.add(ParagraphStyle(name="H1x", fontName="NE3ULA-Bold", fontSize=24, leading=27,
    textColor=INK, spaceAfter=12))
styles.add(ParagraphStyle(name="H2x", fontName="NE3ULA-Bold", fontSize=15, leading=18,
    textColor=INK, spaceBefore=5, spaceAfter=7))
styles.add(ParagraphStyle(name="H3x", fontName="NE3ULA-Bold", fontSize=10, leading=13,
    textColor=INK, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="Bodyx", fontName="NE3ULA", fontSize=9.25, leading=13.4,
    textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", fontName="NE3ULA", fontSize=7.5, leading=10.5,
    textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="Prompt", fontName="NE3ULA-Bold", fontSize=8.5, leading=11.5,
    textColor=INK, spaceBefore=6, spaceAfter=3))
styles.add(ParagraphStyle(name="Quote", fontName="NE3ULA-Bold", fontSize=12, leading=16,
    textColor=INK, leftIndent=16, rightIndent=12, borderColor=GOLD, borderWidth=0,
    borderPadding=10, spaceBefore=8, spaceAfter=10))
styles.add(ParagraphStyle(name="Bulletx", parent=styles["Bodyx"], leftIndent=13,
    firstLineIndent=-8, bulletIndent=2, spaceAfter=4))
styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Small"], alignment=TA_CENTER))


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def line_space(n=2, width=1):
    out=[]
    for _ in range(n):
        out += [Spacer(1, 10), HRFlowable(width="100%", thickness=width, color=LINE)]
    return out


class AccentQuote(Flowable):
    def __init__(self, text):
        super().__init__(); self.text=text; self.height=64
    def wrap(self, aw, ah): self.width=aw; return aw, self.height
    def draw(self):
        c=self.canv
        c.setFillColor(colors.HexColor("#F1EBF8")); c.roundRect(0,0,self.width,self.height,10,fill=1,stroke=0)
        c.setFillColor(GOLD); c.roundRect(0,0,5,self.height,2,fill=1,stroke=0)
        para=Paragraph(self.text, styles["Quote"])
        w,h=para.wrap(self.width-26,self.height-12); para.drawOn(c,14,(self.height-h)/2)


def orbit(c, x, y, r=22):
    c.saveState(); c.setLineWidth(1.2)
    for col, dx, dy, rr in [(VIOLET,0,0,r),(CYAN,4,-2,r*.72),(GOLD,-5,4,r*.42)]:
        c.setStrokeColor(col); c.ellipse(x-rr+dx,y-rr+dy,x+rr+dx,y+rr+dy,stroke=1,fill=0)
    c.setFillColor(PINK); c.circle(x+r*.55,y+r*.45,2,fill=1,stroke=0); c.restoreState()


def footer(c, doc):
    c.saveState(); c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(LINE); c.line(.62*inch,H-.47*inch,W-.62*inch,H-.47*inch)
    c.setFont("NE3ULA-Bold",6.5); c.setFillColor(VIOLET); c.drawString(.62*inch,H-.35*inch,"NE3ULA  /  E3 RESET")
    orbit(c,W-.69*inch,H-.29*inch,8)
    c.setFont("NE3ULA",6.5); c.setFillColor(MUTED); c.drawCentredString(W/2,.34*inch,str(doc.page))
    c.restoreState()


class Doc(BaseDocTemplate):
    pass


doc=Doc(str(OUT), pagesize=PAGE, leftMargin=.65*inch, rightMargin=.65*inch,
        topMargin=.68*inch, bottomMargin=.52*inch, title="The E3 Reset",
        author="NE3ULA", subject="A 10-Minute E3 Practice")
frame=Frame(doc.leftMargin,doc.bottomMargin,W-doc.leftMargin-doc.rightMargin,
            H-doc.topMargin-doc.bottomMargin,id="main")
doc.addPageTemplates(PageTemplate(id="paper",frames=[frame],onPage=footer))

S=[]

def new(title, kicker=None, subtitle=None):
    if kicker: S.append(p(kicker.upper(),"Kicker"))
    S.append(p(title,"H1x"))
    if subtitle: S.append(p(subtitle,"Small"))
    S.append(HRFlowable(width="100%",thickness=1,color=LINE,spaceAfter=12))

def pb(): S.append(PageBreak())
def bullets(items):
    for item in items: S.append(p("• &nbsp;"+item,"Bulletx"))

# Cover (canvas flowable occupying the frame)
class Cover(Flowable):
    def wrap(self,aw,ah): self.width=aw; self.height=ah; return aw,ah
    def draw(self):
        c=self.canv; c.saveState(); c.resetTransforms()
        c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setStrokeColor(colors.HexColor("#2D233A")); c.setLineWidth(.8)
        c.ellipse(W*.39-170,H*.55-170,W*.39+170,H*.55+170,stroke=1,fill=0)
        for col,off,rad in [(VIOLET,0,128),(CYAN,24,92),(GOLD,-17,57)]:
            c.setStrokeColor(col); c.setLineWidth(1.6); c.ellipse(W*.76-rad+off,H*.72-rad,W*.76+rad+off,H*.72+rad,stroke=1,fill=0)
        c.setFillColor(PINK); c.circle(W*.88,H*.84,4,fill=1,stroke=0)
        c.setFont("NE3ULA-Bold",8); c.setFillColor(VIOLET); c.drawString(.7*inch,H-.72*inch,"NE3ULA  /  E3")
        c.setFont("NE3ULA-Bold",38); c.setFillColor(colors.white); c.drawString(.55*inch,H-2.15*inch,"THE E3")
        c.setFillColor(GOLD); c.drawString(.55*inch,H-2.72*inch,"RESET")
        c.setStrokeColor(CYAN); c.setLineWidth(2); c.line(.55*inch,H-2.94*inch,2.18*inch,H-2.94*inch)
        para=Paragraph("A 10-Minute Practice to Read Your Energy,<br/>Return to Yourself, and Choose What Comes Next",
            ParagraphStyle("cover-sub",fontName="NE3ULA",fontSize=11,leading=16,textColor=colors.white))
        para.wrapOn(c,3.35*inch,.7*inch); para.drawOn(c,.55*inch,H-3.92*inch)
        c.setFont("NE3ULA-Bold",8); c.setFillColor(LAV); c.drawString(.7*inch,.72*inch,"A PRACTICAL ENTRY INTO WE ARE ALCHEMY")
        c.restoreState()

S += [Cover(), PageBreak()]

new("Change Is Already Happening","Begin here")
for t in ["You are changing.","Every experience leaves something behind. Every choice strengthens a pattern. Every repeated thought, action, and response participates in the person you are becoming.","Some of that formation is conscious. Much of it is not.","The question is not whether you are changing.","<b>The question is whether you are participating in that change.</b>","The E3 Reset is a brief practice for moments when you feel scattered, depleted, uncertain, stuck, or pulled away from yourself. It will not redesign your entire life in ten minutes. It will help you read what is happening, return to an authored center, and choose one action that can enter reality.","You do not need perfect clarity before you begin. You need enough honesty to notice what is here."]:
    S.append(p(t))
S.append(AccentQuote("The practice is not to remain perfectly aligned. The practice is to notice, learn, choose, and return with greater awareness.")); pb()

new("Before You Begin","Choose one living edge")
S.append(p("Choose one real situation. It may be:"))
bullets(["a decision you keep postponing","a repeated pattern you are beginning to notice","a responsibility that feels heavier than it should","a relationship asking for attention","a creative impulse that keeps returning","a change in energy you do not yet understand","a next step that matters but remains unclear"])
S.append(p("Do not choose your whole life. <b>Choose one living edge.</b>"))
S.append(p("The situation I am bringing into this practice is:","Prompt")); S += line_space(3)
S.append(Spacer(1,12)); S.append(p("Take one breath before continuing. The goal is not to judge the situation. The goal is to read it accurately enough to move.","Small")); pb()

new("Why Forcing Yourself Often Fails","Read the instrument")
for t in ["Every choice is made through an instrument. <b>That instrument is you.</b>","Your body carries a level of energy. Your mind carries a level of clarity. Your emotional life carries movement and unfinished material. Your relationships can steady, drain, challenge, or restore you. Your sense of purpose can give effort direction—or leave action feeling empty even when the work is getting done.","These conditions affect what is available now. They do not tell the whole truth about who you are.","A depleted person may interpret necessary rest as failure. An overloaded mind may treat every decision as equally urgent. An emotionally flooded person may call reaction intuition. A lonely person may accept what violates their values because connection feels more necessary than discernment.","Action without state awareness easily becomes conflict with the self."]:
    S.append(p(t))
S.append(AccentQuote("Hear the instrument before trying to force the performance."))
S.append(p("Accuracy comes before adjustment. You cannot tune an instrument you refuse to hear.")); pb()

new("The Human Battery","Read available capacity")
S.append(p("The Human Battery is a practical way to read available capacity. It is not a medical diagnosis, a judgment of worth, or a demand to remain fully charged. It is a check across five dimensions that continually influence one another."))
for h,t in [("Physical","Sleep, nourishment, movement, pain, health, recovery, and the body's current level of demand."),("Mental","Attention, clarity, cognitive load, stimulation, decision fatigue, and unfinished loops competing for awareness."),("Emotional","Feelings moving through you, the effort required to regulate them, and what has not yet been processed or expressed."),("Social","Connection, belonging, boundaries, conflict, care, loneliness, visibility, and relational demand."),("Purpose","Meaning, direction, contribution, and connection to what matters beyond immediate maintenance.")]:
    S.append(p(h,"H3x")); S.append(p(t,"Small"))
S.append(p("<b>Read the pattern, not only the total.</b> The purpose is not a perfect score. It is to make the next adjustment more intelligent.")); pb()

class FullImage(Flowable):
    def __init__(self,path,label): self.path=Path(path); self.label=label
    def wrap(self,aw,ah): self.width=aw; self.height=ah; return aw,ah
    def draw(self):
        c=self.canv; c.saveState(); c.resetTransforms()
        c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
        im=PILImage.open(self.path).convert("RGB")
        iw,ih=im.size
        # Center the entire approved plate in true page coordinates. Never crop it.
        maxw=W-.28*inch; maxh=H-.28*inch; scale=min(maxw/iw,maxh/ih)
        dw,dh=iw*scale,ih*scale
        c.drawImage(ImageReader(im), (W-dw)/2, (H-dh)/2, dw, dh, preserveAspectRatio=True, mask='auto')
        c.restoreState()

S += [FullImage(ASSET_DIR / "human-battery-reference.png","Human Battery"),PageBreak()]

new("Your Five-Dimension Scan","Present reading")
S.append(p("Rate what feels available <b>right now</b>, using a 1–5 scale. This is a present reading—not a verdict about you."))
data=[["DIMENSION","1","2","3","4","5"],*[ [d,"○","○","○","○","○"] for d in ["Physical","Mental","Emotional","Social","Purpose"]]]
t=Table(data,colWidths=[1.55*inch]+[.48*inch]*5,rowHeights=[.33*inch]+[.39*inch]*5)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),INK),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"NE3ULA-Bold"),("FONTNAME",(0,1),(0,-1),"NE3ULA-Bold"),("FONTNAME",(1,1),(-1,-1),"NE3ULA"),("FONTSIZE",(0,0),(-1,-1),8),("ALIGN",(1,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("GRID",(0,0),(-1,-1),.5,LINE),("BACKGROUND",(0,1),(-1,-1),colors.white)])); S.append(t)
for q in ["Which dimension is asking for attention?","Which dimension remains available and may support the others?","What condition have I been treating as an identity problem?"]:
    S.append(p(q,"Prompt")); S += line_space(1)
S.append(Spacer(1,5)); S.append(AccentQuote("State is not identity. Your state matters because it shapes what kind of next move is honest and available.")); pb()

S += [FullImage(ASSET_DIR / "e3-practice-loop-diagram.png","E3 Practice Loop"),PageBreak()]

new("1. Reveal — What Is Happening?","The E3 practice")
S.append(p("Begin with observation before explanation. Notice the facts, the signals in your body, the pressure in your thoughts, the emotional tone, the relational field, and the pattern that may be repeating."))
S.append(p("Avoid turning the present condition into a final statement about your identity."))
for q,n in [("What is happening:",2),("What I notice in my body or energy:",1),("The pattern, friction, or opportunity I can see:",1),("What keeps asking for my attention:",1)]:
    S.append(p(q,"Prompt")); S += line_space(n)
S.append(p("Reveal does not require you to solve anything yet. Let what is present become visible.","Small")); pb()

new("2. Interpret — What Does It Show Me?","The E3 practice")
S.append(p("Interpretation gives experience meaning, but the first story your mind produces is not always the most accurate one."))
bullets(["Is this a capacity problem, an identity conflict, or both?","Is the difficulty meaningful effort or avoidable depletion?","Is an inherited script shaping what I believe I must do?","Is a boundary, need, truth, or value asking to be recognized?","Am I reacting to the present—or to what the present resembles?"])
for q in ["The story I have been telling is:","Another interpretation that may be more complete is:","What the situation appears to be asking from me is:"]:
    S.append(p(q,"Prompt")); S += line_space(1)
S.append(p("No one interpretation is the whole. Choose the one that creates greater honesty, responsibility, and room for a coherent response.","Small")); pb()

new("3. Align — Who Am I Choosing to Be?","The E3 practice")
S.append(p("Alignment returns the situation to identity—not inherited identity, temporary state, or performance, but the person you are consciously choosing to become."))
S.append(p("Authorship does not mean controlling every outcome. It means meaningful participation in how you meet what is here."))
bullets(["What matters here?","What value deserves expression?","What would be honest without becoming cruel?","What would be courageous without becoming reckless?","What would respect both my limits and my direction?"])
S.append(p("I am choosing to become someone who…","H2x")); S += line_space(2)
for q in ["In this situation, that person would protect:","That person would be willing to:"]:
    S.append(p(q,"Prompt")); S += line_space(1)
S.append(p("Alignment is not a mood. It is a chosen center from which action becomes more coherent.","Small")); pb()

new("4. Act — What Is the Next Meaningful Move?","The E3 practice")
S.append(p("The next action does not need to finish the journey. It needs to enter reality."))
bullets(["send the message or ask for help","protect one hour or remove one unnecessary input","eat, rest, move, or take medication","make one decision or tell one honest truth","create the first visible piece","reduce the scope while preserving direction"])
for q in ["What matters now?","What comes next?"]:
    S.append(p(q,"Prompt")); S += line_space(1)
S.append(p("Within the next 24 hours, I will…","H2x")); S += line_space(2)
row=Table([[p("<b>When:</b> ____________________","Small"),p("<b>Where:</b> ____________________","Small")]],colWidths=[2.25*inch]*2); S.append(row)
S.append(p("First visible step:","Prompt")); S += line_space(1)
S.append(p("Make it small enough to enter reality and meaningful enough to create evidence.","Small")); pb()

new("Reduce Friction with One LifeMod","Design the conditions")
S.append(p("Sometimes the person does not need more pressure. <b>The system needs a better design.</b> A LifeMod is a deliberate change to the conditions around an action."))
data=[["TYPE","EXAMPLE"],["Environment","Put the needed tool in reach; remove a recurring distraction."],["Boundary","Protect a specific hour; decline one competing demand."],["Scope","Reduce the task to the smallest useful version."],["Rhythm","Attach the action to an existing routine or time."],["Support","Ask for information, help, accountability, or care."],["Framing","Replace “finish everything” with “create the next evidence.”"]]
t=Table(data,colWidths=[1.05*inch,3.45*inch],repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),INK),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,0),(-1,0),"NE3ULA-Bold"),("FONTNAME",(0,1),(0,-1),"NE3ULA-Bold"),("FONTNAME",(1,1),(-1,-1),"NE3ULA"),("FONTSIZE",(0,0),(-1,-1),7),("LEADING",(0,0),(-1,-1),9),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("GRID",(0,0),(-1,-1),.5,LINE),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor('#F5F1F7')]),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)])); S.append(t)
for q in ["The friction I can modify is:","The LifeMod I will make is:","I will put it in place by:"]:
    S.append(p(q,"Prompt")); S += line_space(1)
pb()

new("5. Integrate — What Will I Learn?","The E3 practice")
S.append(p("Action produces information. Integration is how you return to learn from it without turning the result into a judgment of your worth."))
S.append(p("I will review this action on:","Prompt")); S += line_space(1)
for h,t in [("Retain","What supported the action and should remain?"),("Revise","What did reality show me that requires adjustment?"),("Release","What assumption, condition, demand, or method no longer belongs?"),("Repeat","What useful action deserves another repetition?")]:
    S.append(p(h,"H3x")); S.append(p(t,"Small"))
S.append(p("You are not trying to prove that your first choice was perfect. You are building a more intelligent relationship with action, consequence, and return."))
S.append(AccentQuote("Mastery is not never losing the path. Mastery is learning how to find your way back.")); pb()

new("Your E3 Reset","One-page practice")
for h,q in [("Situation","What situation am I bringing into this practice?"),("Reveal","What is happening? What pattern, signal, friction, or opportunity is present?"),("Interpret","What may this be showing me? What story needs a wider reading?"),("Align","Who am I choosing to become in relationship to this?"),("Act","What is the next meaningful action I will take within 24 hours?"),("LifeMod","What condition will I change to support the action?"),("Integrate","When will I return, and what will I retain, revise, release, or repeat?")]:
    S.append(p(h,"H3x")); S.append(p(q,"Small")); S += line_space(1)
pb()

new("Return Is Part of the Practice","Continue")
for t in ["The reset is not complete because the page is filled. <b>It becomes complete when the first action enters your life.</b>","You may drift. Your energy will change. A new condition may reveal an old pattern. Reality may show that the action needs to be smaller, stronger, kinder, more honest, or entirely different.","This does not mean the process failed. It means life has provided new material.","<b>Return.</b>","Read what changed. Choose again.","Over time, return becomes a capacity. Reflection becomes more honest. Action becomes more precise. Repetition begins to support the identity you are authoring rather than only the identity you inherited."]:
    S.append(p(t))
S.append(AccentQuote("Change is already happening. Participate in it.")); pb()

new("Continue with WE ARE ALCHEMY","The complete E3 field guide")
S.append(p("The E3 Reset gives you one complete movement through the practice. <i>WE ARE ALCHEMY</i> explores the larger philosophy and mechanics beneath that movement: Spark, the Mask, cause and effect, the Human Battery, Authorship, Myth, LifeMods, the Alchemist Path, the Identity Launch Sequence, and the continuing practice of living your legend."))
S.append(p("WE ARE ALCHEMY","H1x")); S.append(p("<i>An E3 Field Guide to Identity, Action, and Living Your Legend</i>","H2x"))
S.append(p("Inside the complete field guide, you will learn how to:","Prompt"))
bullets(["recognize the patterns shaping identity","distinguish state from self","move from reaction toward conscious cause","author identity through lived evidence","modify conditions that work against aligned action","integrate what experience teaches—and return when you drift"])
S.append(Spacer(1,8)); S.append(p("READ THE COMPLETE FIELD GUIDE","Kicker")); S.append(p('<link href="https://ne3ula.com/we-are-alchemy?utm_source=e3-reset&amp;utm_medium=pdf&amp;utm_campaign=we-are-alchemy&amp;offer=participant" color="#17131F"><u>ne3ula.com/we-are-alchemy</u></link>',"H2x")); pb()

class EndPage(Flowable):
    def wrap(self,aw,ah): self.width=aw; self.height=ah; return aw,ah
    def draw(self):
        c=self.canv; c.saveState(); c.resetTransforms()
        c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
        orbit(c,W/2,H*.68,66)
        c.setFont("NE3ULA-Bold",22); c.setFillColor(colors.white); c.drawCentredString(W/2,H*.53,"NOTICE. CHOOSE.")
        c.setFillColor(GOLD); c.drawCentredString(W/2,H*.485,"RETURN.")
        para=Paragraph("This guide is educational and reflective. It is not medical, psychological, legal, or financial advice. Seek qualified professional support for decisions or concerns that require it.",ParagraphStyle("end",fontName="NE3ULA",fontSize=8.5,leading=13,textColor=LAV,alignment=TA_CENTER))
        para.wrapOn(c,3.8*inch,1.2*inch); para.drawOn(c,1.1*inch,H*.30)
        c.setFont("NE3ULA-Bold",8); c.setFillColor(GOLD); c.drawCentredString(W/2,.8*inch,"© 2026 NE3ULA  /  E3")
        c.restoreState()

S.append(EndPage())

doc.build(S)
print(OUT)
