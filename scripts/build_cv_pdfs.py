from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase.pdfmetrics import stringWidth
from pathlib import Path

OUT=Path('assets/cv'); OUT.mkdir(parents=True,exist_ok=True)
for n,f in [('Inter','DejaVuSans.ttf'),('Inter-Medium','DejaVuSans.ttf'),('Inter-SemiBold','DejaVuSans-Bold.ttf'),('Inter-Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
W,H=A4
NAVY=HexColor('#0B1018'); SURFACE2=HexColor('#1B2836'); ACCENT=HexColor('#74C0D8'); ACCENT2=HexColor('#A5DCEC'); WHITE=HexColor('#F7FAFC'); PAPER=HexColor('#F4F7FA'); TEXT=HexColor('#12202E'); MUTED=HexColor('#5E7080'); BORDER=HexColor('#D7E2EA'); PALE=HexColor('#EAF4F7')

def wrap(text,font,size,width):
    lines=[]; cur=''
    for w in text.split():
        t=w if not cur else cur+' '+w
        if stringWidth(t,font,size)<=width: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def text(c,s,x,y,w,font='Inter',size=8,lead=10.5,color=TEXT,bullet=False):
    c.setFont(font,size); c.setFillColor(color)
    if bullet:
        lines=wrap(s,font,size,w-10); c.circle(x+2.8,y-3.2,1.25,fill=1,stroke=0); x+=10
    else: lines=wrap(s,font,size,w)
    for i,line in enumerate(lines): c.drawString(x,y-i*lead,line)
    return y-len(lines)*lead

def title(c,s,x,y,w,dark=False):
    c.setFillColor(ACCENT2 if dark else NAVY); c.setFont('Inter-Bold',9.1); c.drawString(x,y,s.upper()); c.setStrokeColor(ACCENT if dark else HexColor('#B6DDE7')); c.line(x,y-5,x+w,y-5); return y-16

def build(name,lang):
    c=canvas.Canvas(str(OUT/name),pagesize=A4); c.setAuthor('Vladyslav Yeletskyi'); c.setTitle('Vladyslav Yeletskyi - '+('CV' if lang=='it' else 'Resume'))
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
    hh=118; c.setFillColor(NAVY); c.rect(0,H-hh,W,hh,fill=1,stroke=0); c.setFillColor(ACCENT); c.rect(0,H-hh,W,4,fill=1,stroke=0)
    bx,by=32,H-78; c.setFillColor(SURFACE2); c.roundRect(bx,by,48,48,13,fill=1,stroke=0); c.setStrokeColor(Color(.45,.75,.85,alpha=.35)); c.roundRect(bx,by,48,48,13,fill=0,stroke=1); c.setFillColor(ACCENT2); c.setFont('Inter-Bold',15); c.drawCentredString(bx+24,by+16,'VY')
    c.setFillColor(WHITE); c.setFont('Inter-Bold',24.5); c.drawString(96,H-45,'VLADYSLAV YELETSKYI')
    sub='LOGISTICA · MAGAZZINO · BACK OFFICE' if lang=='it' else 'LOGISTICS · WAREHOUSE · BACK OFFICE'; c.setFillColor(ACCENT2); c.setFont('Inter-SemiBold',10.7); c.drawString(96,H-65,sub)
    c.setFillColor(HexColor('#B7C6D2')); c.setFont('Inter',7.5); c.drawString(96,H-84,'Fagarè di San Biagio di Callalta (TV)  ·  +39 379 158 0070  ·  lavorovladyslav.yeletskyi@gmail.com')
    c.setFillColor(HexColor('#8EA1B2')); c.setFont('Inter',7.1); c.drawString(96,H-99,'linkedin.com/in/vladyslavyeletskyi  ·  github.com/VladislavII  ·  vladislavii.github.io/vladyslav-cv/')
    m=30; gap=20; lw=185; rx=m+lw+gap; rw=W-rx-m; top=H-hh-22; bottom=40
    c.setFillColor(NAVY); c.roundRect(m,bottom,lw,top-bottom+7,20,fill=1,stroke=0); sx=m+17; sw=lw-34; sy=top-5
    left_it=[('Competenze',['Operazioni di magazzino e movimentazione merci','Carrello elevatore e transpallet - abilitazione valida','Riordino degli spazi e supporto operativo','Microsoft Excel e Word','Google Workspace','Registrazione dati e documenti di base','Precisione, affidabilità e lavoro in squadra']),('Certificazioni',['Carrelli elevatori semoventi industriali - Azienda Sicura / SINALF · 25.02.2026','Sicurezza sul lavoro D.Lgs. 81/08 - formazione generale e specifica rischio basso · 2022']),('Lingue',['Italiano - B2','Inglese - A2','Ucraino - Madrelingua','Russo - Madrelingua']),('Disponibilità',['Immediata','Full time o part time','Stage o apprendistato','Disponibile al trasferimento']),('Informazioni',['Permesso di soggiorno valido','Disponibile a spostamenti compatibili con la sede di lavoro'])]
    left_en=[('Skills',['Warehouse operations and goods handling','Forklift and pallet truck - valid qualification','Storage-area organization and operational support','Microsoft Excel and Word','Google Workspace','Basic data and document recording','Accuracy, reliability and teamwork']),('Certifications',['Industrial self-propelled forklifts - Azienda Sicura / SINALF · 25 Feb 2026','Workplace safety D.Lgs. 81/08 - general and low-risk specific training · 2022']),('Languages',['Italian - B2','English - A2','Ukrainian - Native','Russian - Native']),('Availability',['Immediate','Full-time or part-time','Internship or apprenticeship','Open to relocation']),('Information',['Valid Italian residence permit','Open to reasonable commuting for the role'])]
    for h,items in (left_it if lang=='it' else left_en):
        sy=title(c,h,sx,sy,sw,True)
        for v in items: sy=text(c,v,sx,sy,sw,size=7.65,lead=9.4,color=HexColor('#D6E0E8'),bullet=True)-3
        sy-=10
    ry=top
    def rt(s):
        nonlocal ry; ry=title(c,s,rx,ry,rw,False)
    def rp(s,size=8.3,lead=11):
        nonlocal ry; ry=text(c,s,rx,ry,rw,size=size,lead=lead)-9
    def job(role,meta,bullets):
        nonlocal ry; c.setFillColor(PALE); c.roundRect(rx,ry-12,rw,15,7,fill=1,stroke=0); c.setFillColor(NAVY); c.setFont('Inter-SemiBold',9.4); c.drawString(rx+8,ry-1,role); ry-=19; c.setFillColor(MUTED); c.setFont('Inter-Medium',7.5); c.drawString(rx,ry,meta); ry-=12
        for b in bullets: ry=text(c,b,rx,ry,rw,size=7.65,lead=9.8,bullet=True)-2
        ry-=8
    def edu(h,meta,b):
        nonlocal ry; c.setFillColor(NAVY); c.setFont('Inter-SemiBold',9.1); c.drawString(rx,ry,h); ry-=11; c.setFillColor(MUTED); c.setFont('Inter-Medium',7.3); c.drawString(rx,ry,meta); ry-=11; ry=text(c,b,rx,ry,rw,size=7.5,lead=9.5,bullet=True)-9
    if lang=='it':
        rt('Profilo'); rp("Diplomato in Sistemi Informativi Aziendali con formazione in logistica e abilitazione all'uso del carrello elevatore. Ho esperienza in attività manuali, manutenzione, riordino e lavoro agricolo svolto nel rispetto di procedure e norme igienico-sanitarie. Cerco un impiego operativo stabile e sono disponibile a imparare una nuova mansione tramite affiancamento, stage o apprendistato.")
        rt('Esperienza lavorativa'); job('Addetto ai servizi generali','Camelia Rooms · Mestre (VE) · Apr 2026 - Lug 2026',['Riparazione, stuccatura e tinteggiatura di pareti; posa di pannelli per controsoffitto.','Supporto alla pulizia del cortile e, quando necessario, alla preparazione della colazione.',"Avvio del riordino dell'area deposito e svolgimento di attività operative secondo le priorità della struttura."]); job('Operatore agricolo','Azienda Agricola Rivolo · Zero Branco (TV) · Giu 2023 - Set 2023',['Distribuzione del mangime e pulizia di mangiatoie, stalle e aree comuni in allevamento suinicolo.','Supporto alla squadra nelle attività di selezione, vaccinazione e alimentazione di suini e suinetti.','Applicazione delle procedure igienico-sanitarie e di sicurezza durante le attività quotidiane.'])
        rt('Istruzione e formazione'); edu('Diploma in Sistemi Informativi Aziendali','Istituto Tecnico Economico Riccati-Luzzatti · Treviso · 2022 - 2025','Economia aziendale, informatica e gestione dei dati.'); edu('Operatore della logistica e del magazzino','Regione del Veneto · MAW SPA · 112 ore · EQF 3 · 12 - 29 Mag 2026','Movimentazione e stoccaggio, organizzazione degli spazi, imballaggio, spedizione e dati di magazzino.'); edu('Operatore amministrativo segretariale','Regione del Veneto · MAW SPA · 84 ore · EQF 3 · Ott 2025','Gestione documentale, comunicazione scritta e organizzazione operativa.')
        rt('Formazione extra e interessi');
        for b in ['Violino - percorso completo di 8 anni presso una scuola di musica in Ucraina, con diploma.','Tecnologia e AI - creazione di piccoli progetti digitali con strumenti di intelligenza artificiale; conoscenza di base dei concetti di programmazione.']: ry=text(c,b,rx,ry,rw,size=7.45,lead=9.5,bullet=True)-3
        foot='Autorizzo il trattamento dei dati personali ai sensi del Regolamento UE 2016/679 (GDPR).'
    else:
        rt('Profile'); rp('Business Information Systems graduate with logistics training and a valid forklift qualification. I have experience in hands-on work, maintenance, organizing storage areas and agricultural operations carried out in line with procedures and hygiene and safety standards. I am looking for a stable operational role and I am open to learning a new position through on-the-job training, an internship or an apprenticeship.',8.15,10.8)
        rt('Work experience'); job('General Services Assistant','Camelia Rooms · Mestre (VE) · Apr 2026 - Jul 2026',['Wall repair, filling and painting; installation of suspended-ceiling panels.','Support with courtyard cleaning and, when needed, breakfast preparation.','Started reorganizing the storage area and carried out operational tasks according to the property’s priorities.']); job('Agricultural Worker','Azienda Agricola Rivolo · Zero Branco (TV) · Jun 2023 - Sep 2023',['Distributed feed and cleaned feeders, pens and common areas on a pig farm.','Supported the team with selection, vaccination and feeding of pigs and piglets.','Followed hygiene, sanitation and safety procedures during daily work.'])
        rt('Education and training'); edu('Diploma in Business Information Systems','Istituto Tecnico Economico Riccati-Luzzatti · Treviso · 2022 - 2025','Business administration, IT and data management.'); edu('Logistics and Warehouse Operator','Regione del Veneto · MAW SPA · 112 hours · EQF 3 · 12 - 29 May 2026','Goods handling and storage, warehouse-space organization, packing, shipping and warehouse data.'); edu('Administrative and Secretarial Operator','Regione del Veneto · MAW SPA · 84 hours · EQF 3 · Oct 2025','Document management, written communication and operational organization.')
        rt('Additional training and interests');
        for b in ['Violin - completed an 8-year music-school program in Ukraine and received a diploma.','Technology and AI - small digital projects using AI tools; basic understanding of programming concepts.']: ry=text(c,b,rx,ry,rw,size=7.45,lead=9.5,bullet=True)-3
        foot='I authorize the processing of my personal data in accordance with EU Regulation 2016/679 (GDPR).'
    c.setStrokeColor(BORDER); c.line(rx,bottom-4,W-m,bottom-4); c.setFillColor(HexColor('#7B8C9A')); c.setFont('Inter',6.2); c.drawRightString(W-m,20,foot); c.save()

build('Vladyslav_Yeletskyi_CV_IT.pdf','it')
build('Vladyslav_Yeletskyi_CV_EN.pdf','en')
