# ref-定积分计算.md（专题 9 方法库）

来源：用户 2026-09-27 贴出的「高数上册进阶 9　定积分计算的解题方法」板书（考法一~五，例题 1–24，含若干类题）。
本文件只收**可复用的判据**与**已解例题的结果**，逐题推进时追加（与 `ref-不等式与中值定理.md`、`ref-不定积分方法.md` 同一体系）。

## 一、五考法动作对照

| 考法 | 题面长相 | 第一步动作 |
|---|---|---|
| 一 牛顿—莱布尼兹 | 区间有限、被积函数可化简 | 先用三角恒等式／代数变形压成单变量代数式，再求原函数，最后端点相减 |
| 二 性质简化 | 区间对称、含 $x$ 权重、$\sin^m\cos^n$ | 平移把对称中心搬到原点 → 查奇偶 → 配对 $x$ 与 $a+b-x$ → 点火公式 |
| 三 区间再现 | 被积函数含 $\ln$、$\arctan e^x$，或 $f(x)+f(a+b-x)$ 为常数 | 写出 $x\to a+b-x$ 的配对式，两式相加（半数即结果） |
| 四 分段函数 | 最值、取整、绝对值 | 先定分界点，逐段写表达式再积 |
| 五 综合 | 被积含变限积分、含 $f'$、待定常数、递推 | 换序积分／分部／设待定常数解方程／分部导出递推 |

## 二、已解例题（结果 + 关键动作）

