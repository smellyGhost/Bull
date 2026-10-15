import math
N=lambda z:0.5*(1+math.erf(z/math.sqrt(2)))
def bs(S,K,T,s,c,r=0.039):
    if T<=1e-6: return max(S-K,0) if c else max(K-S,0)
    d1=(math.log(S/K)+(r+s*s/2)*T)/(s*math.sqrt(T)); d2=d1-s*math.sqrt(T)
    return S*N(d1)-K*math.exp(-r*T)*N(d2) if c else K*math.exp(-r*T)*N(-d2)-S*N(-d1)
S=553.11
Q={('J',520,'P'):(23.95,.362),('J',500,'P'):(17.40,.375),('J',450,'P'):(7.975,.409),('J',420,'P'):(4.975,.440),('J',400,'P'):(3.575,.461),('J',600,'C'):(21.2,.341),
   ('M',520,'P'):(33.7,.373),('M',450,'P'):(15.0,.409),('M',400,'P'):(7.40,.434),
   ('U',520,'P'):(44.7,.373),('U',450,'P'):(23.35,.399),('U',400,'P'):(13.25,.421)}
T={'J':0.25,'M':0.43,'U':0.67}
structs={
 'Jan 520P 单买':[('J',520,'P',1)],
 'Jan 500P 单买':[('J',500,'P',1)],
 'Jan 520/450':[('J',520,'P',1),('J',450,'P',-1)],
 'Jan 520/400':[('J',520,'P',1),('J',400,'P',-1)],
 'Jan 500/400':[('J',500,'P',1),('J',400,'P',-1)],
 'Mar 520/400':[('M',520,'P',1),('M',400,'P',-1)],
 'Jun 520/400':[('U',520,'P',1),('U',400,'P',-1)],
 'Jun 520/450':[('U',520,'P',1),('U',450,'P',-1)],
 'Jan 领口 520P+卖600C':[('J',520,'P',1),('J',600,'C',-1)],
 'Jan 520/400+卖600C':[('J',520,'P',1),('J',400,'P',-1),('J',600,'C',-1)],
}
shocks=[('+10%',.10,-.03),('-10%',-.10,.05),('-18%',-.18,.10),('-35%',-.35,.25)]
n=2
print('结构 | 成本(2张) | 最大赔付 | 赔付/成本 | 保护区间 | 每月成本 | 1个月后MTM: +10% / -10% / -18% / -35% | 到期: -18% / -35%')
for name,legs in structs.items():
    cost=sum(q*Q[(e,k,t)][0] for e,k,t,q in legs)*100*n
    months=T[legs[0][0]]*12
    def val(S1,dt,ivb):
        return sum(q*bs(S1,k,max(T[e]-dt,0),Q[(e,k,t)][1]+ivb,t=='C') for e,k,t,q in legs)*100*n
    base=val(S,0,0)
    mtm=[val(S*(1+r),1/12,ivb)-base for _,r,ivb in shocks]
    exp=[sum(q*(max(k-S1,0) if t=='P' else max(S1-k,0)) for e,k,t,q in legs)*100*n-cost for S1 in (S*0.82,S*0.65)]
    puts=[k for e,k,t,q in legs if t=='P']
    if len(puts)==2: mx=(puts[0]-puts[1])*100*n; rng=f'{puts[0]}→{puts[1]} ({100*(puts[0]/S-1):.0f}%→{100*(puts[1]/S-1):.0f}%)'
    else: mx=None; rng=f'{puts[0]}以下不封顶 ({100*(puts[0]/S-1):.0f}%以下)'
    ratio=f'{(mx-cost)/cost:.1f}x' if mx and cost>0 else '—'
    print(f"{name} | ${cost:,.0f} | {'$%s'%format(mx,',') if mx else '不封顶'} | {ratio} | {rng} | ${cost/months:,.0f} | "+' / '.join(f'{v:+,.0f}' for v in mtm)+' | '+' / '.join(f'{v:+,.0f}' for v in exp))
