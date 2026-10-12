from playwright.sync_api import sync_playwright
import os, shutil, sys
from PIL import Image
D=os.getcwd()
LOGO=f'file://{D}/logo/Loveth-icon-1024.png'
F="Inter, 'Noto Color Emoji', sans-serif"
FD="'Inter Display', Inter, sans-serif"
MSG='<div class="ic" style="background:linear-gradient(#65F47E,#0FC035);display:flex;align-items:center;justify-content:center"><svg width="25" height="23" viewBox="0 0 24 22"><path d="M12 1C5.9 1 1 5 1 9.9c0 2.8 1.6 5.3 4.1 6.9-.2 1.4-.9 2.9-2.1 4 2.4-.1 4.4-1 5.8-2.2 1 .3 2.1.4 3.2.4 6.1 0 11-4 11-8.9S18.1 1 12 1z" fill="#fff"/></svg></div>'
LIC=f'<img class="ic" src="{LOGO}">'
def n(t,b,w='now',kind='l'):
    return f'<div class="nt">{LIC if kind=="l" else MSG}<div style="flex:1;min-width:0"><div class="hd"><b>{t}</b><span>{w}</span></div><div class="bd">{b}</div></div></div>'
# wallpapers: (base, blobs[(x,y,r,color)])
W={
 'dusk':('#1a1530',[(20,18,60,'#d9907a'),(85,30,55,'#8a4f7d'),(40,70,70,'#2d2a5c'),(90,90,50,'#3a1f3f')]),
 'blue':('#0d1630',[(75,12,60,'#86b2e8'),(15,40,55,'#3c63a8'),(60,75,70,'#1b2c5c'),(10,95,45,'#0f1b3d')]),
 'warm':('#2a1424',[(25,10,60,'#f4b98c'),(80,35,55,'#d06a5f'),(35,75,65,'#7a3658'),(85,95,45,'#3b1830')]),
 'green':('#0b1b1a',[(65,10,60,'#a6d0a8'),(15,40,55,'#4f8670'),(70,75,65,'#1f4440'),(15,95,45,'#0e2422')]),
 'night':('#0e1022',[(50,5,60,'#6a6f9c'),(10,45,55,'#33386a'),(85,70,60,'#20234a'),(40,100,50,'#0b0c1c')]),
}
def wall(k):
    base,bl=W[k]
    g=','.join(f'radial-gradient(circle at {x}% {y}%, {c} 0%, transparent {r}%)' for x,y,r,c in bl)
    return f'{g},{base}'