| 题 | 结果 | 关键动作 |
|---|---|---|
| 例 1 $\int_0^{\pi/2}\sin x\ln\sin x\,\mathrm dx$ | $\ln2-1$ | $t=\cos x$ 吸收 $\sin x\,\mathrm dx$；$\ln\sin x=\frac12\ln(1-t^2)$ 拆 $(1-t)(1+t)$；端点按 $t\to1^-$ 取极限 |
| 例 2 $\int_0^\pi\frac{\mathrm dx}{1+\cos^2x}$ | $\frac{\pi}{\sqrt2}$ | 关于 $\frac\pi2$ 对称折半 → 同除 $\cos^2x$ → $t=\tan x$（上限 $+\infty$） |
| 例 3 $\int_{-\pi/2}^{\pi/2}(x^3+\sin^2x)\cos^2x\,\mathrm dx$ | $\frac\pi8$ | 奇部 $x^3\cos^2x$ 归零；偶部折半后 $\sin^2x\cos^2x=\frac18(1-\cos4x)$ |
| 例 4 $\int_0^2\arcsin|x-1|\sqrt{2x-x^2}\,\mathrm dx$ | $\frac{\pi^2}{8}-\frac12$ | 平移 $u=x-1$ 造对称 → 偶函数折半 → $u=\sin\theta$ 同去根号与反三角 |
| 例 4 类题 $\int_0^2[(x-1)^3+2x]\sqrt{1-\cos2\pi x}\,\mathrm dx$ | $\frac{8\sqrt2}{\pi}$ | $\sqrt{1-\cos2\pi x}=\sqrt2|\sin\pi x|$ → 平移 → $t^3$ 与 $2t$ 项归零 |
| 例 5 $\int_0^\pi\frac{x|\sin x\cos x|}{1+\sin^4x}\,\mathrm dx$ | $\frac{\pi^2}{8}$ | 因子只依赖 $\sin x$ → 套 $\int_0^\pi xf(\sin x)\mathrm dx=\frac\pi2\int_0^\pi f(\sin x)\mathrm dx$ → 折半去绝对值 → $u=\sin^2x$ |
| 例 6 $\int_{e^{-2\pi}}^{1}\left|\frac{\mathrm d}{\mathrm dx}\cos\left(\ln\frac1x\right)\right|\mathrm dx$ | $4$ | 先求导得 $-\frac{\sin(\ln x)}x$ → $t=\ln x$，区间变 $[-2\pi,0]$ → $|\sin t|$ 偶性翻正 + 周期 $\pi$ 折拱 → $\int_0^{2\pi}\|\sin t\|\mathrm dt=2\cdot2=4$ |
| 例 7 $\int_{-2}^{2}x\ln(1+e^x)\,\mathrm dx$ | $\frac{8}{3}$ | 区间再现 $x\to-x$ 配对 → $\ln\frac{1+e^x}{1+e^{-x}}=\ln e^x=x$（分子分母同乘 $e^x$）→ $2I=\int_{-2}^2x^2\mathrm dx=\frac{16}{3}$ |
| 例 7 类题 1 $\int_{-1}^{1}\frac{\mathrm dx}{(e^x+1)(x^2+1)}$ | $\frac{\pi}{4}$ | $x\to-x$ 配对相加 → $\frac{1}{1+e^x}+\frac{1}{1+e^{-x}}=1$（后者分子分母同乘 $e^x$），保留的因子 $\frac{1}{1+x^2}$ → $2I=\int_{-1}^{1}\frac{\mathrm dx}{1+x^2}=\frac{\pi}{2}$ |
| 例 7 类题 2 $\int_{\pi/6}^{\pi/3}\frac{\cos^2x}{x(\pi-2x)}\mathrm dx$ | $\frac{\ln 2}{\pi}$ | $a+b=\frac{\pi}{2}$，配对 $x\to\frac{\pi}{2}-x$：分母 $x(\pi-2x)$ **配对后不变**，分子 $\cos^2x\to\sin^2x$，相加为 $1$ → $2I=\int_{\pi/6}^{\pi/3}\frac{\mathrm dx}{x(\pi-2x)}$，拆项 $\frac{1}{\pi}\left(\frac1x+\frac{2}{\pi-2x}\right)$，原函数 $\frac1\pi\ln\frac{x}{\pi-2x}$，端点 $x=\frac\pi3$ 处 $\ln1=0$、$x=\frac\pi6$ 处 $\ln\frac14=-2\ln2$ |
| 例 7 类题 3 $\int_{-\pi}^{\pi}\frac{x\sin x\arctan e^x}{1+\cos^2x}\mathrm dx$ | $\frac{\pi^3}{8}$ | **三级链条**：① $x\to-x$ 配对 + $\arctan e^x+\arctan e^{-x}=\frac\pi2$，系数 $\frac\pi2$；② 余下 $\frac{x\sin x}{1+\cos^2x}$ 为偶函数，折半系数 $2$；③ $\int_0^\pi xf(\sin x)\mathrm dx=\frac\pi2\int_0^\pi f(\sin x)\mathrm dx$，系数 $\frac\pi2$；收口 $\int_0^\pi\frac{\sin x\mathrm dx}{1+\cos^2x}=\left[\arctan(\cos x)\right]^\pi_0$ 取绝对值 = $\frac\pi2$ → $I=\frac12\cdot\frac\pi2\cdot2\cdot\frac\pi2\cdot\frac\pi2=\frac{\pi^3}{8}$ |
| 例 7 类题 4 $\int_{-\pi/2}^{\pi/2}\cos^4x\ln\left(x+\sqrt{4+x^2}\right)\mathrm dx$ | $\frac{3\pi\ln 2}{8}$ | $x\to-x$ 配对相加：$\ln\left(x+\sqrt{4+x^2}\right)+\ln\left(-x+\sqrt{4+x^2}\right)=\ln 4$（两真数相乘 $=(4+x^2)-x^2=4$）→ $2I=\ln4\int_{-\pi/2}^{\pi/2}\cos^4x\mathrm dx=2\ln2\cdot2\cdot\frac{3\pi}{16}=\frac{3\pi\ln2}{4}$ → $I=\frac{3\pi\ln2}{8}$ |
| 例 8 $\int_0^{\pi/2}\ln(\sin x)\mathrm dx$ | $-\frac{\pi}{2}\ln 2$ | **配对折回自身**：$x\to\frac{\pi}{2}-x$ 得 $I=\int_0^{\pi/2}\ln(\cos x)\mathrm dx$（$\sin$ 变 $\cos$）→ 相加 $2I=\int_0^{\pi/2}\ln(\sin x\cos x)\mathrm dx=\int_0^{\pi/2}\ln(\sin2x)\mathrm dx-\frac{\pi}{2}\ln2$ → 换元 $u=2x$ 且 $\int_0^\pi\ln\sin u\mathrm du=2\int_0^{\pi/2}\ln\sin u\mathrm du$，第一项折回 $I$ → $2I=I-\frac{\pi}{2}\ln2$ → $I=-\frac{\pi}{2}\ln2$ |
| 例 18 $f(x)=x^2-x\int_0^2f+2\int_0^1f$ | $f(x)=x^2-\frac43x+\frac23$ | 「定积分的结果是一个数」：两个积分值各当一个待定常数，分别对 $[0,1]$、$[0,2]$ 各积一次得二元一次方程组（$\int_0^1f=\frac13$、$\int_0^2f=\frac43$） |
| 例 19 $f=x+\int_0^\pi f\sin^5x\,\mathrm dx$，求 $\int_0^\pi f\cos^4x\,\mathrm dx$ | $-\frac{45\pi^2}{16}$ | 常数 $A=\int_0^\pi f\sin^5x\,\mathrm dx$ → $f=x+A$ → 代回得 $A=\frac{8\pi}{15}+\frac{16}{15}A=-8\pi$；$\int_0^\pi t\sin^5t\,\mathrm dt$ 按权重的配对折半（$\int_0^\pi\sin^5=\frac{16}{15}$），$\int_0^\pi\cos^4=\frac{3\pi}{8}$ 用点火公式 |
| 例 20 $f=3x^2+1+\int_0^1g$、$g=-x+6x^2\int_0^1f$ | $f=3x^2-\frac52$、$g=-x-9x^2$ | 同套路：$\int_0^1f=-\frac32$、$\int_0^1g=-\frac72$，均为负也照样代回 |
| 例 21 $\int_0^1x^m(\ln x)^n\,\mathrm dx$ | $\frac{(-1)^nn!}{(m+1)^{n+1}}$ | 分部积分（对数幂放求导端降次）：$I_{m,n}=-\frac n{m+1}I_{m,n-1}$，$I_{m,0}=\frac1{m+1}$；边界靠 $\lim_{x\to0^+}x^{m+1}(\ln x)^n=0$ |
| 例 22 点火公式（填写并推导） | $\int_0^{\pi/2}\sin^mx\cos^nx\,\mathrm dx=\frac{(m-1)!!(n-1)!!}{(m+n)!!}k$；$m,n$ 同偶 $k=\frac\pi2$，否则 $k=1$ | 分部积分得 $(m+n)I_{m,n}=(m-1)I_{m-2,n}$，降幂至 $I_{1,n}=\frac1{n+1}$、$I_{0,n}=\frac{(n-1)!!}{n!!}$ 收口；$x\mapsto\frac\pi2-x$ 给 $I_{m,n}=I_{n,m}$ |
| 例 23 $J_n=\int_0^{\pi/4}\tan^nx\,\mathrm dx$ | $J_n+J_{n-2}=\frac1{n-1}$；$\frac1{2(n+1)}<J_n<\frac1{2(n-1)}$；$\lim nJ_n=\frac12$ | $\tan^{n-2}x(1+\tan^2x)\mathrm dx=\tan^{n-2}x\,\mathrm d(\tan x)$ → $t=\tan x$ 上限 1（等价 $J_n=\int_0^1\frac{t^n}{1+t^2}\mathrm dt$）；上下界用 $J_n<J_{n-2}$、$J_{n+2}<J_n$ 各配一条递推 |
| 例 24 $a_n=\int_0^1x^n\sqrt{1-x^2}\,\mathrm dx$ | $a_n=\frac{n-1}{n+2}a_{n-2}$；$\lim\frac{a_n}{a_{n-1}}=1$ | 分部积分（积分端 $x\sqrt{1-x^2}\mathrm dx\to-\frac13(1-x^2)^{3/2}$，$n\ge2$ 边界为 0）→ $a_n=\frac{n-1}{3}(a_{n-2}-a_n)$；比式极限夹逼 $\frac{n-1}{n+2}<\frac{a_n}{a_{n-1}}<1$ |
| 例 8 类题 $\int_0^1\frac{\ln(1+x)}{1+x^2}\mathrm dx$ 与 $\int_0^1\frac{\arctan x}{1+x}\mathrm dx$ | 均为 $\frac{\pi\ln 2}{8}$ | 第一题：$x=\tan\theta$ → $\int_0^{\pi/4}\ln(1+\tan\theta)\mathrm d\theta$ → 配对 $\theta\to\frac\pi4-\theta$，由 $1+\tan\left(\frac\pi4-\theta\right)=\frac{2}{1+\tan\theta}$ 得配对式 $=\frac\pi4\ln2-I$ → $2I=\frac\pi4\ln2$。第二题：对 $\arctan x$ 分部积分（$v=\ln(1+x)$）得 $\frac\pi4\ln2-I$，与第一题同值 |
| 例 9 $\int_0^{n\pi}x|\sin x|\mathrm dx$（$n$ 为正整数） | $n^2\pi$ | **配对 + 周期性**：$x\to n\pi-x$ 且 $\|\sin(n\pi-x)\|=\|\sin x\|$ → $2I=n\pi\int_0^{n\pi}\|\sin x\|\mathrm dx$；$\|\sin x\|$ 以 $\pi$ 为周期、每周期 $2$，故 $\int_0^{n\pi}=2n$ → $2I=2n^2\pi$ → $I=n^2\pi$。**等价视角**：逐段 $x=k\pi+t$，第 $k$ 段贡献 $2k\pi+\pi=(2k+1)\pi$，拱面积成等差数列 $1,3,5,\dots$，前 $n$ 项和 $=n^2$ |
| 例 10（2006）$f$ 分段给出，求 $F(x)=\int_{-1}^{x}f(t)\mathrm dt$ | $x<0$ 时 $\frac{x^{3}}{2}+x^{2}-\frac{1}{2}$；$x\ge0$ 时 $x-\frac{x}{e^{x}+1}-\ln(1+e^{x})+\ln 2-\frac{1}{2}$ | **变限积分分两段**：① $x<0$ 时 $F=\int_{-1}^{x}(2t+\frac32t^2)\mathrm dt=\frac{x^3}{2}+x^2-\frac12$；② $x\ge0$ 时拆成 $\int_{-1}^{0}+\int_0^x$，前一截 $=-\frac12$，后一截用分部积分（$u=t$、$v=-\frac{1}{e^t+1}$）得 $x-\frac{x}{e^x+1}-\ln(1+e^x)+\ln2$，故 $F=x-\frac{x}{e^x+1}-\ln(1+e^x)+\ln2-\frac12$。两段在 $x=0$ 同取 $-\frac12$，$F$ 连续 |

