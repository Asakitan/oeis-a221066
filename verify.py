"""Determinize the row-parity relation; count distinct output masks only."""
from itertools import product
def allowed(u,v,w):
    if u^v^w: return (0,)
    return (1,2) if v else (0,3)
def step(U,letter):
    return frozenset((v,w) for u,v in U for w in (0,1) if letter in allowed(u,v,w))
states=[frozenset([(0,0),(0,1)])]; successors=[]
for U in states:
    row=[]
    for letter in range(4):
        Z=step(U,letter)
        if not Z:
            row.append(-1)
        else:
            if Z not in states:states.append(Z)
            row.append(states.index(Z))
    successors.append(row)
C=[int(any(w==0 for v,w in U)) for U in states]
Q=[1,-2,-2,-4,5,6]
V=[C]
for _ in range(6):
    V.append([sum(V[-1][j] for j in row if j>=0) for row in successors])
a=[0]+[v[0] for v in V[1:]]
if __name__=='__main__':
    print('Subset states:',len(states),'first terms:',a[1:7])
    residual=[sum(Q[j]*V[6-j][i] for j in range(len(Q))) for i in range(len(C))]
    assert len(states)==6 and residual==[0]*6,residual
    p=[sum(Q[j]*a[n-j] for j in range(min(n,5)+1)) for n in range(7)]
    assert p==[0,2,4,0,-8,-6,0],p
    print('All six residuals and numerator passed')
    for n in range(1,4):
        masks=set()
        for w in product(range(4),repeat=2*n):
            s=[0]+[w[2*i]+w[2*i+1] for i in range(n)]+[0]
            masks.add(tuple(int((2*w[i]-sum(s[i//2:i//2+3]))%4==0) for i in range(2*n)))
        assert len(masks)==a[n]
    print('Direct four-valued board enumeration also passed at heights 1..3.')
