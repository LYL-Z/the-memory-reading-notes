function simulate(){
 let seed=20261125;function u(){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed+.5)/4294967296}function normal(){return Math.sqrt(-2*Math.log(u()))*Math.cos(2*Math.PI*u())}
 const theta=Math.PI/3,a=Math.cos(theta/2)**2,b=Math.sin(theta/2)**2;
 const berry=[16,64,256,1024].map(N=>{const d=2*Math.PI/N,phase=-N*Math.atan2(b*Math.sin(d),a+b*Math.cos(d));return {N,phase,error:Math.abs(phase+Math.PI/2)}})
 const erasure=[0,100,300,1000].map(D=>{const eta=.8,p=eta*2**(-D/100),N=20000;let k=0;for(let i=0;i<N;i++)k+=u()<p?1:0;return {D,N,k,expected:p,observed:k/N,SE:Math.sqrt(p*(1-p)/N)}})
 const noise=[0,.9].map(rho=>{let N=600,R=3000,sum=0,sq=0,exceed=0;for(let j=0;j<R;j++){let x=normal(),s=x;for(let i=1;i<N;i++){x=rho*x+Math.sqrt(1-rho*rho)*normal();s+=x}const m=s/N;sum+=m;sq+=m*m;exceed+=Math.abs(m)>3/Math.sqrt(N)?1:0}let varExact=N;for(let k=1;k<N;k++)varExact+=2*(N-k)*rho**k;return {rho,N,R,observedSD:Math.sqrt((sq-sum*sum/R)/(R-1)),theorySD:Math.sqrt(varExact)/N,naive3sigmaFalsePositive:exceed/R}})
 return {seed:20261125,berry,erasure,noise,whiteNoise:{N:600000,SE:1e-3/Math.sqrt(600000),z:3e-7/(1e-3/Math.sqrt(600000)),N5:Math.ceil((5e-3/3e-7)**2)},landauer300K:1.380649e-23*300*Math.log(2)}
}
console.log(JSON.stringify(simulate(), null, 2));