| 例 11 $f(x)=\int_0^1\|t^2-x^2\|\mathrm dt$（$x>0$），求 $f'$ 与最小值 | $0<x<1$ 时 $f=\frac{4x^3}{3}-x^2+\frac13$、$f'=4x^2-2x$；$x\ge1$ 时 $f=x^2-\frac13$、$f'=2x$；**最小值 $f\left(\frac12\right)=\frac14$** | **含参绝对值积分**：值零点 $t=x$ 是否落在 $[0,1]$ 决定分界 $x=1$。① $0<x<1$：拆 $\int_0^x+\int_x^1$，前段取 $x^2-t^2$、后段取 $t^2-x^2$，得 $\frac43x^3-x^2+\frac13$；② $x\ge1$：$t^2-x^2\le0$ 恒成立，得 $x^2-\frac13$。两段在 $x=1$ 同为 $\frac23$。求导后 $f'=2x(2x-1)$，驻点 $x=\frac12$，$f''>0$，且 $x\ge1$ 段最小值 $\frac23>\frac14$ |

| 例 12（1995）$f(x)=\int_0^x\frac{\sin t}{\pi-t}\mathrm dt$，求 $\int_0^\pi f(x)\mathrm dx$ | $2$ | **交换积分次序**：内层 $f$ 无初等原函数（$f(\pi)=\mathrm{Si}(\pi)\approx1.8519$），故换序 → $\int_0^\pi\frac{\sin t}{\pi-t}\mathrm dt\int_t^\pi\mathrm dx=\int_0^\pi\frac{\sin t}{\pi-t}(\pi-t)\mathrm dt=\int_0^\pi\sin t\,\mathrm dt=2$。等价走法：对 $\int_0^\pi f$ 分部积分，端点项 $\pi f(\pi)$ 与被减积分合并为 $\int_0^\pi\frac{(\pi-t)\sin t}{\pi-t}\mathrm dt$，同样得 2 |

