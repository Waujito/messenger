import{s as m,r as a,o as _,c as g,a as e,x as l,y as u,z as i,A as c,v as d,Q as f,R as v,_ as y}from"./entry.Bx5cC3F6.js";const h=e("h1",null,"Register",-1),w=e("h2",null,"Enter name:",-1),x=e("h2",null,"Enter password:",-1),R=m({__name:"register",setup(F){const r=a(""),o=a("");async function p(){const n=f();if(!r.value||!o.value)return alert("Required fields are null.");const t={username:r.value,password:o.value};try{const s=await n.post("/register",t)}catch(s){alert(s instanceof Error?s.message:"An unexpected error occured")}v().push("/login")}return(n,t)=>(_(),g("div",{class:d(n.$style.registerForm)},[h,e("div",null,[w,l(e("input",{"onUpdate:modelValue":t[0]||(t[0]=s=>c(r)?r.value=s:null),type:"text"},null,512),[[u,i(r)]])]),e("div",null,[x,l(e("input",{"onUpdate:modelValue":t[1]||(t[1]=s=>c(o)?o.value=s:null),type:"password"},null,512),[[u,i(o)]])]),e("button",{class:d(n.$style.loginButton),onClick:p},"Login",2)],2))}}),k="_registerForm_1haak_1",B={registerForm:k},E={$style:B},C=y(R,[["__cssModules",E]]);export{C as default};
