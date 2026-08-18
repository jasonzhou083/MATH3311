import hashlib
import io
from pathlib import Path

from PIL import Image
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, FrameBreak, Image as RLImage, PageTemplate, Paragraph, Spacer
from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[2]
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf" / "MATH3311_cheat_sheet_A4_front_back.pdf"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
DV_DIR = ROOT / "tmp" / "pdfs" / "vendor" / "matplotlib" / "mpl-data" / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("Arial", str(DV_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(DV_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(DV_DIR / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", str(DV_DIR / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFontFamily(
    "Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-BoldItalic"
)

NAVY = colors.HexColor("#102A43")
BLUE = colors.HexColor("#0B5FA5")
TEAL = colors.HexColor("#00796B")
RED = colors.HexColor("#B42318")
PURPLE = colors.HexColor("#6B3FA0")
GOLD = colors.HexColor("#8A5A00")
PALE_BLUE = colors.HexColor("#DDEEFF")
PALE_TEAL = colors.HexColor("#DDF4EE")
GRID = colors.HexColor("#AAB7C4")
TEXT = colors.HexColor("#16212B")

MATH_DPI = 450
MATH_FONT_SIZE = 6.35
MATH_DIR = TMP / "math_assets"
MATH_PAD_TOP_PT = 2.9
MATH_PAD_BOTTOM_PT = 1.3

PAGE_W, PAGE_H = landscape(A4)
MARGIN_X = 10.0
BOTTOM = 9.0
HEADER_H = 23.0
GAP = 6.0
COLS = 4
FRAME_H = PAGE_H - BOTTOM - HEADER_H - 3.0
COL_W = (PAGE_W - 2 * MARGIN_X - (COLS - 1) * GAP) / COLS


TEX = {
    "fpn": r"\mathrm{fl}(x)=\pm(1.d_1d_2\ldots d_p)_2\,2^e",
    "epsilon": r"\varepsilon=2^{-52}\approx2.22\times10^{-16}",
    "fpn_limits": r"\varepsilon_i=2^m\varepsilon\ (2^m\leq i<2^{m+1}),\quad x_{\max}=(2-\varepsilon)2^{1023},\quad x_{\min}^{\mathrm{normal}}=2^{-1022}",
    "errors": r"e_a=|\bar x-x|,\qquad e_r=\frac{|\bar x-x|}{|x|}",
    "sigfig": r"e_r<\frac{1}{2}\,10^{-p}",
    "quadratic": r"q=-\frac{1}{2}\!\left(b+\operatorname{sign}(b)\sqrt{b^2-4ac}\right),\qquad x_1=\frac{q}{a},\quad x_2=\frac{c}{q}",
    "storage_cost": r"\mathrm{memory}(n\!\times\!n)=8n^2\ \mathrm{bytes},\qquad \mathrm{flops}(AB)=n^2(2n-1)\approx2n^3",
    "vnorm": r"\Vert x\Vert_p=\left(\sum_{i=1}^{n}|x_i|^p\right)^{1/p}",
    "special_norms": r"\Vert x\Vert_1=\sum_i|x_i|,\qquad\Vert x\Vert_2=\sqrt{x^{\mathsf{T}}x},\qquad\Vert x\Vert_\infty=\max_i|x_i|",
    "numeric_equal": r"x=y\Longleftrightarrow\Vert x-y\Vert=0,\qquad\Vert x-y\Vert\leq\tau(\varepsilon,n,\Vert x\Vert,\Vert y\Vert)",
    "vector_error": r"e_a=\Vert\bar x-x\Vert,\qquad e_r=\frac{\Vert\bar x-x\Vert}{\Vert x\Vert}",
    "vector_sigfig": r"\frac{\Vert\bar x-x\Vert_\infty}{\Vert x\Vert_\infty}<\frac{1}{2}\,10^{-k},\qquad k=\left\lfloor-\log_{10}(2e_{r,\infty})\right\rfloor",
    "mnorm": r"\Vert A\Vert_p=\max_{x\ne0}\frac{\Vert Ax\Vert_p}{\Vert x\Vert_p}",
    "kappa": r"\kappa(A)=\Vert A\Vert\,\Vert A^{-1}\Vert\geq1",
    "perturb": r"\frac{\Vert\delta x\Vert}{\Vert x\Vert}\leq\alpha\kappa(A)(\rho_A+\rho_b)",
    "mnorm_props": r"\Vert Ax\Vert_p\leq\Vert A\Vert_p\Vert x\Vert_p,\qquad\Vert AB\Vert_p\leq\Vert A\Vert_p\Vert B\Vert_p",
    "named_mnorms": r"\Vert A\Vert_1=\max_j\sum_i|a_{ij}|,\quad\Vert A\Vert_\infty=\max_i\sum_j|a_{ij}|,\quad\Vert A\Vert_2=\sqrt{\lambda_{\max}(A^{\mathsf{T}}A)}=\sigma_1",
    "kappa_specs": r"\kappa_2(A)=\frac{\max_i|\lambda_i|}{\min_i|\lambda_i|}\ (A=A^{\mathsf{T}}),\qquad\kappa_2(A)=\frac{\sigma_1}{\sigma_n}\ (\mathrm{rank}(A)=n)",
    "rho_defs": r"\rho_A=\frac{\Vert\delta A\Vert}{\Vert A\Vert},\qquad\rho_b=\frac{\Vert\delta b\Vert}{\Vert b\Vert}",
    "perturbed_system": r"(A+\delta A)(x+\delta x)=b+\delta b,\qquad\Vert(A+\delta A)^{-1}\Vert\leq\alpha\Vert A^{-1}\Vert",
    "covariance": r"C_{ij}=E[(X_i-\mu_i)(X_j-\mu_j)],\qquad C_{ii}=\sigma_i^2",
    "correlation": r"K_{ij}=\frac{C_{ij}}{\sigma_i\sigma_j},\qquad K=\Sigma^{-1}C\Sigma^{-1},\qquad K_{ii}=1",
    "triangular": r"\det A=\prod_i a_{ii},\qquad A\ \mathrm{nonsingular}\Longleftrightarrow a_{ii}\ne0\ \forall i",
    "banded": r"a_{ij}=0\quad\mathrm{if}\quad i-j>m_\ell\ \mathrm{or}\ j-i>m_u",
    "sym_split": r"A=\frac{A+A^{\mathsf{T}}}{2}+\frac{A-A^{\mathsf{T}}}{2}",
    "orthogonal": r"Q^{\mathsf{T}}Q=I,\qquad Q^{-1}=Q^{\mathsf{T}},\qquad\kappa_2(Q)=1,\qquad\Vert Qx\Vert_2=\Vert x\Vert_2",
    "diag_dom": r"|a_{ii}|>\sum_{j\ne i}|a_{ij}|",
    "plu": r"PA=LU",
    "chol": r"A=R^{\mathsf{T}}R",
    "qrp": r"AP=Q\left[\genfrac{}{}{0}{0}{R}{0}\right]",
    "svd": r"A=U\left[\genfrac{}{}{0}{0}{\Sigma}{0}\right]V^{\mathsf{T}}",
    "qr_economy": r"A=Q\left[\genfrac{}{}{0}{0}{R}{0}\right]=YR,\qquad Q=[Y\ Z],\qquad Q^{\mathsf{T}}Q=I",
    "svd_sums": r"A=\sum_{j=1}^{r}\sigma_ju_jv_j^{\mathsf{T}},\qquad Av_i=\sigma_iu_i,\qquad u_i^{\mathsf{T}}A=\sigma_iv_i^{\mathsf{T}}",
    "normal": r"A^{\mathsf{T}}Ax^*=A^{\mathsf{T}}y",
    "residual": r"r_i(x)=\phi(x;t_i)-y_i,\qquad x^*=\arg\min_x\Vert r(x)\Vert_p",
    "linear_residual": r"\phi(x;t)=\sum_jx_j\phi_j(t),\qquad A_{ij}=\phi_j(t_i),\qquad r=Ax-y",
    "lp_l1": r"\min\sum_i v_i:\quad-v_i\leq r_i\leq v_i,\quad v_i\geq0",
    "lp_linf": r"\min v:\quad-v\leq r_i\leq v,\quad v\geq0",
    "ls_qr": r"R(P^{\mathsf{T}}x^*)=Y^{\mathsf{T}}y",
    "ls_svd": r"x^*=V\Sigma^{-1}Y^{\mathsf{T}}y,\qquad x_{\min}^*=V\Sigma^+Y^{\mathsf{T}}y",
    "c2": r"s\in C^2[a,b]",
    "polynomial": r"p(t)=\sum_{k=0}^{n}a_kt^k=a_0+t\!\left(a_1+t\!\left(a_2+\cdots+t(a_{n-1}+ta_n)\right)\right)",
    "spline_join": r"s_i(t_i)=s_{i+1}(t_i),\quad s_i'(t_i)=s_{i+1}'(t_i),\quad s_i''(t_i)=s_{i+1}''(t_i)",
    "spline_bc": r"\mathrm{natural}:s''(a)=s''(b)=0;\quad\mathrm{clamped}:s'(a),s'(b);\quad\mathrm{not\!\!-\!a\!\!-\!knot}:s_1'''(t_1)=s_2'''(t_1),\ s_{n-1}'''(t_{n-1})=s_n'''(t_{n-1})",
    "spline": r"s_i(t)=\frac{M_{i-1}(t_i-t)^3}{6h}+\frac{M_i(t-t_{i-1})^3}{6h}+\left(\frac{y_{i-1}}{h}-\frac{M_{i-1}h}{6}\right)(t_i-t)+\left(\frac{y_i}{h}-\frac{M_ih}{6}\right)(t-t_{i-1})",
    "spline_system": r"\frac{h}{6}M_{i-1}+\frac{2h}{3}M_i+\frac{h}{6}M_{i+1}=d_{i+1}-d_i",
    "bvp": r"-\frac{U_{j+1}-2U_j+U_{j-1}}{(\Delta x)^2}=f(x_j)",
    "bvp_setup": r"-u''=f\ \mathrm{on}\ (0,1),\quad u(0)=\alpha,\quad u(1)=\beta,\quad x_j=j\Delta x,\quad\Delta x=\frac{1}{n+1}",
    "hidden_sparse": r"(I+BB^{\mathsf{T}})x=x+B(B^{\mathsf{T}}x),\qquad B\in R^{n\times r},\quad r\ll n",
    "periodic": r"g(t+T)=g(t),\qquad f=\frac{1}{T},\qquad \cos(\omega t):T=\frac{2\pi}{\omega}",
    "trig_poly": r"g_n(t)=a_0+\sum_{k=1}^{n}\left[a_k\cos\!\left(\frac{2\pi kt}{T}\right)+b_k\sin\!\left(\frac{2\pi kt}{T}\right)\right]",
    "fourier_a0": r"a_0=\frac{1}{T}\int_{-T/2}^{T/2}g(t)\,dt",
    "fourier_ak": r"a_k=\frac{2}{T}\int_{-T/2}^{T/2}g(t)\cos\!\left(\frac{2\pi kt}{T}\right)dt",
    "fourier_bk": r"b_k=\frac{2}{T}\int_{-T/2}^{T/2}g(t)\sin\!\left(\frac{2\pi kt}{T}\right)dt",
    "fourier_ck": r"c_k=\frac{1}{T}\int_{-T/2}^{T/2}g(t)e^{-i2\pi kt/T}\,dt",
    "complex_series": r"g(t)=\sum_{k\in Z}c_ke^{i2\pi kt/T},\qquad c_k=\frac{a_k-ib_k}{2},\quad c_{-k}=\frac{a_k+ib_k}{2}",
    "dft": r"\widehat y_k=\sum_{j=0}^{n-1}y_je^{-i2\pi jk/n}=\sum_{j=0}^{n-1}y_j\omega^{-jk}",
    "idft": r"y_j=\frac{1}{n}\sum_{k=0}^{n-1}\widehat y_ke^{i2\pi jk/n}",
    "dft_symmetry": r"y_j\in R:\quad\widehat y_{n-k}=\overline{\widehat y_k},\qquad\widehat y_0\in R,\qquad\widehat y_{n/2}\in R\ (n\ \mathrm{even})",
    "power": r"p_k=\frac{|\widehat y_k|^2}{n}",
    "sample_coeffs": r"A_0=\frac{\widehat y_0}{n},\qquad A_k=\frac{2\operatorname{Re}(\widehat y_k)}{n},\qquad B_k=-\frac{2\operatorname{Im}(\widehat y_k)}{n}",
    "bs_call": r"c=SN(d_1)-Ke^{-r\tau}N(d_2)",
    "bs_d": r"d_1=\frac{\ln(S/K)+r\tau}{\sigma\sqrt{\tau}}+\frac{1}{2}\sigma\sqrt{\tau},\qquad d_2=d_1-\sigma\sqrt{\tau}",
    "normal_cdf": r"N(x)=\frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x}e^{-\xi^2/2}\,d\xi",
    "implied": r"f(\sigma)=c(\sigma)-c_{\mathrm{mkt}}=0,\qquad f'(\sigma)=SN'(d_1)\sqrt{\tau}>0",
    "call_bounds": r"\max\!\left(S-Ke^{-r\tau},0\right)\leq c_{\mathrm{mkt}}\leq S",
    "implied_limits": r"f(0^+)=\max(S-Ke^{-r\tau},0)-c_{\mathrm{mkt}},\qquad f(\infty)=S-c_{\mathrm{mkt}}",
    "taylor": r"f(x+h)=\sum_{k=0}^{n}\frac{h^k}{k!}f^{(k)}(x)+O(h^{n+1})",
    "fd_first": r"f'(x)=\frac{f(x+h)-f(x)}{h}+O(h)=\frac{f(x)-f(x-h)}{h}+O(h)",
    "fd_central": r"f'(x)=\frac{f(x+h)-f(x-h)}{2h}+O(h^2)",
    "fd_second": r"f''(x)=\frac{f(x+h)-2f(x)+f(x-h)}{h^2}+O(h^2)",
    "fd_rounding": r"O(h)+O(\varepsilon/h):h\asymp\varepsilon^{1/2};\quad O(h^2)+O(\varepsilon/h):h\asymp\varepsilon^{1/3};\quad O(h^2)+O(\varepsilon/h^2):h\asymp\varepsilon^{1/4}",
    "convergence": r"e^{(k)}=x^{(k)}-x^*,\qquad\beta=\lim_{k\to\infty}\frac{e^{(k+1)}}{(e^{(k)})^\nu}",
    "newton": r"x^{(k+1)}=x^{(k)}-\frac{f(x^{(k)})}{f'(x^{(k)})}",
    "secant": r"x^{(k+1)}=x^{(k)}-\frac{f(x^{(k)})}{f[x^{(k-1)},x^{(k)}]}",
    "newton_system": r"J(x^{(k)})d^{(k)}=-r(x^{(k)}),\qquad x^{(k+1)}=x^{(k)}+d^{(k)}",
    "gauss_newton": r"J^{\mathsf{T}}Jd=-J^{\mathsf{T}}r",
    "jacobian_linear": r"J_{ij}=\frac{\partial r_i}{\partial x_j},\qquad r(x+d)=r(x)+J(x)d+O(\Vert d\Vert^2)",
    "jacobian_fd": r"J_{ij}\approx\frac{r_i(x+he_j)-r_i(x)}{h},\qquad J_{ij}\approx\frac{r_i(x+he_j)-r_i(x-he_j)}{2h}",
    "expectation": r"E[f(X)]=\int_{-\infty}^{\infty}f(x)p(x)\,dx,\qquad P(x)=\int_{-\infty}^{x}p(\xi)\,d\xi",
    "quadrature": r"I(f)=\int_a^b f(x)\,dx,\qquad Q(f)=\sum_iw_if(\xi_i),\qquad E=I-Q",
    "trap": r"Q_N^{\mathrm{trap}}=\sum_{i=1}^{N}\frac{h_i}{2}(f_{i-1}+f_i)",
    "mid": r"Q_N^{\mathrm{mid}}=\sum_{i=1}^{N}h_i f\!\left(\frac{x_{i-1}+x_i}{2}\right)",
    "simpson": r"Q_N^{\mathrm{S}}=\frac{h}{3}\left[f_0+4f_1+2f_2+\cdots+4f_{N-1}+f_N\right]",
    "quad_errors": r"|E_N^{\mathrm{trap}}|\leq\frac{(b-a)Mh^2}{12},\qquad |E_N^{\mathrm{mid}}|\leq\frac{(b-a)Mh^2}{24}",
    "simpson_error": r"|E_N^{\mathrm{S}}|\leq\frac{(b-a)\max|f^{(4)}|h^4}{2880}",
    "error_rate": r"|E_{2N}|\approx\frac{|E_N|}{2^r},\qquad r\approx\log_2\!\left(\frac{|E_N|}{|E_{2N}|}\right)",
    "gauss_degree": r"2N-1",
    "gauss_map": r"\int_a^bf(x)\,dx\approx\frac{b-a}{2}\sum_{i=1}^{N}w_i f\!\left(\frac{a+b}{2}+\frac{b-a}{2}\xi_i\right)",
    "gauss_nodes": r"N=2:\ \xi=\pm\frac{1}{\sqrt{3}},\ w=1;\qquad N=3:\ \xi=0,\pm\sqrt{\frac{3}{5}},\ w=\frac{8}{9},\frac{5}{9},\frac{5}{9}",
    "tensor": r"\int_{[0,1]^2}f(x,y)\,dx\,dy\approx\sum_{i,j}w_iw_jf(\xi_i,\xi_j)",
    "uniform_dist": r"X\sim U[a,b]:\quad p(x)=\frac{1}{b-a},\quad E[X]=\frac{a+b}{2},\quad\operatorname{Var}(X)=\frac{(b-a)^2}{12}",
    "inverse_transform": r"U\sim U[0,1],\qquad Y=F^{-1}(U)\Longrightarrow F_Y=F",
    "normal_dist": r"Y\sim N(\mu,\sigma^2):\quad p(y)=\frac{e^{-(y-\mu)^2/(2\sigma^2)}}{\sqrt{2\pi}\sigma},\qquad Y=\mu+\sigma Z",
    "mc": r"E_N[f]=\frac{1}{N}\sum_{i=1}^{N}f(x_i)",
    "mc_error": r"e_N[f]=\frac{\sigma[f]}{\sqrt{N}}=O(N^{-1/2})",
    "mc_target": r"e_N[f]\leq\mathrm{tol}\quad\Longrightarrow\quad N\geq\left(\frac{\sigma[f]}{\mathrm{tol}}\right)^2",
    "mc_expectation": r"E[f]=\int_{R^d}f(x)p(x)\,dx,\qquad x_i\overset{\mathrm{iid}}{\sim}p",
    "qmc_estimator": r"Q_N=\frac{1}{N}\sum_{j=1}^{N}f(x_j),\qquad x_j\in[0,1]^d",
    "importance": r"q(x)=g(x)p(x),\qquad E[f]\approx\frac{1}{N}\sum_{i=1}^{N}\frac{f(y_i)}{g(y_i)},\quad y_i\sim q",
    "kh": r"\left|\int_{[0,1]^d}f-Q_N\right|\leq V(f)D_N^*",
    "discrepancy": r"D_N^*=\sup_{y\in[0,1]^d}\left|\prod_{i=1}^{d}y_i-\frac{\#\{x_j\in[0,y)\}}{N}\right|,\qquad D_N^*\leq C\frac{(\log N)^d}{N}",
    "gamma": r"\gamma=\frac{1}{2}",
    "random_walk": r"\Delta X_n=\mu\Delta t+\sigma(\Delta t)^\gamma Z_n,\quad E[X_N-X_0]=\mu T,\quad\operatorname{Var}(X_N-X_0)=\sigma^2T(\Delta t)^{2\gamma-1}",
    "wiener": r"W(t)-W(s)\sim N(0,t-s),\qquad W_{j+1}=W_j+\sqrt{\Delta t}\,Z_j",
    "stock_step": r"S_{n+1}=S_n\left(1+\mu\Delta t+\sigma\sqrt{\Delta t}\,Z_n\right)",
    "ito_integral": r"\int_0^T f(W(t),t)\,dW(t)=\lim_{N\to\infty}\sum_{n=0}^{N-1}f(W(t_n),t_n)\,[W(t_{n+1})-W(t_n)]",
    "ito_lemma": r"dY=\left(H_t+\frac{1}{2}g^2H_{xx}\right)dt+H_x\,dX",
    "ito_qv": r"\sum_n(\Delta W_n)^2\longrightarrow T,\qquad\int_0^T W\,dW=\frac{1}{2}W(T)^2-\frac{1}{2}T",
    "sde": r"dX=f(X,t)\,dt+g(X,t)\,dW,\qquad X(0)=X_0",
    "gbm": r"S(t)=S_0\exp\!\left[\left(\mu-\frac{1}{2}\sigma^2\right)t+\sigma W(t)\right]",
    "gbm_dist": r"\ln\!\left(\frac{S(t)}{S_0}\right)\sim N\!\left(\left(\mu-\frac{1}{2}\sigma^2\right)t,\sigma^2t\right)",
    "bs_pde": r"V_t+rSV_S+\frac{1}{2}\sigma^2S^2V_{SS}=rV",
    "parity": r"S+p=c+Ke^{-r(T-t)}",
    "option_bc": r"c(S,T)=\max(S-K,0),\ c(0,t)=0,\ c\sim S-Ke^{-r(T-t)};\qquad p(S,T)=\max(K-S,0),\ p(0,t)=Ke^{-r(T-t)},\ p\to0",
    "log_pde": r"-U_\tau+\left(r-\frac{1}{2}\sigma^2\right)U_y+\frac{1}{2}\sigma^2U_{yy}=rU",
    "log_call_bc": r"U(y,0)=K\max(e^y-1,0),\quad U\to0\ (y\to-\infty),\quad U\sim Ke^y-Ke^{-r\tau}\ (y\to\infty)",
    "log_put_bc": r"U(y,0)=K\max(1-e^y,0),\quad U\sim Ke^{-r\tau}\ (y\to-\infty),\quad U\to0\ (y\to\infty)",
    "explicit": r"V_j^{n-1}=\alpha_jV_{j-1}^n+\beta_jV_j^n+\gamma_jV_{j+1}^n",
    "implicit": r"\alpha_jV_{j-1}^n+\beta_jV_j^n+\gamma_jV_{j+1}^n=V_j^{n+1}",
    "cn_order": r"O\!\left((\Delta t)^2+(\Delta S)^2\right)",
    "fd_space": r"V_S\approx\frac{V_{j+1}-V_{j-1}}{2\Delta S},\qquad V_{SS}\approx\frac{V_{j+1}-2V_j+V_{j-1}}{(\Delta S)^2}",
    "fd_grid": r"\Delta S=\frac{S_{\max}}{N_S+1},\quad S_j=j\Delta S;\qquad\Delta t=\frac{T}{N_t},\quad t_n=n\Delta t",
    "explicit_coeffs": r"\rho=\frac{\Delta t}{2(\Delta S)^2},\quad\alpha_j=(\sigma^2S_j^2-rS_j\Delta S)\rho,\quad\beta_j=1-r\Delta t-2\sigma^2S_j^2\rho,\quad\gamma_j=(\sigma^2S_j^2+rS_j\Delta S)\rho",
    "explicit_stability": r"\sigma^2\geq r,\qquad\frac{\Delta t}{(\Delta S)^2}\leq\min_{1\leq j\leq N_S}\frac{1}{r(\Delta S)^2+\sigma^2S_j^2}",
    "implicit_coeffs": r"\alpha_j=\frac{j\Delta t}{2}(r-\sigma^2j),\quad\beta_j=1+r\Delta t+\frac{\sigma^2S_j^2\Delta t}{(\Delta S)^2},\quad\gamma_j=-\frac{\sigma^2S_j^2\Delta t}{2(\Delta S)^2}-\frac{rS_j\Delta t}{2\Delta S}",
    "cn_average": r"V_j^{n+1/2}=\frac{V_j^n+V_j^{n+1}}{2},\qquad V_t\approx\frac{V_j^{n+1}-V_j^n}{\Delta t}",
    "greeks": r"\Delta=V_S,\qquad\Gamma=V_{SS},\qquad\Theta=V_t,\qquad\rho=V_r,\qquad\mathrm{Vega}=V_\sigma",
}


FORMULA_KEYS = {
    "±(1.d₁d₂…dₚ)₂ × 2ᵉ": "fpn",
    "ε = 2⁻⁵² ≈ 2.22×10⁻¹⁶": "epsilon",
    "‖x‖ₚ=(Σ|xᵢ|ᵖ)¹ᐟᵖ": "vnorm",
    "‖A‖ₚ=maxₓ≠₀ ‖Ax‖ₚ/‖x‖ₚ": "mnorm",
    "κ(A)=‖A‖‖A⁻¹‖≥1": "kappa",
    "‖δx‖/‖x‖ ≤ ακ(A)(ρA+ρb)": "perturb",
    "PA=LU": "plu",
    "A=RᵀR": "chol",
    "AP=Q[R;0]": "qrp",
    "A=U[Σ;0]Vᵀ": "svd",
    "AᵀAx*=Aᵀy": "normal",
    "s∈C²[a,b]": "c2",
    "sᵢ(t)=Mᵢ₋₁(tᵢ−t)³/(6h)+Mᵢ(t−tᵢ₋₁)³/(6h)+(yᵢ₋₁/h−Mᵢ₋₁h/6)(tᵢ−t)+(yᵢ/h−Mᵢh/6)(t−tᵢ₋₁).": "spline",
    "(h/6)Mᵢ₋₁+(2h/3)Mᵢ+(h/6)Mᵢ₊₁=dᵢ₊₁−dᵢ": "spline_system",
    "−(Uⱼ₊₁−2Uⱼ+Uⱼ₋₁)/(Δx)²=f(xⱼ)": "bvp",
    "a₀=(1/T)∫g(t)dt": "fourier_a0",
    "aₖ=(2/T)∫g(t)cos(2πkt/T)dt": "fourier_ak",
    "bₖ=(2/T)∫g(t)sin(2πkt/T)dt": "fourier_bk",
    "cₖ=(1/T)∫g(t)e<super>−i2πkt/T</super>dt": "fourier_ck",
    "ŷₖ=Σⱼyⱼe<super>−i2πjk/n</super>=Σⱼyⱼω<super>−jk</super>": "dft",
    "yⱼ=(1/n)Σₖŷₖe<super>i2πjk/n</super>": "idft",
    "pₖ=|ŷₖ|²/n": "power",
    "c=SN(d₁)−Ke<super>−rτ</super>N(d₂)": "bs_call",
    "x⁽ᵏ⁺¹⁾=x⁽ᵏ⁾−f(x⁽ᵏ⁾)/f′(x⁽ᵏ⁾)": "newton",
    "J(x⁽ᵏ⁾)d⁽ᵏ⁾=−r(x⁽ᵏ⁾), x⁽ᵏ⁺¹⁾=x⁽ᵏ⁾+d⁽ᵏ⁾": "newton_system",
    "JᵀJd=−Jᵀr": "gauss_newton",
    "Q<sub>N</sub><super>trap</super>=Σ(hᵢ/2)(fᵢ₋₁+fᵢ)": "trap",
    "Q<sub>N</sub><super>mid</super>=Σhᵢf((xᵢ₋₁+xᵢ)/2)": "mid",
    "Q<sub>N</sub><super>S</super>=(h/3)[f₀+4f₁+2f₂+⋯+4f<sub>N−1</sub>+f<sub>N</sub>]": "simpson",
    "2N−1": "gauss_degree",
    "E<sub>N</sub>[f]=(1/N)Σᵢf(xᵢ)": "mc",
    "e<sub>N</sub>[f]=σ[f]/√N=O(N⁻¹ᐟ²)": "mc_error",
    "|∫f−Q<sub>N</sub>|≤V(f)D<sub>N</sub>*": "kh",
    "γ=1/2": "gamma",
    "∫₀ᵀf(W(t),t)dW(t)=lim Σf(W(tₙ),tₙ)[W(tₙ₊₁)−W(tₙ)]": "ito_integral",
    "dY=[H<sub>t</sub>+½g²H<sub>xx</sub>]dt+H<sub>x</sub>dX": "ito_lemma",
    "S(t)=S₀exp[(μ−½σ²)t+σW(t)]": "gbm",
    "V<sub>t</sub>+rSV<sub>S</sub>+½σ²S²V<sub>SS</sub>=rV": "bs_pde",
    "S+p=c+Ke<super>−r(T−t)</super>": "parity",
    "−U<sub>τ</sub>+(r−½σ²)U<sub>y</sub>+½σ²U<sub>yy</sub>=rU": "log_pde",
    "Vⱼ<super>n−1</super>=αⱼVⱼ₋₁ⁿ+βⱼVⱼⁿ+γⱼVⱼ₊₁ⁿ": "explicit",
    "αⱼVⱼ₋₁ⁿ+βⱼVⱼⁿ+γⱼVⱼ₊₁ⁿ=Vⱼ<super>n+1</super>": "implicit",
    "O((Δt)²+(ΔS)²)": "cn_order",
}


def equation_asset(key: str):
    """Render a compact TeX-style equation and return its asset and dimensions."""
    MATH_DIR.mkdir(parents=True, exist_ok=True)
    tex = TEX[key]
    math_color = "#0B5FA5"
    asset_signature = f"{tex}|{math_color}|pad={MATH_PAD_TOP_PT},{MATH_PAD_BOTTOM_PT}"
    digest = hashlib.sha1(asset_signature.encode("utf-8")).hexdigest()[:16]
    path = MATH_DIR / f"{key}_{digest}.png"
    if not path.exists():
        raw = io.BytesIO()
        math_to_image(
            f"${tex}$",
            raw,
            prop=FontProperties(size=MATH_FONT_SIZE, math_fontfamily="stix"),
            dpi=MATH_DPI,
            format="png",
            color=math_color,
        )
        raw.seek(0)
        with Image.open(raw) as source:
            source_rgba = source.convert("RGBA")
        pad_top = round(MATH_PAD_TOP_PT * MATH_DPI / 72.0)
        pad_bottom = round(MATH_PAD_BOTTOM_PT * MATH_DPI / 72.0)
        padded = Image.new(
            "RGBA",
            (source_rgba.width, source_rgba.height + pad_top + pad_bottom),
            (255, 255, 255, 0),
        )
        padded.alpha_composite(source_rgba, (0, pad_top))
        padded.save(path)
    with Image.open(path) as img:
        width, height = img.size
    width_pt = width * 72.0 / MATH_DPI
    height_pt = height * 72.0 / MATH_DPI
    max_width = COL_W - 7.0
    if width_pt > max_width:
        scale = max_width / width_pt
        width_pt *= scale
        height_pt *= scale
    return path, width_pt, height_pt


def equation(key: str) -> str:
    """Return Paragraph markup for a compact inline TeX-style equation."""
    path, width_pt, height_pt = equation_asset(key)
    return f'<img src="{path}" width="{width_pt:.2f}" height="{height_pt:.2f}" valign="middle"/>'


def equation_block(key: str):
    """Return a measured standalone equation block that cannot overlap text."""
    path, width_pt, height_pt = equation_asset(key)
    flowable = RLImage(str(path), width=width_pt, height=height_pt)
    flowable.hAlign = "LEFT"
    flowable.spaceBefore = 0.8
    flowable.spaceAfter = 2.2
    return flowable


def styles(font_size: float):
    # Equations are inline high-resolution images and can be much taller than
    # ordinary glyphs (fractions, roots, sums, matrices).  autoLeading="max"
    # makes only those lines grow to their actual content height, preventing
    # collisions without wasting space on prose-only lines.
    leading = font_size * 1.40
    body = ParagraphStyle(
        "body",
        fontName="Arial",
        fontSize=font_size,
        leading=leading,
        autoLeading="max",
        textColor=TEXT,
        spaceAfter=1.30,
        splitLongWords=True,
        allowWidows=1,
        allowOrphans=1,
    )
    sub = ParagraphStyle(
        "sub",
        parent=body,
        fontName="Arial-Bold",
        fontSize=font_size + 0.2,
        leading=leading + 0.15,
        textColor=TEAL,
        spaceBefore=1.35,
        # Tall limits in the first equation line must clear the subheading.
        spaceAfter=2.6,
    )
    head = ParagraphStyle(
        "head",
        parent=body,
        fontName="Arial-Bold",
        fontSize=font_size + 1.45,
        leading=font_size + 2.25,
        textColor=colors.white,
        backColor=BLUE,
        borderPadding=(1.2, 2.0, 1.1, 2.0),
        spaceBefore=1.5,
        spaceAfter=1.8,
        keepWithNext=True,
    )
    return body, sub, head


def B(text: str) -> str:
    if text in FORMULA_KEYS:
        return equation(FORMULA_KEYS[text])
    return f'<font color="{BLUE.hexval()}"><b>{text}</b></font>'


def R(text: str) -> str:
    return f'<font color="{RED.hexval()}"><b><i>{text}</i></b></font>'


def P(text: str) -> str:
    return f'<font color="{PURPLE.hexval()}"><b>{text}</b></font>'


def topic(num: str, title: str, blocks, S):
    body, sub, head = S
    out = [Paragraph(f"{num}. {title}", head)]
    for kind, text in blocks:
        if kind == "sub":
            out.append(Paragraph(text, sub))
        elif kind == "math":
            out.append(equation_block(text))
        else:
            out.append(Paragraph(text, body))
    return out


def front_columns(S):
    c1 = []
    c1 += topic("1", "COMPUTING WITH REAL NUMBERS", [
        ("sub", "Floating-point system"),
        ("body", f"Normalized binary FPN: {B('±(1.d₁d₂…dₚ)₂ × 2ᵉ')}, dⱼ∈{{0,1}}, e<sub>min</sub>≤e≤e<sub>max</sub>. IEEE double: sign 1 bit, p=52 fraction bits, 11 exponent bits; normal e∈[−1022,1023].<br/>{B('ε = 2⁻⁵² ≈ 2.22×10⁻¹⁶')} (gap from 1 to next FPN); {equation('fpn_limits')}. Below: subnormal, then underflow to 0; overflow→±∞; undefined→NaN. {R('FPN arithmetic is not associative; avoid exact equality tests.')}"),
        ("sub", "Errors, accuracy, stability"),
        ("body", f"For approximation x̄ to x: {equation('errors')} ({R('x≠0')}). Significant decimal figures: largest p satisfying {equation('sigfig')}. Storage rounding error ≲ε|x|.<br/>{P('Catastrophic cancellation:')} subtracting computed nonzero x̄,ȳ when x≈y can greatly amplify relative error. Quadratic ax²+bx+c=0: {equation('quadratic')}. {R('Require a≠0, real-root form b²−4ac≥0, q≠0 for c/q.')}"),
        ("sub", "Cost and storage"),
        ("body", f"1 bit∈{{0,1}}; 1 byte=8 bits; KiB=2¹⁰ bytes, MiB=2²⁰, GiB=2³⁰. Signed b-bit integer range [−2ᵇ⁻¹,2ᵇ⁻¹−1]. 1 flop = one FPN +, −, ×, /. Speed=(cycles/s)(cores)(flops/cycle); time=flops/speed. {equation('storage_cost')}."),
    ], S)
    c1 += topic("2", "NORMS, EQUALITY, SENSITIVITY", [
        ("sub", "Vector norms and error"),
        ("body", f"For x∈ℝⁿ, p≥1: {B('‖x‖ₚ=(Σ|xᵢ|ᵖ)¹ᐟᵖ')}; {equation('special_norms')}. Norm axioms: positivity/definiteness, triangle inequality, absolute homogeneity. {equation('numeric_equal')}.<br/>{equation('vector_error')} ({R('x≠0')}); {equation('vector_sigfig')}."),
        ("sub", "Matrix norms"),
        ("body", f"Subordinate norm: {B('‖A‖ₚ=maxₓ≠₀ ‖Ax‖ₚ/‖x‖ₚ')}; {equation('mnorm_props')}. {equation('named_mnorms')}; Frobenius ‖A‖<sub>F</sub>=√Σᵢⱼ|aᵢⱼ|² ({R('not generally ‖A‖₂')})."),
        ("sub", "Conditioning of Ax=b"),
        ("body", f"For nonsingular A: {B('κ(A)=‖A‖‖A⁻¹‖≥1')}; rcond=1/κ. {equation('kappa_specs')}.<br/>{equation('perturbed_system')}; A+δA nonsingular, α&gt;1. {equation('rho_defs')}; {B('‖δx‖/‖x‖ ≤ ακ(A)(ρA+ρb)')}. Large κ ⇒ sensitive/ill-conditioned; κ≳1/ε can destroy machine-precision information."),
    ], S)

    c2 = []
    c2 += topic("3", "MATRIX STRUCTURE & FACTORISATIONS", [
        ("sub", "Special matrices"),
        ("body", f"{equation('covariance')}; C symmetric PSD. {equation('correlation')}, |Kᵢⱼ|≤1 ({R('σᵢ,σⱼ>0')}).<br/>Upper/lower triangular: aᵢⱼ=0 for i&gt;j / i&lt;j. {equation('triangular')}. Unit triangular: aᵢᵢ=1. Triangular solve ≈n² flops.<br/>{equation('banded')}; total bandwidth m<sub>ℓ</sub>+m<sub>u</sub>+1; nnz≤(1+m<sub>ℓ</sub>+m<sub>u</sub>)n−m<sub>ℓ</sub>(m<sub>ℓ</sub>+1)/2−m<sub>u</sub>(m<sub>u</sub>+1)/2. Tridiagonal: m<sub>ℓ</sub>=m<sub>u</sub>=1. Toeplitz: aᵢⱼ=α<sub>j−i</sub>.<br/>Symmetric Aᵀ=A; skew Aᵀ=−A. {equation('sym_split')}. Definiteness by xᵀAx: PD &gt;0, PSD ≥0, ND &lt;0, NSD ≤0; for real symmetric A, signs of eigenvalues give type. Strict row diagonal dominance: {equation('diag_dom')}; symmetric + strict dominance ⇒ PD.<br/>{equation('orthogonal')}. Permutation matrices are orthogonal."),
        ("sub", "LU and Cholesky"),
        ("body", f"LU: A=LU with L unit lower, U upper; when it exists for nonsingular A it is unique. In general partial pivoting gives {B('PA=LU')}; |ℓᵢⱼ|≤1. Factor cost ≈2n³/3; two triangular solves ≈2n². {R('Require nonsingular A for a unique solve; do not form A⁻¹.')}<br/>Cholesky: {B('A=RᵀR')}, R upper. {R('Require real symmetric positive-definite A.')}; factor cost n³/3, solves 2n²; no row pivoting."),
        ("sub", "QR"),
        ("body", f"For A∈ℝᵐˣⁿ, m≥n, rank(A)=n: {equation('qr_economy')}; R nonsingular upper. Cost ≈2mn²−(2/3)n³. If rank deficient: {B('AP=Q[R;0]')}, column pivoting, |r₁₁|≥⋯≥|rₙₙ|; small diagonal entries indicate numerical rank deficiency."),
        ("sub", "SVD"),
        ("body", f"A∈ℝᵐˣⁿ, m≥n: {B('A=U[Σ;0]Vᵀ')}; U,V orthogonal, Σ=diag(σ₁≥⋯≥σₙ≥0). rank(A)=number of positive σᵢ; {equation('svd_sums')}. Full rank: κ₂(A)=σ₁/σₙ. Numerical rank tolerance ≈max(m,n)εσ₁."),
    ], S)
    topic4 = topic("4", "PARAMETRIC DATA FITTING", [
        ("sub", "Residual model"),
        ("body", f"Data (tᵢ,yᵢ), i=1,…,m; parameters x∈ℝⁿ, {R('m≥n')}. {equation('residual')}. Interpolation ⇔ r=0 ({R('appropriate only for highly accurate data')}). Linear-in-parameters: {equation('linear_residual')}."),
        ("sub", "Linear least squares (p=2)"),
        ("body", f"Normal equations: {B('AᵀAx*=Aᵀy')}; residual orthogonal to col(A). AᵀA PSD, and PD iff A has full column rank. {R('Avoid forming AᵀA when conditioning matters: κ₂(AᵀA)=κ₂(A)².')}<br/>Pivoted QR AP=Q[R;0], Q=[Y Z]: {equation('ls_qr')}. SVD A=U[Σ;0]Vᵀ, U=[Y Z]: {equation('ls_svd')}. Use Σ⁺=diag(1/σ₁,…,1/σᵣ,0,…) for rank r&lt;n."),
        ("sub", "Choice of norm / transformation"),
        ("body", f"p=2: suited to independent N(0,σ²) errors with common variance. p=1: robust to outliers, {equation('lp_l1')}. p=∞: {equation('lp_linf')}. Linear r gives linear programs.<br/>Log-linearisation: products/exponentials/powers may be transformed. {R('Log transform requires every logged quantity positive and any shifted base t−βⱼ>0.')}"),
    ], S)

    c3 = []
    c3 += topic4
    topic5_blocks = [
        ("sub", "Polynomials and interpolation"),
        ("body", f"{equation('polynomial')}; Horner form uses n multiplies+n adds. Weierstrass: for continuous f on closed [a,b], ∀ε&gt;0 ∃ polynomial p with |f−p|&lt;ε on [a,b].<br/>Polynomial interpolation at distinct t₀,…,tₙ: Vandermonde Ax=y, Aᵢⱼ=tᵢʲ. {R('High-degree equally spaced interpolation can be ill-conditioned and oscillatory; use low-degree pieces.')}"),
        ("sub", "Cubic spline"),
        ("body", f"Knots a=t₀&lt;⋯&lt;tₙ=b. s(t)=sᵢ(t) on [tᵢ₋₁,tᵢ], degree(sᵢ)≤3, and {B('s∈C²[a,b]')}. Interpolation s(tᵢ)=yᵢ; at interior knots {equation('spline_join')}. Two endpoint conditions required: {equation('spline_bc')}."),
        ("body", f"Uniform h=tᵢ−tᵢ₋₁, dᵢ=(yᵢ−yᵢ₋₁)/h, Mᵢ=s″(tᵢ). For t∈[tᵢ₋₁,tᵢ]:<br/>{B('sᵢ(t)=Mᵢ₋₁(tᵢ−t)³/(6h)+Mᵢ(t−tᵢ₋₁)³/(6h)+(yᵢ₋₁/h−Mᵢ₋₁h/6)(tᵢ−t)+(yᵢ/h−Mᵢh/6)(t−tᵢ₋₁).')}<br/>Interior system: {B('(h/6)Mᵢ₋₁+(2h/3)Mᵢ+(h/6)Mᵢ₊₁=dᵢ₊₁−dᵢ')}, i=1,…,n−1, plus endpoint equations. Natural: M₀=Mₙ=0; coefficient matrix symmetric tridiagonal diagonally dominant PD; Thomas solve O(n)."),
        ("sub", "Sparse structure"),
        ("body", f"Sparsity=#zeros/(mn); density=nnz/(mn). Diagonal density≈1/n; tridiagonal≈3/n. Hidden sparse product: {equation('hidden_sparse')}. Store/operate on nonzeros. Fill-in=new nonzeros during factorisation; PAQ=LU can reduce fill-in. For banded A=LU without disruptive pivoting, L/U retain lower/upper bandwidth; SPD A=RᵀR gives R same upper bandwidth."),
        ("sub", "1-D boundary-value finite difference"),
        ("body", f"{equation('bvp_setup')}. {B('−(Uⱼ₊₁−2Uⱼ+Uⱼ₋₁)/(Δx)²=f(xⱼ)')}, j=1,…,n; U₀=α,Uₙ₊₁=β; error O((Δx)²) under sufficient smoothness. Matrix tridiagonal Toeplitz SPD with diagonal 2 and off-diagonal −1; RHS endpoints add α,β."),
    ]
    c3 += topic("5", "CUBIC SPLINES & SPARSE MATRICES", topic5_blocks[:5], S)

    c4 = []
    c4 += topic("5", "CUBIC SPLINES & SPARSE MATRICES (CONT.)", topic5_blocks[5:], S)
    c4 += topic("6", "FOURIER ANALYSIS & FFT", [
        ("sub", "Periodic and trigonometric form"),
        ("body", f"{equation('periodic')}. Harmonic k: frequency k/T, angular frequency 2πk/T. {equation('trig_poly')}.<br/>Over any full period (shown on [−T/2,T/2]): {B('a₀=(1/T)∫g(t)dt')}; {B('aₖ=(2/T)∫g(t)cos(2πkt/T)dt')}; {B('bₖ=(2/T)∫g(t)sin(2πkt/T)dt')}. Orthogonality: equal nonzero sine/sine or cosine/cosine integral=T/2; unequal or sine/cosine=0.<br/>{R('If periodic g is piecewise differentiable: Fourier series converges to g at continuity points and to [g(t+)+g(t−)]/2 at jumps.')} Gibbs oscillations persist near jumps."),
        ("sub", "Complex Fourier series"),
        ("body", f"{equation('complex_series')}; {B('cₖ=(1/T)∫g(t)e<super>−i2πkt/T</super>dt')}; c₀=a₀. {R('Pointwise equality stated at continuity points.')}"),
        ("sub", "DFT / inverse / FFT"),
        ("body", f"ω=e<super>i2π/n</super>. For j,k=0,…,n−1: {B('ŷₖ=Σⱼyⱼe<super>−i2πjk/n</super>=Σⱼyⱼω<super>−jk</super>')}; {B('yⱼ=(1/n)Σₖŷₖe<super>i2πjk/n</super>')}. Direct O(n²); FFT O(n log₂n). {equation('dft_symmetry')}."),
        ("sub", "Fourier coefficients from equally spaced data"),
        ("body", f"tⱼ=jΔt, Δt=T/n, yⱼ≈g(tⱼ), p=⌊n/2⌋. {equation('sample_coeffs')}.<br/>If n=2p even: k=1,…,p−1 use ordinary form; Aₚ=ŷₚ/n, Bₚ=0. If n=2p+1 odd: ordinary form through k=p. Then yⱼ=A₀+Σₖ[Aₖcos(2πktⱼ/T)+Bₖsin(2πktⱼ/T)]."),
        ("sub", "De-trending and spectrum"),
        ("body", f"For Yⱼ≈x₁+x₂tⱼ+g(tⱼ), g periodic: least-squares fit x₁+x₂t and define yⱼ=Yⱼ−(x₁+x₂tⱼ) before DFT. Power spectrum {B('pₖ=|ŷₖ|²/n')} plotted against frequency k/T; inspect k=0,…,⌊n/2⌋ for real data. Large pₖ identify dominant periodic components; period=T/k ({R('k>0')})."),
    ], S)
    return [c1, c2, c3, c4]


def back_columns(S):
    c1 = []
    c1 += topic("7", "IMPLIED VOLATILITY & NONLINEAR EQUATIONS", [
        ("sub", "Black–Scholes call and implied volatility"),
        ("body", f"τ=T−t&gt;0. {B('c=SN(d₁)−Ke<super>−rτ</super>N(d₂)')}; {equation('bs_d')}; {equation('normal_cdf')}. Put-call parity: c+Ke<super>−rτ</super>=p+S.<br/>{R('Require S>0, K>0, σ>0, τ>0; model assumptions in Topic 10.')}<br/>Implied volatility: {equation('implied')}. Existence and uniqueness when {equation('call_bounds')}. {equation('implied_limits')}."),
        ("sub", "Taylor and finite differences"),
        ("body", f"If f∈C<super>n+1</super>[a,b], x,x+h∈[a,b]: {equation('taylor')}.<br/>{equation('fd_first')} {R('Require f∈C² and shifted point in [a,b].')}<br/>{equation('fd_central')} {R('Require f∈C³ and x±h∈[a,b].')}<br/>{equation('fd_second')} {R('Require f∈C⁴ and x±h∈[a,b].')}<br/>Machine-rounding balance: {equation('fd_rounding')}. {R('h must be representable so x±h differs from x.')}"),
        ("sub", "Scalar iterations"),
        ("body", f"{equation('convergence')}; for ν=1 require |β|&lt;1.<br/>Newton: {B('x⁽ᵏ⁺¹⁾=x⁽ᵏ⁾−f(x⁽ᵏ⁾)/f′(x⁽ᵏ⁾)')}. Quadratic locally; {R('require f(x*)=0, f′ and f″ continuous near x*, f′≠0 there, initial guess sufficiently close')}; asymptotic ratio →|f″(x*)|/(2|f′(x*)|).<br/>Secant: {equation('secant')}; order (1+√5)/2 locally. {R('Require two distinct initial iterates, nonzero divided differences, starts sufficiently close to a simple root.')}"),
        ("sub", "Systems / Gauss–Newton"),
        ("body", f"r:ℝⁿ→ℝᵐ: {equation('jacobian_linear')}. For m=n, Newton–Raphson: {B('J(x⁽ᵏ⁾)d⁽ᵏ⁾=−r(x⁽ᵏ⁾), x⁽ᵏ⁺¹⁾=x⁽ᵏ⁾+d⁽ᵏ⁾')}; {R('J must be nonsingular at each solve; local quadratic convergence under smoothness and a sufficiently close start.')}<br/>For m≥n nonlinear least squares min‖r‖₂²: {B('JᵀJd=−Jᵀr')}. {R('Local step is uniquely defined when J has full column rank.')}<br/>{equation('jacobian_fd')}; use h≈ε¹ᐟ² forward, h≈ε¹ᐟ³ central."),
    ], S)

    c2 = []
    c2 += topic("8", "NUMERICAL INTEGRATION", [
        ("sub", "Probability integrals and quadrature"),
        ("body", f"PDF p: p≥0, ∫ℝp=1. {equation('expectation')}. If P is differentiable and strictly increasing, y=P(x) gives E[f(X)]=∫₀¹f(P⁻¹(y))dy.<br/>{equation('quadrature')}. Degree of precision m: exact for all polynomials degree≤m and not all of degree m+1."),
        ("sub", "Composite rules"),
        ("body", f"Grid a=x₀&lt;⋯&lt;x<sub>N</sub>=b, hᵢ=xᵢ−xᵢ₋₁. Trapezoidal: {B('Q<sub>N</sub><super>trap</super>=Σ(hᵢ/2)(fᵢ₋₁+fᵢ)')}. Uniform h=(b−a)/N: h[½f₀+Σᵢ₌₁ᴺ⁻¹fᵢ+½f<sub>N</sub>].<br/>Midpoint: {B('Q<sub>N</sub><super>mid</super>=Σhᵢf((xᵢ₋₁+xᵢ)/2)')}.<br/>{equation('quad_errors')}. {R('Require f∈C²[a,b] for O(h²).')} Both have degree 1.<br/>Composite Simpson, {R('uniform grid and even N')}: {B('Q<sub>N</sub><super>S</super>=(h/3)[f₀+4f₁+2f₂+⋯+4f<sub>N−1</sub>+f<sub>N</sub>]')}. Degree 3; {equation('simpson_error')}. {R('Require f∈C⁴[a,b] for O(h⁴).')}<br/>{equation('error_rate')}."),
        ("sub", "Gauss–Legendre"),
        ("body", f"On [−1,1], N nodes/weights chosen exact through x<super>2N−1</super>: degree {B('2N−1')}. {equation('gauss_nodes')}.<br/>{equation('gauss_map')}."),
        ("sub", "Non-smooth and multidimensional"),
        ("body", f"Formal orders are not guaranteed when required derivatives are missing/unbounded. Split at nonsmooth points or change variables to regularise before applying a high-order rule.<br/>Tensor product: {equation('tensor')}. A d-fold (N+1)-point rule uses (N+1)ᵈ points ({P('curse of dimensionality')})."),
    ], S)
    c2 += topic("9", "RANDOM NUMBERS & SIMULATION — DISTRIBUTIONS", [
        ("body", f"True random: physical source. Pseudorandom: deterministic, reproducible, statistically random-like. Quasirandom: deterministic, designed for multidimensional uniformity.<br/>{equation('uniform_dist')} ({R('a&lt;b')}); if U~U[0,1], Y=a+(b−a)U.<br/>{equation('inverse_transform')}. {R('Use a suitable generalised inverse if strict invertibility fails.')}<br/>{equation('normal_dist')} ({R('σ>0')}). Independent sums: EΣXᵢ=ΣEXᵢ; VarΣXᵢ=ΣVarXᵢ. CLT: iid sums are approximately normal for large n and finite variance."),
    ], S)

    c3 = []
    c3 += topic("9", "RANDOM NUMBERS & SIMULATION — MC/QMC", [
        ("sub", "Monte Carlo"),
        ("math", "mc_expectation"),
        ("math", "mc"),
        ("body", "Estimator is unbiased; RMS error is independent of d."),
        ("math", "mc_error"),
        ("math", "mc_target"),
        ("body", f"{R('Require independent samples and finite Var[f].')}"),
        ("sub", "Variance reduction"),
        ("body", f"Control variate: known μ<sub>g</sub>=E[g], estimate E[f−g]+μ<sub>g</sub>; useful when Var(f−g)≪Var(f).<br/>Antithetic pairs: {R('N even')}; on symmetric ℝᵈ pair x and −x; on [0,1]ᵈ pair x and 1−x. Odd component integrates exactly.<br/>Importance sampling: {equation('importance')}. {R('Require q≥0, ∫q=1, and g(x)≠0 wherever f(x)≠0; finite variance of f/g under q.')}"),
        ("sub", "Quasi-Monte Carlo"),
        ("body", "Deterministic points:"),
        ("math", "qmc_estimator"),
        ("body", "Koksma–Hlawka:"),
        ("math", "kh"),
        ("body", f"{R('Requires bounded variation V(f).')} Star discrepancy:"),
        ("math", "discrepancy"),
        ("body", "Constant C depends on d."),
    ], S)
    c3 += topic("10", "STOCHASTIC INTEGRATION & SDEs — FOUNDATIONS", [
        ("sub", "Random walk / Wiener process"),
        ("body", f"tₙ=nΔt, Δt=T/N: {equation('random_walk')}; iid Zₙ~N(0,1). Finite nonzero limit requires {B('γ=1/2')}. {equation('stock_step')}.<br/>Wiener W: W(0)=0; a.s. continuous paths; increments over non-overlapping intervals are independent: for a&lt;b≤c&lt;d, W(b)−W(a) is independent of W(d)−W(c); {equation('wiener')}."),
        ("sub", "Itô integral / lemma"),
        ("body", f"{B('∫₀ᵀf(W(t),t)dW(t)=lim Σf(W(tₙ),tₙ)[W(tₙ₊₁)−W(tₙ)]')} ({R('left endpoints; adapted integrand')}). {equation('ito_qv')}.<br/>{equation('sde')}. For Y=H(X,t): {B('dY=[H<sub>t</sub>+½g²H<sub>xx</sub>]dt+H<sub>x</sub>dX')}. {R('Require H continuously differentiable in t and twice continuously differentiable in x.')}"),
    ], S)

    c4 = []
    c4 += topic("10", "STOCHASTIC INTEGRATION & BLACK–SCHOLES", [
        ("sub", "Geometric Brownian motion"),
        ("body", f"dS/S=μdt+σdW, {R('S₀>0, σ>0')}. {B('S(t)=S₀exp[(μ−½σ²)t+σW(t)]')}; {equation('gbm_dist')}; S(t) is lognormal and positive."),
        ("sub", "Black–Scholes PDE and conditions"),
        ("body", f"{B('V<sub>t</sub>+rSV<sub>S</sub>+½σ²S²V<sub>SS</sub>=rV')}, S&gt;0, 0&lt;t&lt;T. Delta hedge uses f=V<sub>S</sub> short shares. {R('Assumptions: GBM underlying; constant known r,σ; no dividends, transaction costs, taxes or arbitrage; continuous trading and short selling allowed.')}<br/>{equation('option_bc')}. Put-call parity: {B('S+p=c+Ke<super>−r(T−t)</super>')} ({R('European options, same K,T')})."),
        ("sub", "Log-price/time transformation"),
        ("body", f"y=ln(S/K), τ=T−t, V(S,t)=U(y,τ): {B('−U<sub>τ</sub>+(r−½σ²)U<sub>y</sub>+½σ²U<sub>yy</sub>=rU')}; y∈ℝ, τ∈[0,T].<br/>{equation('log_call_bc')}; {equation('log_put_bc')}."),
    ], S)
    c4 += topic("11", "FDMs FOR BLACK–SCHOLES", [
        ("sub", "Grid and differences"),
        ("body", f"Truncate S∈[0,S<sub>max</sub>], {R('S<sub>max</sub>>K and sufficiently large')}. {equation('fd_grid')}.<br/>{equation('fd_space')}; each O((ΔS)²). Time one-sided error O(Δt). Boundary/terminal values from Topic 10."),
        ("sub", "Backward Euler - EXPLICIT scheme"),
        ("body", f"{equation('explicit_coeffs')}. {B('Vⱼ<super>n−1</super>=αⱼVⱼ₋₁ⁿ+βⱼVⱼⁿ+γⱼVⱼ₊₁ⁿ')}. Accuracy O(Δt+(ΔS)²) when stable.<br/>Sufficient stability: {equation('explicit_stability')}; then α,β,γ≥0 and |α|+|β|+|γ|≤1. Under this mesh relation overall order is O((ΔS)²)."),
        ("sub", "Forward Euler - IMPLICIT scheme"),
        ("body", f"{equation('implicit_coeffs')}. Solve tridiagonal {B('αⱼVⱼ₋₁ⁿ+βⱼVⱼⁿ+γⱼVⱼ₊₁ⁿ=Vⱼ<super>n+1</super>')} with boundary terms in RHS, backwards n=N<sub>t</sub>−1,…,0. Accuracy O(Δt+(ΔS)²); unconditionally stable. {R('σ²≥r is sufficient for strict diagonal dominance/nonsingularity, not necessary.')} Factor once if r,σ time-independent; total O(N<sub>t</sub>N<sub>S</sub>)."),
        ("sub", "Crank-Nicolson - IMPLICIT scheme; Greeks"),
        ("body", f"At t<sub>n+½</sub>: {equation('cn_average')}; use midpoint value in all S terms. Implicit; accuracy {B('O((Δt)²+(ΔS)²)')}.<br/>{equation('greeks')}."),
    ], S)
    return [c1, c2, c3, c4]


def add_header(canvas, doc, side_label):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 20.5, PAGE_W, 20.5, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Arial-Bold", 10.2)
    canvas.drawString(MARGIN_X, PAGE_H - 14.2, "MATH3311 — NUMERICAL METHODS IN FINANCE")
    canvas.setFont("Arial-Italic", 6.0)
    canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 13.8, side_label)
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.35)
    for i in range(1, COLS):
        x = MARGIN_X + i * COL_W + (i - 0.5) * GAP
        canvas.line(x, BOTTOM, x, PAGE_H - HEADER_H)
    canvas.setFillColor(colors.HexColor("#52606D"))
    canvas.setFont("Arial", 4.7)
    canvas.drawString(MARGIN_X, 3.2, "Formula/definition sheet distilled only from Topics 1–11 lecture slides; conditions are highlighted in red italics.")
    canvas.drawRightString(PAGE_W - MARGIN_X, 3.2, side_label)
    canvas.restoreState()


def measure_column(flowables):
    total = 0.0
    for f in flowables:
        _, h = f.wrap(COL_W - 4, FRAME_H)
        total += h + getattr(f, "spaceBefore", 0) + getattr(f, "spaceAfter", 0)
    return total


def build_single_page(path: Path, columns, side_label):
    frames = []
    for i in range(COLS):
        x = MARGIN_X + i * (COL_W + GAP)
        frames.append(Frame(x, BOTTOM + 1.5, COL_W, FRAME_H - 1.5, leftPadding=2, rightPadding=2, topPadding=1.5, bottomPadding=1.5, id=f"c{i}"))
    doc = BaseDocTemplate(
        str(path), pagesize=(PAGE_W, PAGE_H), leftMargin=0, rightMargin=0, topMargin=0, bottomMargin=0,
        title="MATH3311 Two-Sided A4 Cheat Sheet", author="OpenAI Codex",
    )
    doc.addPageTemplates(PageTemplate(id="fourcols", frames=frames, onPage=lambda c, d: add_header(c, d, side_label)))
    story = []
    for i, col in enumerate(columns):
        story.extend(col)
        if i < len(columns) - 1:
            story.append(FrameBreak())
    doc.build(story)


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    font_size = 6.70
    S = styles(font_size)
    front = front_columns(S)
    back = back_columns(S)
    for label, cols in [("front", front), ("back", back)]:
        heights = [measure_column(c) for c in cols]
        print(label, "column heights", ", ".join(f"{h:.1f}" for h in heights), "limit", f"{FRAME_H:.1f}")
    front_pdf = TMP / "cheatsheet_front.pdf"
    back_pdf = TMP / "cheatsheet_back.pdf"
    build_single_page(front_pdf, front, "FRONT • TOPICS 1–6")
    build_single_page(back_pdf, back, "BACK • TOPICS 7–11")
    if len(PdfReader(str(front_pdf)).pages) != 1 or len(PdfReader(str(back_pdf)).pages) != 1:
        raise RuntimeError("A side overflowed beyond one A4 page; reduce or rebalance content.")
    writer = PdfWriter()
    writer.append(str(front_pdf))
    writer.append(str(back_pdf))
    writer.add_metadata({
        "/Title": "MATH3311 Lecture-Slide Cheat Sheet — A4 Front and Back",
        "/Subject": "Core formulas, definitions, algorithms and constraints from lecture slides only",
        "/Author": "OpenAI Codex",
    })
    with OUT.open("wb") as fh:
        writer.write(fh)
    reader = PdfReader(str(OUT))
    print("wrote", OUT)
    print("pages", len(reader.pages), "size", float(reader.pages[0].mediabox.width), float(reader.pages[0].mediabox.height))


if __name__ == "__main__":
    main()