| 例 12 类题 1（2013）$f(x)=\int_1^x\frac{\ln(1+t)}{t}\mathrm dt$，求 $\int_0^1\frac{f(x)}{\sqrt x}\mathrm dx$ | $8-2\pi-4\ln 2$（$\approx-1.0558$） | 两条等价路：① 换序（区域 $0\le x\le t\le1$）得 $-2\int_0^1\frac{\ln(1+t)}{\sqrt t}\mathrm dt$；② 分部积分（$v=2\sqrt x$，端点项为 $0$）直接得同一式 → 再换元 $t=u^2$ 化为 $-4\int_0^1\ln(1+u^2)\mathrm du$ → 对 $\ln(1+u^2)$ 分部得 $\ln2-2+\frac\pi2$ → 乘 $-4$ 即 $8-2\pi-4\ln2$ |

| 例 12 类题 2（2019）$f(x)=x\int_1^x\frac{\sin(t^2)}{t}\mathrm dt$，求 $\int_0^1f(x)\mathrm dx$ | $\frac{\cos 1-1}{4}=-\frac{1-\cos 1}{4}$（$\approx-0.1149$） | $f$ 在 $(0,1)$ 上恒负，故结果带负号。换序（区域 $0\le x\le t\le1$）：$-\int_0^1\frac{\sin(t^2)}{t}\left(\int_0^t x\mathrm dx\right)\mathrm dt=-\frac12\int_0^1 t\sin(t^2)\mathrm dt$ → 换元 $u=t^2$ 得 $-\frac14\int_0^1\sin u\,\mathrm du=\frac{\cos1-1}{4}$。内层权的 $x$ 一旦被积成 $\frac{t^2}{2}$，$\frac{t^2}{t}=t$ 就把分母消灭 |

| 例 13 $f(x)=\int_1^x\frac{\arctan t}{(1+t^2)^{3/2}\ln(1+t^2)}\mathrm dt$，求 $\int_0^1\frac{x}{1+x^2}f(x)\mathrm dx$ | $\frac{8-\sqrt2(4+\pi)}{16}=\frac12-\frac{\sqrt2}{4}\left(1+\frac\pi4\right)$（$\approx-0.1312$） | **先分部、再换元**：取 $u=f(x)$、$\mathrm dv=\frac{x\mathrm dx}{1+x^2}$、$v=\frac12\ln(1+x^2)$，端点项 $=0$（$f(1)=0$、$\ln1=0$），于是 $I=-\frac12\int_0^1\ln(1+x^2)\cdot\frac{\arctan x}{(1+x^2)^{3/2}\ln(1+x^2)}\mathrm dx=-\frac12\int_0^1\frac{\arctan x}{(1+x^2)^{3/2}}\mathrm dx$——**设计好的分母 $\ln(1+x^2)$ 被权重的原函数整体约掉**。再令 $x=\tan\theta$ 得 $\int_0^{\pi/4}\theta\cos\theta\,\mathrm d\theta=\frac{\sqrt2}{2}\left(1+\frac\pi4\right)-1$，乘 $-\frac12$ 即答案 |