CSS=f'''body{{margin:0}}*{{box-sizing:border-box}}
.ph{{width:393px;height:852px;position:relative;overflow:hidden;font-family:{F};-webkit-font-smoothing:antialiased}}
.grain{{position:absolute;inset:0;opacity:.16;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
.nt{{display:flex;gap:10px;align-items:flex-start;padding:13px 14px 13px 13px;border-radius:22px;background:rgba(242,242,247,.62);backdrop-filter:blur(28px) saturate(1.9);-webkit-backdrop-filter:blur(28px) saturate(1.9);color:#000}}
.ic{{width:38px;height:38px;border-radius:9px;flex-shrink:0;margin-top:1px}}
.hd{{display:flex;justify-content:space-between;gap:8px;font-size:15px;line-height:20px;letter-spacing:-.2px}}
.hd b{{font-weight:600}} .hd span{{font-size:13px;color:rgba(60,60,67,.62);white-space:nowrap}}
.bd{{font-size:15px;line-height:20px;letter-spacing:-.2px}}
.cap{{display:inline;font-family:{F};font-weight:700;font-size:21px;line-height:1.55;color:#fff;background:rgba(0,0,0,.55);padding:3px 9px;border-radius:7px;-webkit-box-decoration-break:clone;box-decoration-break:clone}}
.btn{{position:absolute;bottom:42px;width:50px;height:50px;border-radius:25px;background:rgba(40,40,48,.42);backdrop-filter:blur(20px);display:flex;align-items:center;justify-content:center}}
'''
def lock(cap,time,date,notifs,wk):
    return f'''<div class="ph" style="background:{wall(wk)}"><div class="grain"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08),transparent 30%,transparent 60%,rgba(0,0,0,.35))"></div>
<div style="position:absolute;top:17px;left:34px;color:#fff;font-weight:600;font-size:17px;letter-spacing:-.3px">EE</div>
<div style="position:absolute;top:19px;right:28px;display:flex;gap:6px;align-items:center">
<svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx=".8" fill="#fff"/><rect x="5" y="5.5" width="3" height="6.5" rx=".8" fill="#fff"/><rect x="10" y="3" width="3" height="9" rx=".8" fill="#fff"/><rect x="15" y="0" width="3" height="12" rx=".8" fill="#fff"/></svg>
<svg width="17" height="12" viewBox="0 0 17 12"><path d="M8.5 2.3c2.4 0 4.6.9 6.2 2.5l1.3-1.3C14 1.6 11.4.5 8.5.5S3 1.6 1 3.5l1.3 1.3C3.9 3.2 6.1 2.3 8.5 2.3zm0 3.5c1.4 0 2.7.6 3.7 1.5l1.3-1.3c-1.3-1.2-3.1-2-5-2s-3.7.8-5 2L4.8 7.3c1-.9 2.3-1.5 3.7-1.5zm0 3.4c-.6 0-1.2.2-1.6.6l1.6 1.7 1.6-1.7c-.4-.4-1-.6-1.6-.6z" fill="#fff"/></svg>
<div style="display:flex;align-items:center;gap:1px"><div style="width:25px;height:12px;border-radius:3.5px;border:1px solid rgba(255,255,255,.5);padding:1.5px"><div style="width:72%;height:100%;border-radius:2px;background:#fff"></div></div><div style="width:1.5px;height:4px;border-radius:0 1px 1px 0;background:rgba(255,255,255,.5)"></div></div></div>
<div style="position:absolute;top:58px;left:0;right:0;display:flex;justify-content:center"><svg width="13" height="17" viewBox="0 0 13 17"><path d="M3 7V4.8a3.5 3.5 0 0 1 7 0V7" fill="none" stroke="#fff" stroke-width="1.8"/><rect x="0.5" y="7" width="12" height="9.5" rx="2.2" fill="#fff"/></svg></div>
<div style="position:absolute;top:84px;left:0;right:0;text-align:center;color:rgba(255,255,255,.9);font-weight:600;font-size:20px;letter-spacing:-.2px">{date}</div>
<div style="position:absolute;top:104px;left:0;right:0;text-align:center;color:rgba(255,255,255,.93);font-family:{FD};font-weight:700;font-size:100px;line-height:1;letter-spacing:-2px">{time}</div>
<div style="position:absolute;left:24px;right:24px;top:262px;text-align:center">{''.join(f'<span class="cap">{c}</span><br>' for c in cap.split('|'))}</div>
<div style="position:absolute;left:8px;right:8px;top:352px;display:flex;flex-direction:column;gap:8px">{''.join(notifs)}</div>
<div class="btn" style="left:46px"><svg width="14" height="24" viewBox="0 0 14 24"><path d="M1 1h12v3.5L10 9v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V9L1 4.5z" fill="#fff"/><rect x="6" y="11" width="2" height="4" rx="1" fill="rgba(40,40,48,.9)"/></svg></div>
<div class="btn" style="right:46px"><svg width="24" height="19" viewBox="0 0 24 19"><path d="M2.5 4h4.2l1.6-2.5h7.4L17.3 4h4.2A1.5 1.5 0 0 1 23 5.5v11a1.5 1.5 0 0 1-1.5 1.5h-19A1.5 1.5 0 0 1 1 16.5v-11A1.5 1.5 0 0 1 2.5 4z" fill="#fff"/><circle cx="12" cy="10.5" r="4.3" fill="rgba(40,40,48,.95)"/><circle cx="12" cy="10.5" r="3" fill="#fff"/></svg></div>
<div style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);width:134px;height:5px;border-radius:3px;background:#fff"></div></div>'''

