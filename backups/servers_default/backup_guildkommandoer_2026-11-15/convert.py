"""Move guild chat-command blocks of NPCs from the client part to the server part.
usage: convert.py <worlddir> <backupdir> [--apply]"""
import re,sys,os,shutil
W,B=sys.argv[1],sys.argv[2]; APPLY='--apply' in sys.argv
# (file, x, y, mode)  mode: chat = move top-level 'if (playerchats' blocks; all = move whole client part
T=[]
def add(f,coords,mode):
    for c in coords: T.append((f,str(c[0]),str(c[1]),mode))
add('bridgeton-garriton-throneroom.nw',[(20,19),(25,56),(36,56),(41,19)],'all')
add('bridgeton-garritontunnel2.nw',[(29,44),(36,20)],'all')
for f in ['bridgeton-insides_engineer4.nw']: add(f,[(6,30)],'chat')
add('bridgeton-insides_engineer6.nw',[(39,31)],'chat')
add('bridgeton-insides_engineer7.nw',[(39,30)],'chat')
add('bridgeton-insides_inn2.nw',[(0,0)],'chat')
for f in ['laboo-orcworktent.nw','laboo-orcworktent2.nw','laboo-orcworktent3.nw']: add(f,[(34,14)],'chat')
add('mournglade-karasuhouse.nw',[(65,24)],'chat')
add('portseriah_inn1.nw',[(65,24)],'chat')
add('portseriah_secretinn.nw',[(42,31),(44,31),(42,26),(43,26)],'chat')
add('levels/newworld/greendale/staghorn-castle-outside.nw',[(23,52),(29,28),(34,28),(41,52)],'all')
for f in ['levels/newworld/mournhold/mournhold_maze.nw','levels/newworld/mournhold/mournhold_test.nw']:
    add(f,[(11,18),(13,8),(15,34),(17,20),(19,9),(9,32)],'all')
add('val-new-city_c4.nw',[(48,42)],'c4')
add('levels/newworld/thistletop/thistletop_treasure.nw',[(22,26),(11,28),(21,28),(19,25),(19,30),(18,27),(16,29),(16,25),(15,27),(12,30)],'trap')
TRAP=open(os.path.join(os.path.dirname(__file__),'trap.txt')).read()
CLIENTONLY=set(open(os.path.join(os.path.dirname(__file__),'clientonly.txt')).read().split())

def stmt_end(s,i):
    """s[i] starts a statement; return index after it."""
    while i<len(s) and s[i].isspace(): i+=1
    if s.startswith('if',i) and not s[i+2:i+3].isalnum():
        j=s.index('(',i); d=0
        while True:
            if s[j]=='(': d+=1
            elif s[j]==')':
                d-=1
                if d==0: break
            j+=1
        k=stmt_end(s,j+1)
        m=re.match(r'\s*else\b',s[k:])
        if m: k=stmt_end(s,k+m.end())
        return k
    if i<len(s) and s[i]=='{':
        d=0; j=i
        while j<len(s):
            if s[j]=='{': d+=1
            elif s[j]=='}':
                d-=1
                if d==0: return j+1
            j+=1
        return len(s)  # unbalanced: to the end
    j=s.find(';',i); return len(s) if j<0 else j+1

def balance(b):
    n=b.count('{')-b.count('}'); return b+'\n'+'}'*n if n>0 else b

changed={}
for f,x,y,mode in T:
    p=os.path.join(W,f); t=changed.get(p) or open(p,encoding='latin1').read()
    m=[m for m in re.finditer(r'^NPC (\S+) (\S+) (\S+)\n(.*?)^NPCEND',t,re.S|re.M) if m.group(2)==x and m.group(3)==y]
    assert len(m)==1,(f,x,y,len(m)); m=m[0]
    body=m.group(4); i=body.find('//#CLIENTSIDE'); srv,cl=body[:i],body[i+len('//#CLIENTSIDE'):]
    cl=cl.replace('//#SERVERSIDE\n','')
    if mode=='trap':
        t=t[:m.start(4)]+TRAP+t[m.end(4):]; changed[p]=t; print('ok',f,x,y,'trap'); continue
    if mode=='all':
        moved,rest=cl,''
    else:
        moved=[];rest=[];k=0
        for mm in re.finditer(r'^\s*if\s*\(\s*(playerchats|created|movementfinished)\b',cl,re.M):
            if mm.start()<k: continue
            ev=mm.group(1)
            if mode=='chat' and ev!='playerchats': continue
            e=stmt_end(cl,mm.start())
            rest.append(cl[k:mm.start()]); moved.append(balance(cl[mm.start():e])); k=e
        rest.append(cl[k:]); moved='\n'.join(moved); rest=''.join(rest)
    bad=[w for w in re.findall(r'\b([a-z0-9]+)\b',moved) if w in CLIENTONLY]
    if bad: print('CLIENT-ONLY in',f,x,y,bad)
    if 'playerchats' not in moved: print('NOTHING moved',f,x,y)
    moved=moved.replace('this.moving=0\n','this.moving=0;\n')
    nb=srv.rstrip('\n')+('\n' if srv.strip() else '')+'// guild commands moved to server-side so every player sees them\n'+moved.strip('\n')+'\n'
    if rest.strip(): nb+='//#CLIENTSIDE\n'+rest.lstrip('\n')
    t=t[:m.start(4)]+nb+t[m.end(4):]
    changed[p]=t
    print('ok',f,x,y,mode,'moved %d lines, client left %d'%(moved.count('\n')+1,rest.strip().count('\n')+1 if rest.strip() else 0))
if APPLY:
    for p,t in changed.items():
        bp=os.path.join(B,os.path.relpath(p,W)); os.makedirs(os.path.dirname(bp),exist_ok=True)
        if not os.path.exists(bp): shutil.copy2(p,bp)
        open(p,'w',encoding='latin1').write(t)
    print('wrote',len(changed),'files')
else:
    out=sys.argv[3] if len(sys.argv)>3 and not sys.argv[3].startswith('--') else None
    for p,t in changed.items():
        d=os.path.join(os.path.dirname(__file__),'preview',os.path.relpath(p,W)); os.makedirs(os.path.dirname(d),exist_ok=True); open(d,'w',encoding='latin1').write(t)