| 例 14（$f'(x)=\arctan(x-1)^2$、$f(0)=0$）求 $\int_0^1f(x)\mathrm dx$ | $\frac{\pi-2\ln 2}{8}=\frac\pi8-\frac{\ln2}{4}$（$\approx0.2194$） | 由 $f(0)=0$ 写成 $f(x)=\int_0^xf'(t)\mathrm dt$ → 换序（区域 $0\le t\le x\le1$）内层长度 $1-t$ → $\int_0^1(1-t)\arctan(t-1)^2\mathrm dt$ → 换元 $u=1-t$ 得 $\int_0^1u\arctan(u^2)\mathrm du$ → 再令 $v=u^2$ 得 $\frac12\int_0^1\arctan v\,\mathrm dv=\frac12\left(\frac\pi4-\frac{\ln2}{2}\right)$。**等价快路**：直接分部 $I=\left[xf(x)\right]_0^1-\int_0^1xf'(x)\mathrm dx=f(1)-\int_0^1x\arctan(x-1)^2\mathrm dx$，两式合并即 $\int_0^1(1-x)\arctan(x-1)^2\mathrm dx$ |

| 例 14 类题（2016，$f$ 是 $\frac{\cos x}{2x-3\pi}$ 的原函数、$f(0)=0$）求平均值并证唯一零点 | 平均值 $\frac{1}{3\pi}$；$\left(0,\frac{3\pi}{2}\right)$ 内唯一零点 | (1) 分部积分：$\int_0^{a}f=\left[xf(x)\right]_0^a-\int_0^axf'(x)\mathrm dx$，用 $f(0)=0$ 与 $f(a)=\int_0^af'$ 把端点项并入积分，得 $\int_0^a\frac{(a-x)\cos x}{2x-3\pi}\mathrm dx$，而 $a=\frac{3\pi}{2}$ 时 $\frac{a-x}{2x-3\pi}=-\frac12$，故 $\int_0^af=-\frac12\int_0^a\cos x\mathrm dx=\frac12$，平均值 $=\frac{1}{a}\cdot\frac12=\frac{1}{3\pi}$。(2) $f'=\frac{\cos x}{2x-3\pi}$ 分母为负，故 $f'$ 与 $\cos x$ **反号**：$(0,\frac\pi2)$ 上递减、$(\frac\pi2,\frac{3\pi}{2})$ 上递增，$f(\frac\pi2)<0$ 是全局最小。若 $f(a)\le0$，则 $f\le0$ 于 $[0,a]$ 且 $f<0$ 于 $(0,\frac\pi2)$，与 $\int_0^af=\frac12>0$ 矛盾；故 $f(a)>0$，结合严格单调在中段恰有一个零点 |

| 例 15（$\int_0^2f=4$、$f'(2)=1$、$f(2)=2$）求 $\int_0^1x^2f''(2x)\mathrm dx$ | $\frac12$ | **换元归一 + 两次分部降阶**：$t=2x$ 得 $\frac18\int_0^2t^2f''(t)\mathrm dt$；第一次分部 $=\frac18\left\{\left[t^2f'\right]_0^2-\int_0^22tf'\mathrm dt\right\}$（用 $f'(2)=1$ 得 $4$）；第二次分部把 $\int_0^22tf'\mathrm dt=\left[2tf\right]_0^2-\int_0^22f\mathrm dt=4\cdot2-2\cdot4=0$（用 $f(2)=2$ 与 $\int_0^2f=4$）。故 $\int_0^2t^2f''\mathrm dt=4$，乘 $\frac18$ 得 $\frac12$。三个已知数恰好各用一次 |

| 例 16（已知 $\int_0^\pi\frac{\cos x}{(x+2)^2}\mathrm dx=A$，求 $\int_0^{\pi/2}\frac{\sin 2x}{x+1}\mathrm dx$） | $\frac12+\frac{1}{\pi+2}-A$ | **换元配族 + 分部对号入座**：$x=\frac y2$ 使 $\frac{1}{x+1}\to\frac{2}{y+2}$、$\mathrm dx\to\frac{\mathrm dy}2$（系数抵消），化为 $\int_0^\pi\frac{\sin y}{y+2}\mathrm dy$；再分部（$u=\frac{1}{y+2}$、$\mathrm dv=\sin y\,\mathrm dy$、$v=-\cos y$）得 $\left[-\frac{\cos y}{y+2}\right]_0^\pi-\int_0^\pi\frac{\cos y}{(y+2)^2}\mathrm dy=\frac{1}{\pi+2}+\frac12-A$。分子若为 $\sin x\cos x=\frac12\sin2x$，答案为上式的一半 |
| ⚠️ 题面辨析（例 16） | — | 若分子写作 $\sin x+\cos x$，**答案不由 $A$ 决定**：换元后分子成 $\sin\frac y2+\cos\frac y2$，分部后冒出 $\frac{\cos\frac y2-\sin\frac y2}{(y+2)^2}$，与已知的 $\frac{\cos y}{(y+2)^2}$ 对不上。数值佐证：$A=0.11201192$、$\frac{1}{\pi+2}=0.19449580$；目标值 $1.19465356$，而 $\frac{2}{\pi+2}+1-2A=1.16496069$（差 $3\times10^{-2}$）、$1+\frac{1}{\pi+2}-A=1.27697261$（差 $8\times10^{-2}$），无任何简单组合吻合。可解版本的分子必须是 $\sin2x$ 或 $\sin x\cos x$ |