ads=[
 ('01-resolved-a-fight','the notification I never|thought I’d get','22:47','Tuesday 13 October',[n('Proud of you two 👏','You two just resolved a fight. 14 minutes, start to finish. Your fastest yet.'),n('Mark','Sorry I got defensive. Love you x','now','m')],'dusk'),
 ('02-not-defensive','he’s actually changing','08:12','Monday 19 October',[n('He’s really trying 💪','Mark has gone 10 days without getting defensive. His longest streak yet.')],'blue'),
 ('03-six-days','6 days. we used to not|manage 6 hours','21:05','Sunday 11 October',[n('Look at you two 🎉','You’ve gone 6 days with no arguments! Well done, you two.')],'warm'),
 ('04-talked-it-through','we actually talked|instead of shouting','23:18','Friday 16 October',[n('That’s how it’s done 🙌','You and John talked it through. Well done! Your summary and next step are ready.'),n('John','Thank you for hearing me out x','2m ago','m')],'night'),
 ('05-sorry-first','he said sorry FIRST','19:40','Thursday 22 October',[n('This is growth 🌱','Mark said sorry first today. That’s the third time this month.')],'green'),
 ('06-noticed-effort','someone finally noticed','22:01','Wednesday 14 October',[n('Your effort counts 💛','Jamie noticed your effort today. He marked it a good day.')],'dusk'),
 ('07-same-fight-faster','same fight as last month.|this time it took 9 minutes','20:26','Saturday 24 October',[n('Look how far you’ve come','Last time this argument: 3 days of silence. Today: sorted in 9 minutes.')],'blue'),
 ('09-kept-his-word','he kept his word.|every single day','21:30','Sunday 18 October',[n('A man of his word 🤝','Dan did what he promised, every day this week. 7 out of 7.'),n('Dan','Told you I would x','1m ago','m')],'warm'),
 ('10-she-noticed','she noticed','21:48','Thursday 15 October',[n('She saw that 👀','Sarah noticed you put your phone away at dinner.'),n('Sarah','Thank you. It meant a lot x','now','m')],'green'),
 ('12-thirty-days','we used to fight every week','19:12','Thursday 5 November',[n('Longest stretch ever 🏆','30 days without a fight. You two did this.','2h ago'),n('Mark','Dinner Friday? Just us x','now','m')],'dusk'),
 ('13-trash','she noticed','19:22','Wednesday 21 October',[n('Small things, big wins','Sarah noticed you took the trash out without being asked.'),n('Sarah','Thank you babe x','now','m')],'green'),
 ('14-asked-about-her-day','it was that simple?','21:36','Monday 12 October',[n('That made her day 💛','Sarah noticed you asked about her day. She marked it a good day.')],'blue'),
 ('15-kind-when-angry','she said I’ve changed','22:54','Friday 23 October',[n('That took strength 💪','Sarah noticed you stayed kind, even when you were angry.'),n('Sarah','I know that wasn’t easy. Thank you x','1m ago','m')],'night'),
 ('16-let-me-finish','he let me finish.|for once','22:19','Tuesday 20 October',[n('He’s listening now','Mark listened without interrupting. All the way through.')],'dusk'),
 ('17-no-but','sorry. no “but”','23:07','Thursday 15 October',[n('Mark','I’m sorry. I was wrong x','now','m'),n('That’s a real apology 🙏','Mark apologised without a “but”. First time this month.')],'warm'),
 ('18-forget-it','I stopped saying|“forget it”','20:48','Sunday 25 October',[n('You’re being heard 💬','You haven’t said “forget it” in 14 days.')],'blue'),
 ('19-silent-treatment','no silent treatment.|21 days','08:03','Saturday 31 October',[n('Peace looks good on you ☀️','21 days without the silent treatment. Your longest stretch yet.'),n('Mark','Morning gorgeous x','now','m')],'dusk'),
 ('20-phone-down','I didn’t even have to ask','21:12','Thursday 22 October',[n('Fully present 📵','Mark put his phone down when you were talking. 5 nights in a row.')],'night'),
 ('21-really-feeling','he asked how I’m|REALLY doing','18:31','Wednesday 28 October',[n('Mark','How are you really feeling today? x','now','m'),n('He’s checking in ❤️','Mark checked in on you today. Day 12 in a row.')],'green'),
 ('22-sofa','the sofa’s just a sofa again','23:40','Saturday 7 November',[n('One whole month 🎉','A whole month and nobody slept on the sofa. Well done, you two.')],'warm'),
]
only=sys.argv[1:]
out='real'; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':393,'height':852},device_scale_factor=3)
    for k,cap,t,d,ns,wk in ads:
        if only and k[:2] not in only: continue
        open('_r.html','w').write(f'<html><head><style>{CSS}</style></head><body>{lock(cap,t,d,ns,wk)}</body></html>')
        pg.goto('file://'+os.path.abspath('_r.html')); pg.wait_for_timeout(400); pg.screenshot(path=f'{out}/Loveth-{k}.png')
    b.close()