| 例 16 类题 1（已知 $\int_0^{+\infty}\frac{\sin x}{x}=\frac\pi2$，求 $\int_0^{+\infty}\frac{\sin^2x}{x^2}\mathrm dx$） | $\frac{\pi}{2}$ | 分部（$u=\sin^2x$、$\mathrm dv=\frac{\mathrm dx}{x^2}$、$v=-\frac1x$），端点项 $-\frac{\sin^2x}{x}$ 在 $0$ 与 $\infty$ 处均趋于 $0$；余项 $\int_0^\infty\frac{2\sin x\cos x}{x}\mathrm dx$ 用倍角化为 $\frac{\sin2x}{x}$，换元 $t=2x$ 即回到已知积分 |
| 例 16 类题 2（$\int_{-\pi/2}^{\pi/2}f(x\cos x)\cos x\mathrm dx=1$，求 $\int_{-\pi/2}^{\pi/2}f(x\cos x)x\sin x\mathrm dx$） | $1$ | 被积函数为偶（$f(x\cos x)$ 偶、$x\sin x$ 偶）→ 折半到 $[0,\frac\pi2]$；用 $x\sin x=\cos x-\frac{\mathrm d}{\mathrm dx}(x\cos x)$ 拆项，**全微分项** $\int_0^{\pi/2}f(x\cos x)\mathrm d(x\cos x)=\int_0^{0}f(u)\mathrm du=0$（因 $x\cos x$ 在 $x=0$ 与 $x=\frac\pi2$ 处都为 $0$），剩下的一半正是条件 $=1$ |

| 例 17（2023 改编，$f(x+2)-f(x)=\sin x$、$\int_0^2f=0$）求 $\int_1^3f$ | $1-\cos 1$（$\approx0.4597$） | $x=t+2$：$\int_1^3f=\int_{-1}^1[f(t)+\sin t]\mathrm dt=\int_{-1}^1f\mathrm dt$（$\sin$ 在对称区间积为 0）；再用 $\int_0^2f=0$ 与关系式在 $[-1,0]$ 上的积分 $\int_1^2f=\int_{-1}^0f+(\cos1-1)$，得 $\int_{-1}^1f=1-\cos1$ |
| 例 17 类题（$f(x+3)-f(x)=2x$、$\int_0^3f=2$）求 $\int_1^4f$ | $3$ | $x=t+3$：$\int_1^4f=\int_{-2}^1[f(t)+2t]\mathrm dt=\int_{-2}^1f\mathrm dt-3$；再用关系式在 $[-2,0]$ 上积分 $\int_1^3f=\int_{-2}^0f-4$ 与已知 $\int_0^3f=2$，得 $\int_{-2}^1f=6$，目标 $=6-3=3$ |

## 三、通用判据

- **权重的配对**：$[0,\pi]$ 上形如「$x$ × 关于 $\frac\pi2$ 对称的因子」→ 配对 $x$ 与 $\pi-x$，权重变常数 $\frac\pi2$。判断「因子只依赖 $\sin x$」的方法是把 $|\cos x|$ 写成 $\sqrt{1-\sin^2x}$；没有绝对值时 $\cos x$ 不被 $\sin x$ 决定，公式作废。
- **对称性三步**：① 先平移，把对称中心（或对称轴）搬到原点／区间端点搬到原点；② 再查奇偶，奇部归零、偶部折半；③ 最后才去绝对值、去根号。
- **绝对值的解除时机**：只在「折半之后、区间单号」时解除。$\sqrt{1-\cos2\pi x}=\sqrt2|\sin\pi x|$、$|\sin x\cos x|$ 这类先写绝对值再分段。
- **点火公式**：$\int_0^{\pi/2}\sin^mx\cos^nx\,\mathrm dx=\frac{(m-1)!!(n-1)!!}{(m+n)!!}k$，$m,n$ 同为偶数时 $k=\frac\pi2$，否则 $k=1$。
- **待定函数（定积分的结果是一个数）**：$f$（或 $f,g$）只藏在若干定积分里 → 把每个不同的定积分值当一个待定常数，代回原式得解析式，再对相应区间各积一次解出常数；解出的数可以为负，原样代回（例 18–20）。
- **分部导出递推（降幂型）**：幂 × 对数幂、$\sin^m\cos^n$、$\tan^n$、$x^n\sqrt{1-x^2}$ 之积一律先试分部积分：一次分部得递推，反复使用到起跳值收口。附带收获：递推式配单调性可直接夹逼出极限（$J_n$、$\frac{a_n}{a_{n-1}}$ 均如此），不必先求通项。
- **同族通式**：$\int_0^\pi\frac{\mathrm dx}{a+b\cos^2x}=\frac{\pi}{\sqrt{a(a+b)}}$（$a>0,\ a+b>0$）。
- **变限积分函数的分段（考法四核心）**：$F(x)=\int_a^x f(t)\mathrm dt$ 的分段表达式，取决于下限 $a$ 落在哪一段。把 $[a,x]$ 按 $f$ 的分段点切成「若干整段 + 一个部分段」：整段的值直接算成常数，部分段保留 $x$（上限含 $x$）。下限所在段用同一段表达式代入 $x=a$ 即可，不必另设。收尾时把两段在分段点处的值对一次（本例同取 $-\frac12$），确认 $F$ 连续。
- **权重 × 周期函数（例 9 族）**：$\int_0^{n\pi}x\,g(x)\mathrm dx$ 中若 $g$ 以 $\pi$ 为周期且满足 $g(n\pi-x)=g(x)$（$\left|\sin x\right|$、$\sin^2x$、$\left|\cos x\right|$ 等），先配对 $x\to n\pi-x$ 把权重换成常数 $\frac{n\pi}{2}$，再用「周期数 × 单周期积分」收口。已验证的两个结果：$\int_0^{n\pi}x\left|\sin x\right|\mathrm dx=n^2\pi$；$\int_0^{n\pi}x\sin^2x\,\mathrm dx=\frac{n^2\pi^2}{4}$。
- **导数的绝对值**：$\int|\varphi'(x)|\,\mathrm dx$ 是 $\varphi$ 的总变差，必须**先求导再管绝对值**；顺序颠倒会退化成 $\varphi(b)-\varphi(a)$（例 6 会得 0）。含 $\ln x$ 时换元 $t=\ln x$，把 $\frac{\mathrm dx}x$ 吸收，落到整流正弦 $|\sin t|$；$|\sin t|$ 以 $\pi$ 为周期，每拱面积 $2$，故 $\int_{e^{-2n\pi}}^{1}\left|\frac{\mathrm d}{\mathrm dx}\cos\ln\frac1x\right|\mathrm dx=4n$。

- **含参定积分求导的顺序（例 11）**：被积函数含参数 $x$ 且带绝对值时，**先把 $f(x)$ 的分段表达式算出来，再对 $x$ 求导**；不要直接对被积函数里的 $x$ 求导。分界点由「绝对值零点与积分区间的位置关系」定（$|t^2-x^2|$ 的零点 $t=x$ 走出 $[0,1]$ 的时刻即 $x=1$）。算出两段后先验证分段点处两段相同，再分段求导、分段找最值并比较。

- **被积函数含变限积分（考法五之一）**：见到 $\int_a^b f(x)\mathrm dx$ 而 $f(x)=\int_c^x g(t)\mathrm dt$，立即换序：把区域 $\{c\le t\le x\le b\}$（或相应三角域）画出来，改成先对 $x$ 积；内层长度常与分母相消（例 12 得 $\pi-t$，把 $\frac{1}{\pi-t}$ 约掉）。判断信号：**内层积分本身积不出来**（如 $\int\frac{\sin t}{\pi-t}\mathrm dt$、$\int\frac{\sin(t^2)}{t}\mathrm dt$）。等价替代：对外层做分部积分，$\left[xf(x)\right]_a^b$ 端点项与余项往往能合并化简。

- **被积函数含导函数（考法五之二，例 15）**：$\int_a^b g(x)f^{(n)}(kx)\mathrm dx$ 型（$g$ 是多项式权重）——先换元 $t=kx$ 把内层归一，再看 $f^{(n)}$ 的阶数决定分部次数（$f''$ 两次、$f'$ 一次），每分部一次降一阶，**端点项与余项分别在每一步注入一个已知数据**（$f'(2)$、$f(2)$、$\int f$）。收尾时检查三个已知数据是否各用一次——若某个数据没用上或用了两次，多半是换元系数或端点代入出错。答案与 $f$ 的具体形状无关（可用两个不同的 $f$ 交叉核验）。

- **已知一个积分求另一个（考法五之三，例 16）**：动作分两步——① **换元配族**：把目标里的 $\frac{1}{x+1}$ 通过 $x=\frac y2$ 变成 $\frac{2}{y+2}$，与被给积分的 $\frac{1}{(y+2)^2}$ 落入同一族（$y+2$）；② **分部对号入座**：取 $\mathrm dv=\sin y\,\mathrm dy$、$v=-\cos y$，让「分子求导」恰好产出被给积分的分子（$\frac{\mathrm d}{\mathrm dy}(-\cos y)=\sin y$），余下的 $\int\frac{\cos y}{(y+2)^2}\mathrm dy$ 正是 $A$。判断能否对号入座的关键：换元后的分子必须是「某初等函数的导数，且该函数与被给积分的分子构成导数—原函数对」。对不上（如 $\sin\frac y2+\cos\frac y2$）则题面有误或需另寻关系。

- **全微分项归零（例 16 类题 2 的核心手法）**：若被积函数中能拆出 $f(g(x))g'(x)$ 且 $g$ 在区间两端取值相同（$g(a)=g(b)$），则 $\int_a^bf(g(x))g'(x)\mathrm dx=\int_{g(a)}^{g(b)}f(u)\mathrm du=0$。识别信号：被积函数含只以 $g=x\cos x$、$\sin x$、$x^2$ 等「偶函数或两端等值的 $g$」形式出现的三角函数，而恒等式（如 $\frac{\mathrm d}{\mathrm dx}(x\cos x)=\cos x-x\sin x$）刚好把讨厌的那一项写成分离形式。常见同族：$\int_0^{\pi/2}f(\sin x)\cos x\,\mathrm dx$、$\int_0^{1}f(x^2)\,2x\,\mathrm dx$。

- **周期型关系式 $f(x+T)-f(x)=g(x)$（例 17 族）**：三步定式——① **平移目标区间**：令 $x=t+T$，把 $[a,a+T]$ 搬到 $[a-T,a]$；② **用关系式换 $f$**：$f(t+T)=f(t)+g(t)$，拆出一个可直接积的项 $\int g$；③ **折回已知**：用已知的 $\int_0^{T}f$ 消去剩下的 $\int f$（$[a-T,a]$ 与 $[0,T]$ 只差一段，按 $\int_{-1}^1=\int_{-1}^0+\int_0^1$ 之类拼接即可）。通解形状为 $f=f_{\text{特}}+h$（$h$ 以 $T$ 为周期），**答案与 $h$ 无关**（$\int_a^{a+T}h=\int_0^Th$ 由周期性保证），可用两个不同的 $h$ 交叉核验。

## 四、考法三的三张常用配对牌

凡「被积函数含下列因子、原函数求不出、区间对称」→ 立刻做 $x\to a+b-x$ 配对，两式相加：

| 因子 | 配对面的和／差 | 结果 |
|---|---|---|
| $\ln(1+e^x)$ | $\ln(1+e^x)-\ln(1+e^{-x})$ | $x$（例 7） |
| $\arctan e^x$ | $\arctan e^x+\arctan e^{-x}$ | $\frac{\pi}{2}$ |
| $\frac{1}{1+e^x}$ | $\frac{1}{1+e^x}+\frac{1}{1+e^{-x}}$ | $1$ |
| $\ln\left(x+\sqrt{a^2+x^2}\right)$ | $\ln\left(x+\sqrt{a^2+x^2}\right)+\ln\left(-x+\sqrt{a^2+x^2}\right)$（两真数相乘） | $\ln a^2$，注意 $a=1$ 时为 $0$ 但 $a\ne1$ 时**常数不为零**（类题 4） |

配套动作：配对式与原式相加、提公因子 $x$（或 $x$ 的线性式），再用上表把因子换成常数，剩下的积分通常退化为幂函数或基本积分。

**第三类出口：配对后折回自身 → 解一次方程。** 当配对相加得到的是「$kI = I + $ 已知量」时，直接解出 $I$（例 8 的 $2I=I-\frac{\pi}{2}\ln2$）。判断信号：配对前后被积函数「同型」（$\sin\leftrightarrow\cos$、$f(x)\leftrightarrow f(a+b-x)$ 只差一个已知函数），或通用形式 $I=\int_a^b\frac{g(x)}{g(x)+g(a+b-x)}\mathrm dx=\frac{b-a}{2}$（配对相加恒得 $1$）。

## 五、数值核验备忘（本题族）

- **嵌套积分数值核验的两个坑**：① 外层被积函数若带权重（如 $\frac{f(x)}{\sqrt x}$），算外层时必须把权重乘进去——漏乘会得到一个「干净」的假值（2013 类题漏乘 $1/\sqrt x$ 时得 $1-2\ln2$，看似合理却对应另一个积分 $\int_0^1f$）；② 外层被积函数在端点发散时（如 $x^{-1/2}$），先换元 $x=s^2$ 把发散因子吸收掉再积，$I=\int_0^1\frac{f(x)}{\sqrt x}\mathrm dx=2\int_0^1f(s^2)\mathrm ds$。

- 含 $|\sin\pi x|$、$|\sin x\cos x|$ 的被积函数在 $0,\frac\pi2,\pi$ 等点取零，自适应 Simpson 会在「端点与中点全为零」时假收敛返回 0；**必须在折点处分段**再积（例 5 变体 2 曾因此报 0，分段后得 $\frac{\pi^2}{2}$，误差 $9\times10^{-16}$）。
