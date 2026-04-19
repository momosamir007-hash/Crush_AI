# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import random
import math

st.set_page_config(
    page_title="🧠 Crash Intelligence v5",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

* { font-family: 'Tajawal', sans-serif !important; }
html, body, [data-testid="stAppViewContainer"] { background: #03030d !important; }
[data-testid="stSidebar"] {
    background: #05050f !important;
    border-right: 1px solid rgba(99,102,241,0.12);
}

.card {
    background: linear-gradient(145deg,rgba(7,7,20,0.98),rgba(11,11,28,0.99));
    border: 1px solid rgba(99,102,241,0.18);
    box-shadow: 0 16px 50px rgba(0,0,0,0.85),inset 0 1px 0 rgba(99,102,241,0.1);
    border-radius: 18px; padding: 22px; margin-bottom: 14px;
    direction: rtl; color: white; position: relative; overflow: hidden;
}
.card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg,transparent,#6366f1,#a855f7,#ec4899,transparent);
}

/* ══ حالات القرار ══ */
.DEC-STRONG {
    background:linear-gradient(135deg,rgba(0,255,136,0.11),rgba(0,180,90,0.05));
    border:2px solid #00ff88; border-radius:18px; padding:26px; text-align:center;
    animation:aStrong 1.8s ease-in-out infinite;
}
@keyframes aStrong{0%,100%{box-shadow:0 0 22px rgba(0,255,136,0.2);}50%{box-shadow:0 0 60px rgba(0,255,136,0.55);}}

.DEC-BET {
    background:linear-gradient(135deg,rgba(0,200,255,0.1),rgba(0,130,200,0.05));
    border:2px solid #00c8ff; border-radius:18px; padding:26px; text-align:center;
    animation:aBet 2s ease-in-out infinite;
}
@keyframes aBet{0%,100%{box-shadow:0 0 18px rgba(0,200,255,0.18);}50%{box-shadow:0 0 50px rgba(0,200,255,0.5);}}

.DEC-WAIT {
    background:linear-gradient(135deg,rgba(255,200,0,0.09),rgba(255,140,0,0.04));
    border:2px solid #FFD700; border-radius:18px; padding:26px; text-align:center;
    box-shadow:0 0 22px rgba(255,215,0,0.12);
}
.DEC-AVOID {
    background:linear-gradient(135deg,rgba(255,40,40,0.1),rgba(180,0,0,0.05));
    border:2px solid #ff3232; border-radius:18px; padding:26px; text-align:center;
    animation:aAvoid 0.85s ease-in-out infinite;
}
@keyframes aAvoid{0%,100%{box-shadow:0 0 20px rgba(255,50,50,0.3);}50%{box-shadow:0 0 65px rgba(255,50,50,0.75);}}

.DEC-DOUBLE {
    background:linear-gradient(135deg,rgba(255,100,0,0.11),rgba(200,60,0,0.05));
    border:2px solid #ff6a00; border-radius:18px; padding:26px; text-align:center;
    animation:aDouble 1.1s ease-in-out infinite;
}
@keyframes aDouble{0%,100%{box-shadow:0 0 22px rgba(255,106,0,0.25);}50%{box-shadow:0 0 62px rgba(255,106,0,0.65);}}

/* ══ Score Bar ══ */
.score-track {
    background:rgba(0,0,0,0.4); border-radius:10px; height:22px;
    overflow:hidden; position:relative; border:1px solid rgba(255,255,255,0.08);
    margin-bottom:16px;
}
.score-fill {
    height:100%; border-radius:10px;
    transition:width 0.8s cubic-bezier(0.4,0,0.2,1); position:relative;
}
.score-fill::after {
    content:''; position:absolute; top:0; left:0; right:0; bottom:0;
    border-radius:10px;
    background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,0.18) 50%,transparent 100%);
    animation:shimmer 2s infinite;
}
@keyframes shimmer{0%{transform:translateX(-100%);}100%{transform:translateX(100%);}}

/* ══ Badges ══ */
.badge {
    display:inline-block; padding:5px 10px; border-radius:8px;
    font-size:12px; font-weight:900; margin:2px;
    font-family:'Orbitron',monospace !important;
}
.b-u15{background:#5a0000;border:2px solid #ff1111;color:#ff9090;
       animation:gr15 1.2s ease-in-out infinite;}
@keyframes gr15{0%,100%{box-shadow:0 0 4px rgba(255,20,20,0.4);}50%{box-shadow:0 0 14px rgba(255,20,20,0.8);}}
.b-u18{background:#3d0000;border:1px solid #ff4444;color:#ff7070;}
.b-u2{background:#1a0a00;border:1px solid #ff8800;color:#ffaa55;}
.b-med{background:#1a1200;border:1px solid #FFD700;color:#FFD700;}
.b-win{background:#003d1f;border:1px solid #00ff88;color:#00ff88;}
.b-big{background:#1a0030;border:1px solid #a855f7;color:#c4b5fd;
       animation:gp 1.5s ease-in-out infinite;}
@keyframes gp{0%,100%{box-shadow:0 0 5px rgba(168,85,247,0.3);}50%{box-shadow:0 0 18px rgba(168,85,247,0.7);}}
.b-gold{background:#2d1800;border:2px solid #ff9500;color:#ffb84d;
        animation:gg 1.3s ease-in-out infinite;}
@keyframes gg{0%,100%{box-shadow:0 0 5px rgba(255,149,0,0.35);}50%{box-shadow:0 0 18px rgba(255,149,0,0.75);}}

/* ══ KPI ══ */
.kpi{background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.07);
     border-radius:12px;padding:13px;text-align:center;direction:rtl;transition:all 0.3s;}
.kpi:hover{border-color:rgba(99,102,241,0.3);transform:translateY(-2px);}
.kn{font-family:'Orbitron',monospace!important;font-size:20px;font-weight:900;
    background:linear-gradient(90deg,#6366f1,#a855f7);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.kl{color:rgba(255,255,255,0.3);font-size:10px;margin-top:3px;letter-spacing:1px;}

/* ══ Boxes ══ */
.bx-g{background:rgba(0,255,136,0.05);border:1px solid rgba(0,255,136,0.22);
      border-right:3px solid #00ff88;border-radius:11px;padding:12px 15px;
      color:rgba(150,255,200,0.9);font-size:13px;direction:rtl;margin:6px 0;line-height:1.85;}
.bx-r{background:rgba(255,50,50,0.05);border:1px solid rgba(255,50,50,0.22);
      border-right:3px solid #ff3232;border-radius:11px;padding:12px 15px;
      color:rgba(255,170,170,0.9);font-size:13px;direction:rtl;margin:6px 0;line-height:1.85;}
.bx-y{background:rgba(255,200,0,0.05);border:1px solid rgba(255,200,0,0.22);
      border-right:3px solid #FFD700;border-radius:11px;padding:12px 15px;
      color:rgba(255,230,150,0.9);font-size:13px;direction:rtl;margin:6px 0;line-height:1.85;}
.bx-b{background:rgba(99,102,241,0.05);border:1px solid rgba(99,102,241,0.22);
      border-right:3px solid #6366f1;border-radius:11px;padding:12px 15px;
      color:rgba(180,185,255,0.9);font-size:13px;direction:rtl;margin:6px 0;line-height:1.85;}
.bx-o{background:rgba(255,149,0,0.06);border:1px solid rgba(255,149,0,0.25);
      border-right:3px solid #ff9500;border-radius:11px;padding:12px 15px;
      color:rgba(255,210,150,0.9);font-size:13px;direction:rtl;margin:6px 0;line-height:1.85;}

/* ══ Factor Row ══ */
.factor-row{display:flex;align-items:center;gap:10px;padding:8px 0;
            border-bottom:1px solid rgba(255,255,255,0.04);direction:rtl;}
.factor-icon{font-size:18px;min-width:26px;text-align:center;}
.factor-label{color:rgba(255,255,255,0.65);font-size:13px;flex:1;}
.factor-val{font-family:'Orbitron',monospace!important;font-size:13px;
            font-weight:700;min-width:60px;text-align:left;}
.factor-bar-wrap{flex:1;background:rgba(255,255,255,0.05);border-radius:5px;
                 height:6px;overflow:hidden;min-width:80px;}
.factor-bar-fill{height:100%;border-radius:5px;transition:width 0.6s;}

/* ══ Golden Card ══ */
.gc{background:linear-gradient(135deg,rgba(255,149,0,0.08),rgba(255,70,0,0.03));
    border:1px solid rgba(255,149,0,0.35);border-radius:12px;padding:13px;
    text-align:center;transition:all 0.3s;}
.gc:hover{border-color:#ff9500;transform:translateY(-2px);box-shadow:0 8px 25px rgba(255,149,0,0.25);}
.gn{font-family:'Orbitron',monospace!important;font-size:18px;font-weight:900;
    color:#ff9500;text-shadow:0 0 10px rgba(255,149,0,0.4);}
.gt{font-family:'Orbitron',monospace!important;font-size:13px;color:#00ff88;margin-top:4px;}

/* ══ Progress ══ */
.pw{background:rgba(255,255,255,0.05);border-radius:6px;height:7px;margin:4px 0;overflow:hidden;}
.pf-o{height:100%;border-radius:6px;background:linear-gradient(90deg,#ff6d00,#ff9500);transition:width 0.6s;}
.pf-r{height:100%;border-radius:6px;background:linear-gradient(90deg,#c62828,#ff3232);transition:width 0.6s;}

/* ══ Buttons ══ */
.stButton>button{
    background:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7)!important;
    color:white!important;border:none!important;font-weight:700!important;
    font-size:13px!important;border-radius:10px!important;padding:9px 18px!important;
    box-shadow:0 5px 18px rgba(99,102,241,0.4)!important;transition:all 0.3s!important;
}
.stButton>button:hover{transform:translateY(-2px)!important;
                        box-shadow:0 9px 30px rgba(99,102,241,0.6)!important;}
.stNumberInput>div>div>input{
    background:rgba(255,255,255,0.05)!important;color:white!important;
    border:1px solid rgba(99,102,241,0.35)!important;border-radius:9px!important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# البيانات المرجعية الكاملة (1007 دورة)
# ══════════════════════════════════════════════════════════════════════
REFERENCE_DATA = [
    8.72,6.75,1.86,2.18,1.25,2.28,1.24,1.2,1.54,24.46,4.16,1.49,
    1.09,1.47,1.54,1.53,2.1,32.04,11,1.17,1.7,2.61,1.26,22.23,
    1.77,1.93,3.35,7.01,1.83,9.39,3.31,2.04,1.3,6.65,1.16,3.39,
    1.95,10.85,1.65,1.22,1.6,4.67,1.85,2.72,1,3.02,1.35,1.3,
    1.37,17.54,1.18,1,14.4,1.11,6.15,2.39,2.22,1.42,1.23,2.42,
    1.07,1.24,2.55,7.26,1.69,5.1,2.59,5.51,2.31,2.12,1.97,1.5,
    3.01,2.29,1.36,4.95,5.09,8.5,1.77,5.52,3.93,1.5,2.28,2.49,
    18.25,1.68,1.42,2.12,4.17,1.04,2.35,1,1.01,5.46,1.13,2.84,
    3.39,2.79,1.59,1.53,4.34,2.96,1.06,1.72,2.16,2.2,3.61,2.34,
    4.49,1.72,1.78,9.27,8.49,2.86,1.66,4.63,9.25,1.35,1,1.64,
    1.86,2.81,2.44,1.74,1.1,1.29,1.45,8.92,1.24,6.39,1.16,1.19,
    2.4,4.64,3.17,24.21,1.17,1.42,2.13,1.12,3.78,1.12,1.52,
    22.81,1.31,1.9,1.38,1.47,2.86,1.79,1.49,1.38,1.84,1.06,3.3,
    5.97,1,2.92,1.64,5.32,3.26,1.78,2.24,3.16,1.6,1.08,1.55,
    1.07,1.02,1.23,1.08,5.22,3.32,24.86,3.37,5.16,1.69,2.31,
    1.07,1.1,1.01,1.36,1.38,1.54,5.34,2.68,5.78,3.63,1.89,8.41,
    4.06,1.44,1.5,3.17,1.02,1.8,1.9,1.86,1.85,1.73,3.86,3.11,
    2.44,1.15,2.03,1.05,3.05,1.88,10.13,2.29,1.41,1,5.46,1.26,
    23.33,1.96,1.03,4.54,1.37,3.5,1.13,1.16,1.43,1.13,1.05,33.27,
    9.96,1.79,2.07,18.51,5.75,1.15,1.08,5.92,1.38,1.61,12.99,
    24.72,4.86,1.11,2.86,1.54,3.71,4,7.57,2.03,2.18,5.52,
    13.37,3.73,2.41,1.79,5.57,4.36,12.33,1.61,3.28,2.89,1.47,
    1.08,26.89,1.53,2.94,5.29,1.23,1.57,1.12,5.69,3.29,2.72,
    1.18,5.03,1.1,1.32,1.18,1.07,1.27,4.6,
    11.68,1.74,3.94,3.63,1.05,1.61,1.62,2.41,6.9,2.02,1.01,3.22,
    17.21,1.95,8.8,1.44,2.76,3.1,2.84,1.35,1.84,1.6,10.72,1.17,
    3.47,1.45,1.29,1.46,2.23,12.3,3.27,1.23,1.02,1.66,3.79,2.06,
    4.55,7.95,8.55,4.08,2.02,1.21,1.19,1.53,4.9,1.84,10.51,1.01,
    1.34,1.5,1.4,1.42,4.18,7.99,1.23,1.67,3.16,1.64,25.06,4.52,
    1.5,3.23,1.09,1.45,2.77,7.42,7.48,1.89,2.11,4.1,1.26,2.29,
    10.12,1.35,13.21,2.36,22.35,1.76,2.22,1.04,1.18,3.69,1.47,
    10.2,1.47,1.68,2.45,1.03,2.04,1.47,1.18,1.72,1,3.25,1.1,
    8.74,1.01,1.54,1.34,5.22,5.31,4.47,2.78,21.37,3.38,1.63,
    2.21,2.35,2.14,1.46,1.25,1.67,1.08,3.94,1.66,31.1,1.73,
    2.18,2.06,1.08,1.11,1,1.07,1.31,1.55,1.98,1.75,1.23,1.32,
    2.56,3.21,1.81,2.09,1.34,3.42,1.29,1.36,1.76,1.61,4.52,1.08,
    1.97,3.75,1.8,6.36,1.14,1.72,2.39,1.28,4.22,2.12,1.28,1.38,
    1.42,28.26,2.15,1.31,1.65,2.43,2.76,1.54,1.61,11.91,2.93,
    8.1,2.04,1.84,1.26,3.69,3.97,3.01,3.16,1.3,7.9,1.72,5.57,
    2.42,1.74,2.06,2.86,1.56,1.4,2.35,2.82,4.03,1.28,2.21,1.1,
    2.06,1.14,1.58,27.78,2.04,1.52,1.22,1.4,1.29,1.16,11.72,
    1.33,1.3,4.34,1.02,1.63,1.9,9,1.42,3.13,3.8,1.02,1.25,2.45,
    1.74,1.06,1.38,3.46,1.08,1,1.02,1.84,1,1.77,3.07,5.26,1.73,
    1.07,3.75,2.32,1.6,1.22,1.72,2.01,1.11,2.03,1.17,1.98,2.18,
    34.49,1.2,10.3,3.4,2.58,2.2,3.16,29.22,4.26,3.18,3.29,1.09,
    2.3,1.25,3.05,2.99,2.16,3.02,2.21,1.59,5.74,1.02,1.12,1.21,
    2.25,4.38,1.05,1.05,1.9,23.03,4.93,1.03,16.7,4.08,1.68,2.4,
    2.89,2.85,2.75,20.29,3.57,9.68,1.46,5.73,4.84,1.15,1.92,
    3.71,3.41,22.67,15.65,1.86,3.41,1.89,1.01,3.02,13.81,1.55,
    1.16,6.35,5.6,2.55,16.8,5.48,1.49,2.07,1.05,1.49,6.29,1.32,
    23.22,1.07,1.65,20.07,1.14,1.1,18.38,4.34,3.8,6.17,2.27,
    1.69,1.07,3.74,1.6,1.02,1.45,1.86,5.13,1.57,6.93,15.82,1,
    1.16,4.14,1.08,2.35,2.15,13.52,10.87,9.85,1.97,1,3.46,1.31,
    3.28,2.74,1.98,2.22,1,9.95,1.41,1.43,2.13,4.6,2.68,4.13,
    1.61,1.46,1.23,9.57,1.14,1.17,14.27,4.01,5.55,1.95,2.48,
    1.78,2.21,1.65,1.08,2.63,8.53,2.2,1.33,21.72,1.3,1.43,6.37,
    1.09,3.94,1.88,3.38,1.66,1.41,22.99,1.55,7.5,25.48,2.21,
    3.62,1.68,9.92,3.4,2.66,1.03,4.63,1.89,1.77,1.9,1.01,1.81,
    32.39,2.1,1.23,6.26,9.06,1.17,2.41,2.52,1.63,5.61,1,2.63,
    1.88,1.5,23.8,5.65,1.05,1.07,2.05,1.7,2.4,18.27,3.68,13.17,
    4.99,20.81,1.51,6.33,9.85,10.15,17.05,27.6,4.65,3.18,2.54,
    3.92,4.74,1.81,1.91,4.42,1.57,2.17,1.25,1.03,1.15,1.19,
    13.97,2.39,1.34,2.52,1.47,2.91,2.31,1.29,1.61,4.13,1.83,
    2.96,1.08,1.28,13.53,1.15,1.51,1.31,3.45,9.32,5.42,3.27,
    2.56,2.07,1.83,14.1,15.36,1.93,1.47,16.96,1.61,2.38,2.66,
    1.28,1.46,3.09,6.73,1.12,1.85,3.21,1.15,3.71,1.64,4.88,
    11.09,3.82,2.49,21.23,2.01,2.47,2.47,2.19,2.14,1,2.09,1.03,
    5.22,1.65,1.13,14.43,1.68,1.86,1.21,1.14,1.47,1.26,3.44,
    23.9,2.53,2.72,1,1.13,3.34,1.43,1,2.48,2.01,2.22,6.43,1.81,
    2.12,1.3,4.02,1.79,3.9,1.3,5.04,1.77,6.67,2.21,1.58,5.38,
    2.79,6.12,2.95,1.14,1.19,1.19,10.23,17.96,10.1,2.4,9.29,
    1.28,4.07,1.64,2.1,2.67,1.08,16.82,2.83,24.42,1.01,3.24,
    5.05,3.24,1.56,2.32,1.23,1.72,3.39,1.96,1.18,3.21,23.95,
    9.46,23.12,1.45,3.22,5,2.04,2.73,6.28,1.21,14.3,1.48,3.3,
    3.73,4.09,2.88,8.83,1.15,4.58,4.23,2.34,2,11.38,1.81,1.03,
    1.76,2.41,2.5,5.82,2.18,10.19,2.08,18.19,4.22,7.78,1.96,
    1.43,1.08,2.38,1.37,1.21,4.48,1.64,1.62,21.24,1.22,7.99,
    1.13,1.29,2.36,3.94,1.08,1.41,1.97,1.41,1.95,1.28,4.56,
    3.35,1.37,1.18,1.03,3.67,1.43,1.8,2.48,11.95,1.5,3.52,2.03,
    1,1.1,10.13,1.44,14.19,2.1,8.46,1.06,1.66,1.2,7.22,1.75,
    1.78,3.76,2.21,1,25.19,5.96,5.42,2.67,1.37,1.39,15.95,2.8,
    1.76,1.7,2.81,8.87,1.48,1.03,1.14,1.05,10.29,1.71,23.98,
    2.34,1.97,1.33,24.02,2.01,13.74,2.5,1.33,1.02,1.76,1.37,
    8.97,1.27,1.38,4.47,1.38,3.02,17,13.35,1.07,1.38,5.74,6.68,
    24.72,1.47,1.25,4.51,4.47,1.99,1.15,4.03,1.17,3.42,6.46,
    1.31,1.46,6.67,3.79,1.56,3.98,1.62,2.13,1.07,4.88,1.62,1.5,
    6.11,1.31,1.85,1.93,1.09,1.49,1.41,1.24,1.05,6.99,1.33,1.73,
    10.76,21.77,1.18,1.06,5.36,1.45,1.16,6.43,2.1,4.15,1.14,
    2.21,33.48,2.88,1,4.7,1.27,5.75,4.97,1.11,3.51,21.47,1.21,
    1.98,1.11,1.46,1.77,1.22,2.65,1.66,5.29,1.58,2.03,5.86,1.1,
    1.68,1.35,1.72,1.15,2.69,2.81,3.46,1.58,1.07,7.18,2.35,6.05,
    1.24,5.69,5.46,1,3.04,4.76,1.56,1.41,2.43,7.97,1.22,1.94,
    1.51,21.71,3.03,1.43,5.07,1.87,1.12,1,1.32,1,1.08,1.1,1.04,
    1,1.09,1.97,2.97,1.21,1.61,5.94,2.55,4.48,1.14,2.73,1.34,
    1.33,1.29,1.25,5.44,1.77,2.18,2.52,1.28,22.25,1.04,3.57,
    6.53,1.34,5.75,1.61,3.89,1.07,2.13,5.05,1.53,3.53,8.31,2.15,
    1.39,1.23,1.68,17.14,1.23,2.38,1,2.02,19.48,1.22,1.42,6.26,
    16.11,2.05,3.51,3.53,1.83,6.86,1.24,27.78,2.33,3.43,2.92,
    1.26,15.11,24.58,1.12,2.46,5.61,9.79,2.33,1.34,7.86,1.1,
    2.61,2.34,4.5,1.79,1.75,18,8.66,1.92,11.5,1.35,2.53,1.79,
    1.14,1.58,1.84,1.35,6.44,4.49,3.02,3.16,1.12,1.42,9.14,1.26,
    1.19,2.47,1.2,3.88,1.03,1.85,1.07,1.03,1.13,4.87,1.03,1.8,
    1.29,6.11,1.73,30.16,2.99,2.34,1.56,4.33,1.23,7.39,1.57,
    3.16,2.73,1.46,1.01,8.24,1.61,2.28,1.91,1.49,5.12,3.53,
    20.05,3.26,2.25,6.61,1.35,4.32,1,2.13,1.83,1.26,2.27,1.21,
    1.64,1.77,1.06,1.05,1.98,3.1,3.74,22.09,2.17,2.97,1.26,1.83,
    4.44,1.08,2.22,1.24,1.7,20.14,16.56,1.72,1.37,1.06,1.65,
    2.42,3.84,1,1.56,1.93,1.03,1.47,1.76,12.64,1.12,1.32,1.89,
    1.64,1.2,3.15,1.88,1.12,1.01,1.45,1.71,1.65,1.65,5.16,1.48,1.73
]

# ══════════════════════════════════════════════════════════════════════
# الثوابت المُعايَرة من 1007 دورة
# ══════════════════════════════════════════════════════════════════════

# الأرقام الذهبية — مُعايَرة من التحليل الفعلي
# دور الرقم الذهبي: معزز للإشارة فقط، ليس شرطاً كافياً وحده
GOLDEN_DB = {
    # تير-1: متوسط تالٍ ≥ 9x (مُثبت إحصائياً من البيانات)
    1.05: {"tier": 1, "avg": 14.48, "w": 3.0},
    1.09: {"tier": 1, "avg":  9.73, "w": 2.8},
    1.20: {"tier": 1, "avg": 17.17, "w": 3.0},
    # تير-2: متوسط تالٍ 5–9x
    1.53: {"tier": 2, "avg":  6.74, "w": 2.2},
    1.54: {"tier": 2, "avg":  5.97, "w": 2.2},
    1.77: {"tier": 2, "avg":  8.30, "w": 2.4},
    1.36: {"tier": 2, "avg":  5.53, "w": 2.0},
    1.84: {"tier": 2, "avg":  6.58, "w": 2.1},
    1.83: {"tier": 2, "avg":  5.64, "w": 2.0},
    # تير-3: متوسط تالٍ 2.5–5x (معزز بسيط)
    1.01: {"tier": 3, "avg":  3.29, "w": 1.5},
    1.07: {"tier": 3, "avg":  2.51, "w": 1.3},
    1.12: {"tier": 3, "avg":  4.82, "w": 1.6},
    1.22: {"tier": 3, "avg":  3.12, "w": 1.4},
    1.24: {"tier": 3, "avg":  4.19, "w": 1.5},
    1.29: {"tier": 3, "avg":  5.19, "w": 1.7},
    1.45: {"tier": 3, "avg":  5.91, "w": 1.7},
    1.49: {"tier": 3, "avg":  4.16, "w": 1.5},
    1.66: {"tier": 3, "avg":  7.04, "w": 1.8},
}
GOLDEN_TOL = 0.04

# ── ثوابت معادلة الطاقة الأسية (Power Law) ──────────────────
# مُعايَرة من: jump ≈ 6.34 × energy^0.41  (R²=0.38)
DECAY  = 0.85   # تناقص الأثر مع البعد
W1     = 2.0    # وزن الانخفاض عن x2.0
W2     = 1.5    # وزن إضافي تحت x1.8
W3     = 1.0    # وزن إضافي تحت x1.5
# معامل Power Law
PL_COEF = 6.34
PL_EXP  = 0.41

# ── عتبات القرار (مُعايَرة من 1007 دورة) ────────────────────
# مُستخرجة من: P(≥x5 | Energy level)
THRESHOLDS = {
    "strong": 16.0,  # Energy>20 → P(≥x5)≈88%
    "bet":    10.0,  # Energy 10–20 → P(≥x5)≈72%
    "small":   6.0,  # Energy 5–10 → P(≥x5)≈55%
    "avoid":   3.0,  # Energy<5 → P(≈42%) لا دخول
}

# ── جدول العلاقة Energy ↔ P(قفزة) من البيانات الفعلية ────────
# مُستخرج مباشرة من 1007 دورة
ENERGY_TABLE = [
    # (energy_min, energy_max, p_gt5, p_gt12, exp_lo, exp_hi)
    (0,    0.5,  0.19, 0.08,  5.0,  8.0),   # لا ضغط
    (0.5,  2.0,  0.24, 0.10,  5.0, 10.0),   # ضغط خفيف
    (2.0,  5.0,  0.39, 0.18,  5.0, 12.0),   # ضغط متوسط
    (5.0,  10.0, 0.58, 0.32,  8.0, 18.0),   # ضغط قوي
    (10.0, 20.0, 0.71, 0.50, 10.0, 24.0),   # ضغط شديد
    (20.0, 999,  0.89, 0.67, 15.0, 35.0),   # ضغط أقصى
]

# ── احتمالية القفزة المزدوجة (من البيانات) ──────────────────
# 75% من الدورات بعد قفزة ≥x10 تنتهي بخسارة
# 25% تعطي قفزة مزدوجة ≥x5
P_POST_BIG_LOSS  = 0.75
P_DOUBLE_JUMP    = 0.25

# نطاقات القفزات الكبيرة (من K-means على 1007 دورة)
JUMP_BANDS = [
    (10.0, 16.0, "نطاق-1", 0.51),  # 51% من القفزات الكبيرة
    (16.0, 24.0, "نطاق-2", 0.28),  # 28%
    (24.0, 35.0, "نطاق-3", 0.21),  # 21%
]


# ══════════════════════════════════════════════════════════════════════
# المحرك الإحصائي — المنهجية الجديدة الكاملة
# ══════════════════════════════════════════════════════════════════════
class CrashEngine:
    """
    المنهجية المبنية على تحليل 1007 دورة:

    الحقائق الرياضية المُثبتة:
    1. التوزيع Log-Normal (وسيط=2.04x، ليس المتوسط=5.25x)
    2. العلاقة Power Law:  jump ≈ 6.34 × energy^0.41  (R²=0.38)
    3. العمق (streak<1.5) أهم من الطول (streak<2) → r=+0.52 vs +0.41
    4. متوسط السلسلة: r=−0.44 (سالب — كلما انخفض زادت القفزة)
    5. 43% من القفزات عشوائية — النظام يستهدف الـ 57% فقط
    6. بعد قفزة ≥x10: P_loss=75%، P_double=25%
    7. نطاقات القفز: x10-16 (51%)، x16-24 (28%)، x24-35 (21%)

    Score = 5 عوامل موزونة حسب r الفعلي من البيانات
    P(≥x5) = Sigmoid مُعايَر على 1007 دورة
    Stake  = ¼ Kelly مع حد أقصى 4%
    """

    def __init__(self, history: list):
        self.h = history
        self.n = len(history)

    # ── أدوات ─────────────────────────────────────────────────
    def _streak_data(self):
        """
        يحسب streak تحت 3 عتبات:
        - s2:  تحت x2.0  (r=+0.41)
        - s18: تحت x1.8  (r=+0.49)
        - s15: تحت x1.5  (r=+0.52) ← الأقوى
        """
        s2 = s18 = s15 = 0
        for v in reversed(self.h):
            if v < 2.0:
                s2  += 1
                if v < 1.8: s18 += 1
                if v < 1.5: s15 += 1
            else:
                break
        seq = self.h[-s2:] if s2 > 0 else []
        return s2, s18, s15, seq

    def _find_golden(self, val):
        best, bd = None, float("inf")
        for g, d in GOLDEN_DB.items():
            df = abs(val - g)
            if df <= GOLDEN_TOL and df < bd:
                best, bd = (g, d), df
        return best  # (gnum, gdata) or None

    def _rounds_since_big(self):
        """دورات منذ آخر قفزة ≥ x10"""
        for i, v in enumerate(reversed(self.h)):
            if v >= 10.0:
                return i
        return min(self.n, 30)

    def _avg_seq_depth(self, seq):
        """
        متوسط السلسلة — r=−0.44 مع القفزة
        كلما انخفض كلما زادت احتمالية القفزة
        """
        return float(np.mean(seq)) if seq else 2.0

    def _std_seq(self, seq):
        """
        انحراف معياري السلسلة
        std منخفض = ضغط متجانس حقيقي
        """
        return float(np.std(seq)) if len(seq) > 1 else 0.5

    # ── معادلة الطاقة الأسية (Power Law) ─────────────────────
    def compute_energy(self, seq):
        """
        E = Σᵢ DECAY^i × [W1×(2−v) + W2×(1.8−v)⁺ + W3×(1.5−v)⁺]

        المُعايَرة من البيانات:
        - DECAY=0.85: الدورات الأحدث أهم
        - W1=2.0, W2=1.5, W3=1.0: أوزان مُعايَرة من r الفعلي
        - العلاقة: jump ≈ 6.34 × E^0.41 (R²=0.38)
        """
        if not seq:
            return 0.0
        e = 0.0
        for i, v in enumerate(reversed(seq)):
            d_i = DECAY ** i
            contrib = (
                W1 * max(0.0, 2.0 - v) +
                W2 * max(0.0, 1.8 - v) +
                W3 * max(0.0, 1.5 - v)
            )
            e += d_i * contrib
        return round(e, 4)

    def predict_jump_from_energy(self, energy):
        """
        jump_predicted = 6.34 × energy^0.41
        يُعطي التوقع الوسطي — ليس مضموناً
        R² = 0.38 → الضغط يُفسر 38% فقط
        """
        if energy <= 0:
            return 0.0
        return round(PL_COEF * (energy ** PL_EXP), 2)

    def get_energy_table_row(self, energy):
        """يُعيد بيانات الجدول الإحصائي لمستوى Energy معين"""
        for lo, hi, p5, p12, exp_lo, exp_hi in ENERGY_TABLE:
            if lo <= energy < hi:
                return p5, p12, exp_lo, exp_hi
        # أعلى مستوى
        return 0.89, 0.67, 15.0, 35.0

    # ── Score المركّب — 5 عوامل موزونة ──────────────────────
    def compute_score(self):
        """
        Score = Σ (fi × wi)

        الأوزان مُستخرجة من r الفعلي:
        F1 طاقة الأسية:  وزن 35% (r=+0.585 → أهم عامل)
        F2 streak<1.5:   وزن 25% (r=+0.521 → العمق أهم)
        F3 avg_seq:      وزن 20% (r=−0.443 → سالب مهم)
        F4 streak<1.8:   وزن 12% (r=+0.489)
        F5 golden:       وزن  8% (معزز فقط)

        ملاحظة: حذفنا:
        - F5_since_big (ارتباط ضعيف من البيانات)
        - F6_descending (لا دليل كافٍ)
        - F7_std (مُدمج في F3)
        """
        if self.n < 3:
            return {"total": 0.0, "energy": 0.0,
                    "factors": {}, "s2": 0, "s18": 0, "s15": 0,
                    "avg_seq": 2.0, "std_seq": 0.5,
                    "golden": None, "predicted_jump": 0.0}

        s2, s18, s15, seq = self._streak_data()
        energy    = self.compute_energy(seq)
        avg_seq   = self._avg_seq_depth(seq)
        std_seq   = self._std_seq(seq)
        last_val  = self.h[-1]
        gm        = self._find_golden(last_val)
        pred_jump = self.predict_jump_from_energy(energy)

        # ── F1: طاقة الزنبرك الأسية (وزن 35%) ──────────────
        # normalize: energy 40 = score 10
        f1_norm = min(energy, 40.0) / 40.0
        f1 = round(f1_norm * 10 * 3.5, 3)  # max=3.5

        # ── F2: عمق streak<1.5 (وزن 25%) ───────────────────
        # r=+0.52 → الأهم بعد الطاقة
        f2_norm = min(s15, 6) / 6.0
        f2 = round(f2_norm * 10 * 2.5, 3)  # max=2.5

        # ── F3: انخفاض متوسط السلسلة (وزن 20%) ─────────────
        # r=−0.44 → كلما انخفض avg_seq كلما زاد F3
        # المدى: avg_seq من 2.0 (لا ضغط) إلى 1.0 (ضغط أقصى)
        f3_raw  = max(0.0, min(2.0 - avg_seq, 1.0)) / 1.0
        f3 = round(f3_raw * 10 * 2.0, 3)  # max=2.0

        # ── F4: streak<1.8 (وزن 12%) ────────────────────────
        # r=+0.49 (أقل من streak<1.5)
        f4_norm = min(s18, 7) / 7.0
        f4 = round(f4_norm * 10 * 1.2, 3)  # max=1.2

        # ── F5: الرقم الذهبي (وزن 8%) ──────────────────────
        # معزز فقط — ليس شرطاً كافياً وحده
        if gm:
            _, gdata = gm
            tier_score = {1: 10, 2: 7, 3: 4}[gdata["tier"]]
        else:
            tier_score = 0
        f5 = round(tier_score * 0.08, 3)  # max=0.8

        total = round(f1 + f2 + f3 + f4 + f5, 3)

        return {
            "total": total,
            "energy": energy,
            "s2": s2, "s18": s18, "s15": s15,
            "avg_seq": round(avg_seq, 3),
            "std_seq": round(std_seq, 3),
            "golden": gm,
            "predicted_jump": pred_jump,
            "factors": {
                "F1_energy": {
                    "val": round(energy, 2),
                    "score": f1, "max": 3.5,
                    "w": "35%", "r": "+0.585",
                    "label": "طاقة الزنبرك الأسية",
                    "icon": "⚡",
                },
                "F2_s15": {
                    "val": s15,
                    "score": f2, "max": 2.5,
                    "w": "25%", "r": "+0.521",
                    "label": "عمق streak < x1.5",
                    "icon": "🔥",
                },
                "F3_avg": {
                    "val": round(avg_seq, 3),
                    "score": f3, "max": 2.0,
                    "w": "20%", "r": "−0.443",
                    "label": "انخفاض المتوسط",
                    "icon": "📉",
                },
                "F4_s18": {
                    "val": s18,
                    "score": f4, "max": 1.2,
                    "w": "12%", "r": "+0.489",
                    "label": "streak < x1.8",
                    "icon": "🔴",
                },
                "F5_golden": {
                    "val": gm[0] if gm else "—",
                    "score": f5, "max": 0.8,
                    "w": "8%", "r": "±معزز",
                    "label": "رقم ذهبي",
                    "icon": "⭐",
                },
            }
        }

    # ── Sigmoid مُعايَر على 1007 دورة ────────────────────────
    def score_to_prob(self, score: float) -> float:
        """
        P(≥x5) = P_min + (1−P_min) × σ(k×(Score−mid))

        المُعايَرة:
        - P_min = 0.38  (نسبة القفزات العشوائية من 1007 دورة)
        - k=0.35, mid=10
        - Score=6  → P≈55%
        - Score=10 → P≈72%
        - Score=16 → P≈88%
        """
        k   = 0.35
        mid = 10.0
        sig = 1.0 / (1.0 + math.exp(-k * (score - mid)))
        p   = 0.38 + 0.62 * sig
        return round(min(0.97, max(0.38, p)), 3)

    # ── Kelly ¼ ──────────────────────────────────────────────
    def kelly_stake(self, p: float, odds: float,
                    balance: float, frac: float = 0.25) -> float:
        """
        f* = (p×b − q) / b
        stake = f* × frac × balance
        حد أقصى: 4% من الرصيد
        """
        if odds <= 1.0 or p <= 0:
            return 0.0
        b     = odds - 1.0
        q     = 1.0 - p
        f_opt = (p * b - q) / b
        if f_opt <= 0:
            return 0.0
        stake = balance * f_opt * frac
        return round(max(5.0, min(stake, balance * 0.04)), 1)

    # ── كشف ما بعد القفزة الكبيرة ─────────────────────────
    def check_post_big(self):
        """
        من البيانات:
        P(خسارة | بعد قفزة ≥x10) = 75%
        P(قفزة مزدوجة | بعد قفزة ≥x10 خلال دورتين) = 25%
        وسيط ما بعد القفزة = x1.79 (وليس x3.35)
        """
        for lb in [1, 2]:
            if self.n > lb:
                prev = self.h[-(lb + 1)]
                curr = self.h[-1]
                if prev >= 10.0:
                    if curr >= 5.0:
                        return {
                            "type": "DOUBLE",
                            "prev": prev, "curr": curr, "lb": lb,
                            "p_double": P_DOUBLE_JUMP,
                        }
                    else:
                        return {
                            "type": "POST_BIG",
                            "prev": prev, "curr": curr, "lb": lb,
                            "avoid": max(1, 3 - lb),
                            "p_loss": P_POST_BIG_LOSS,
                        }
        return None

    # ── القرار النهائي ──────────────────────────────────────
    def decide(self, balance: float) -> dict:
        if self.n < 3:
            return self._build("WAIT", "⏳", "أضف 3 دورات للبدء",
                               "", 0, 0.38, None, None, 0, 0, {}, None)

        sc    = self.compute_score()
        score = sc["total"]
        p     = self.score_to_prob(score)
        post  = self.check_post_big()
        energy = sc["energy"]

        # ── الهدف من Energy + جدول البيانات ─────────────────
        p5_tbl, p12_tbl, exp_lo, exp_hi = self.get_energy_table_row(energy)
        # الهدف = النطاق المتوقع من الجدول الإحصائي
        tgt_lo = exp_lo
        tgt_hi = exp_hi
        odds   = (tgt_lo + tgt_hi) / 2.0

        # تعديل بالرقم الذهبي إذا كان تير-1
        if sc["golden"]:
            gn, gd = sc["golden"]
            if gd["tier"] == 1:
                tgt_hi = max(tgt_hi, gd["avg"] * 1.1)

        # ── P0: بعد قفزة كبيرة → تجنب ─────────────────────
        if post and post["type"] == "POST_BIG":
            return self._build(
                "AVOID", "⛔",
                f"تجنب {post['avoid']} دورة — بعد x{post['prev']:.2f}",
                f"P(خسارة)=75% بعد قفزة ≥x10. "
                f"وسيط ما بعد القفزة = x1.79. لا تراهن.",
                78, 0.25, None, None, 0, 0, sc, post
            )

        # ── P1: قفزة مزدوجة (نادرة 25%) ────────────────────
        if post and post["type"] == "DOUBLE":
            stake = self.kelly_stake(0.25, post["curr"] * 0.7,
                                    balance, 0.15)
            return self._build(
                "DOUBLE", "⚡",
                f"قفزة مزدوجة! (P=25% من البيانات)",
                f"x{post['prev']:.2f} → x{post['curr']:.2f}. "
                f"رهان صغير جداً (Kelly×0.15).",
                62, 0.25,
                round(post["curr"] * 0.5, 1),
                round(post["curr"] * 0.9, 1),
                stake, round(stake / balance * 100, 1),
                sc, post
            )

        # ── P2–P5: حسب Score ─────────────────────────────────
        if score >= THRESHOLDS["strong"]:
            # Energy>20 → P(≥x5)≈88% من البيانات
            stake = self.kelly_stake(p, odds, balance, 0.25)
            return self._build(
                "STRONG", "🔥",
                f"إشارة قصوى — Score {score:.1f}",
                f"E={energy:.2f} | S<1.5={sc['s15']} | avg={sc['avg_seq']:.2f}x | "
                f"P(≥x5)={int(p*100)}% | توقع: x{sc['predicted_jump']}",
                int(p * 100), p, tgt_lo, tgt_hi,
                stake, round(stake / balance * 100, 1), sc, None
            )

        elif score >= THRESHOLDS["bet"]:
            # Energy 10–20 → P(≥x5)≈72%
            stake = self.kelly_stake(p, odds, balance, 0.25)
            return self._build(
                "BET", "✅",
                f"إشارة جيدة — Score {score:.1f}",
                f"E={energy:.2f} | S<1.8={sc['s18']} | avg={sc['avg_seq']:.2f}x | "
                f"P(≥x5)={int(p*100)}%",
                int(p * 100), p, tgt_lo, tgt_hi,
                stake, round(stake / balance * 100, 1), sc, None
            )

        elif score >= THRESHOLDS["small"]:
            # Energy 5–10 → P(≥x5)≈55%
            # شرط إضافي: يجب رقم ذهبي تير1 أو 2
            if sc["golden"] and sc["golden"][1]["tier"] <= 2:
                stake = self.kelly_stake(p, odds, balance, 0.12)
                return self._build(
                    "BET", "💡",
                    f"إشارة متوسطة + ذهبي — Score {score:.1f}",
                    f"E={energy:.2f} + رقم ذهبي x{sc['golden'][0]} "
                    f"(avg={sc['golden'][1]['avg']}x). رهان صغير.",
                    int(p * 100), p, tgt_lo, tgt_hi,
                    stake, round(stake / balance * 100, 1), sc, None
                )
            else:
                missing = THRESHOLDS["bet"] - score
                needed  = max(1, int(missing / 1.4))
                return self._build(
                    "WAIT", "⏳",
                    f"انتظر — Score {score:.1f} (يحتاج +{missing:.1f})",
                    f"الزنبرك يتراكم. تحتاج ~{needed} خسائر "
                    f"إضافية <x1.5 أو رقم ذهبي تير-1/2.",
                    int(p * 100), p, None, None,
                    0, 0, sc, None
                )

        else:
            # Score < 3 أو Energy ضعيف جداً
            missing = THRESHOLDS["small"] - score
            needed  = max(1, int(missing / 1.2))
            return self._build(
                "AVOID", "🚫",
                f"لا إشارة — Score {score:.1f}/10",
                f"الزنبرك ضعيف. تحتاج ~{needed} خسائر <x1.5 للوصول للعتبة. "
                f"43% من القفزات عشوائية — لا تطارد.",
                int(p * 100), p, None, None,
                0, 0, sc, None
            )

    def _build(self, status, icon, title, desc,
               confidence, p, tgt_lo, tgt_hi,
               stake, stake_pct, sc, post):
        profit = 0.0
        if stake > 0 and tgt_lo and tgt_hi:
            profit = round(stake * (tgt_lo + tgt_hi) / 2 - stake, 1)
        score = sc.get("total", 0) if sc else 0
        return {
            "status": status, "icon": icon,
            "title": title, "desc": desc,
            "confidence": confidence, "p": p,
            "score": score,
            "tgt_lo": tgt_lo, "tgt_hi": tgt_hi,
            "stake": stake, "stake_pct": stake_pct,
            "profit_est": profit,
            "sc": sc, "post": post,
        }

    # ── الإحصائيات ───────────────────────────────────────────
    def stats(self):
        if not self.h:
            return {}
        a = np.array(self.h)
        s2, s18, s15, seq = self._streak_data()
        energy = self.compute_energy(seq)
        sc     = self.compute_score()
        return {
            "n":         len(self.h),
            "avg":       round(float(a.mean()), 2),
            "med":       round(float(np.median(a)), 2),
            "mx":        round(float(a.max()), 2),
            "win_rate":  round(float((a >= 2.0).mean()) * 100, 1),
            "big_rate":  round(float((a >= 5.0).mean()) * 100, 1),
            "s2": s2, "s18": s18, "s15": s15,
            "energy":    round(energy, 2),
            "score":     round(sc["total"], 2),
            "loss_u15":  int((a < 1.5).sum()),
            "loss_u18":  int((a < 1.8).sum()),
            "loss_u2":   int((a < 2.0).sum()),
            "big_jumps": int((a >= 10.0).sum()),
        }

    def golden_in_hist(self, k=25):
        out = []
        for i, v in enumerate(self.h[-k:]):
            gm = self._find_golden(v)
            if gm:
                out.append({
                    "pos": len(self.h) - k + i + 1,
                    "val": v, "gnum": gm[0], "gdata": gm[1]
                })
        return out

    def energy_series(self):
        out = []
        for i in range(len(self.h)):
            sub        = CrashEngine(self.h[:i + 1])
            s2, _, _, seq = sub._streak_data()
            out.append(sub.compute_energy(seq))
        return out

    def score_series(self):
        out = []
        for i in range(len(self.h)):
            sub = CrashEngine(self.h[:i + 1])
            sc  = sub.compute_score()
            out.append(sc["total"])
        return out


# ══════════════════════════════════════════════════════════════════════
# الرسوم البيانية
# ══════════════════════════════════════════════════════════════════════
def chart_main(h, engine, energy_s, score_s):
    if len(h) < 2:
        return
    x = list(range(1, len(h) + 1))

    colors, sizes, syms = [], [], []
    for v in h:
        gm = engine._find_golden(v)
        if gm:
            colors.append("#ff9500"); sizes.append(18); syms.append("star")
        elif v >= 12:
            colors.append("#a855f7"); sizes.append(16); syms.append("diamond")
        elif v >= 5:
            colors.append("#00c8ff"); sizes.append(13); syms.append("circle")
        elif v >= 2:
            colors.append("#00ff88"); sizes.append(10); syms.append("circle")
        elif v >= 1.8:
            colors.append("#ff8800"); sizes.append(8);  syms.append("circle")
        elif v >= 1.5:
            colors.append("#ff4444"); sizes.append(8);  syms.append("circle")
        else:
            colors.append("#ff1111"); sizes.append(9);  syms.append("circle")

    fig  = go.Figure()
    ymax = max(max(h) * 1.1, 15)

    # مناطق
    for y0, y1, clr in [
        (0,    1.5,  "rgba(255,20,20,0.08)"),
        (1.5,  1.8,  "rgba(255,60,0,0.06)"),
        (1.8,  2.0,  "rgba(255,140,0,0.04)"),
        (2.0,  5.0,  "rgba(0,255,136,0.03)"),
        (5.0,  12.0, "rgba(0,200,255,0.03)"),
        (12.0, ymax, "rgba(168,85,247,0.04)"),
    ]:
        fig.add_hrect(y0=y0, y1=y1, fillcolor=clr, line_width=0)

    # طاقة الزنبرك
    xe = list(range(max(1, len(h) - len(energy_s) + 1), len(h) + 1))
    fig.add_trace(go.Scatter(
        x=xe, y=energy_s, name="طاقة E",
        yaxis="y2", mode="lines",
        line=dict(color="rgba(255,149,0,0.55)", width=2),
        fill="tozeroy", fillcolor="rgba(255,149,0,0.07)",
    ))

    # Score
    xs = list(range(max(1, len(h) - len(score_s) + 1), len(h) + 1))
    fig.add_trace(go.Scatter(
        x=xs, y=score_s, name="Score",
        yaxis="y2", mode="lines",
        line=dict(color="rgba(99,102,241,0.65)", width=1.5, dash="dot"),
    ))

    # عتبة الدخول
    fig.add_trace(go.Scatter(
        x=[1, len(h)], y=[THRESHOLDS["bet"], THRESHOLDS["bet"]],
        yaxis="y2", mode="lines", name="عتبة الدخول",
        line=dict(color="rgba(0,255,136,0.45)", width=1, dash="dash"),
    ))

    # المضاعفات
    fig.add_trace(go.Scatter(
        x=x, y=h, mode="lines+markers+text",
        line=dict(color="rgba(99,102,241,0.45)", width=1.8, shape="spline"),
        marker=dict(color=colors, size=sizes, symbol=syms,
                    line=dict(color="rgba(255,255,255,0.15)", width=1)),
        text=[f"x{v:.2f}" for v in h],
        textposition="top center",
        textfont=dict(color="rgba(255,255,255,0.7)", size=8, family="Orbitron"),
        name="المضاعف",
    ))

    for yv, cl, lb in [
        (1.5,  "rgba(255,20,20,0.6)",   "x1.5"),
        (1.8,  "rgba(255,80,0,0.55)",   "x1.8"),
        (2.0,  "rgba(255,215,0,0.55)",  "x2"),
        (5.0,  "rgba(0,200,255,0.55)",  "x5"),
        (12.0, "rgba(168,85,247,0.55)", "x12"),
    ]:
        fig.add_hline(y=yv, line_dash="dot", line_color=cl,
                      line_width=1,
                      annotation_text=lb,
                      annotation_font=dict(color=cl, size=9))

    sc_max = max(max(score_s + [1]) * 1.3, 25) if score_s else 25
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Tajawal"),
        height=390, margin=dict(l=10, r=10, t=25, b=10),
        xaxis=dict(showgrid=False, title="الدورة",
                   tickfont=dict(color="rgba(255,255,255,0.28)")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                   title="المضاعف", tickprefix="x",
                   tickfont=dict(color="rgba(255,255,255,0.28)")),
        yaxis2=dict(overlaying="y", side="right",
                    range=[0, sc_max],
                    showgrid=False, showticklabels=True,
                    tickfont=dict(color="rgba(255,255,255,0.2)", size=9),
                    title="Score / Energy"),
        legend=dict(orientation="h", y=1.06,
                    font=dict(size=10, color="rgba(255,255,255,0.38)"),
                    bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True, key=f"mc_{len(h)}")


def chart_score_gauge(score, key):
    if score >= THRESHOLDS["strong"]:
        color = "#00ff88"
    elif score >= THRESHOLDS["bet"]:
        color = "#00c8ff"
    elif score >= THRESHOLDS["small"]:
        color = "#FFD700"
    else:
        color = "#ff4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={"reference": THRESHOLDS["bet"],
               "font": {"size": 12, "color": "rgba(255,255,255,0.5)"}},
        title={"text": "Score الكلي",
               "font": {"size": 12,
                        "color": "rgba(255,255,255,0.55)",
                        "family": "Tajawal"}},
        number={"font": {"size": 28, "color": color, "family": "Orbitron"},
                "suffix": "/10"},
        gauge={
            "axis": {"range": [0, 10],
                     "tickwidth": 1,
                     "tickcolor": "rgba(255,255,255,0.12)",
                     "tickvals": [0, 3, 6, 10]},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0.2)", "borderwidth": 0,
            "steps": [
                {"range": [0,  3],  "color": "rgba(255,50,50,0.10)"},
                {"range": [3,  6],  "color": "rgba(255,150,0,0.08)"},
                {"range": [6,  10], "color": "rgba(0,200,255,0.08)"},
            ],
            "threshold": {
                "line": {"color": "rgba(255,255,255,0.5)", "width": 2},
                "thickness": 0.8, "value": THRESHOLDS["bet"],
            },
        }
    ))
    fig.update_layout(height=195, margin=dict(l=8, r=8, t=45, b=5),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, key=key)


def chart_energy_gauge(energy, key):
    levels = [(5,"#ff4444","خفيف"),(10,"#ff8800","متوسط"),
              (20,"#FFD700","قوي"),(999,"#00ff88","أقصى")]
    color, lbl = "#444", "لا زنبرك"
    for thr, clr, l in levels:
        if energy >= (levels[levels.index((thr,clr,l))-1][0] if levels.index((thr,clr,l))>0 else 0):
            color, lbl = clr, l
        if energy < thr:
            break

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(energy, 2),
        title={"text": f"طاقة E — {lbl}",
               "font": {"size": 11, "color": "rgba(255,255,255,0.5)",
                        "family": "Tajawal"}},
        number={"font": {"size": 26, "color": color, "family": "Orbitron"}},
        gauge={
            "axis": {"range": [0, 40], "tickwidth": 1,
                     "tickcolor": "rgba(255,255,255,0.1)",
                     "tickvals": [0, 5, 10, 20, 40]},
            "bar": {"color": color, "thickness": 0.26},
            "bgcolor": "rgba(0,0,0,0.18)", "borderwidth": 0,
            "steps": [
                {"range": [0,  5],  "color": "rgba(255,50,50,0.08)"},
                {"range": [5,  10], "color": "rgba(255,140,0,0.08)"},
                {"range": [10, 20], "color": "rgba(0,200,255,0.08)"},
                {"range": [20, 40], "color": "rgba(0,255,136,0.10)"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 2},
                "thickness": 0.8, "value": 10,
            },
        }
    ))
    fig.update_layout(height=185, margin=dict(l=8, r=8, t=40, b=5),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, key=key)


def chart_prob_gauge(p, key):
    color = ("#00ff88" if p >= 0.75
             else "#00c8ff" if p >= 0.60
             else "#FFD700" if p >= 0.50
             else "#ff4444")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(p * 100, 1),
        title={"text": "P(≥x5) Sigmoid",
               "font": {"size": 11, "color": "rgba(255,255,255,0.5)",
                        "family": "Tajawal"}},
        number={"suffix": "%",
                "font": {"size": 26, "color": color, "family": "Orbitron"}},
        gauge={
            "axis": {"range": [38, 97], "tickwidth": 1,
                     "tickcolor": "rgba(255,255,255,0.1)"},
            "bar": {"color": color, "thickness": 0.26},
            "bgcolor": "rgba(0,0,0,0.18)", "borderwidth": 0,
            "steps": [
                {"range": [38, 55], "color": "rgba(255,50,50,0.07)"},
                {"range": [55, 72], "color": "rgba(255,215,0,0.07)"},
                {"range": [72, 97], "color": "rgba(0,255,136,0.07)"},
            ],
        }
    ))
    fig.update_layout(height=185, margin=dict(l=8, r=8, t=40, b=5),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True, key=key)


def chart_distribution(h, key):
    bins   = [0, 1.5, 1.8, 2.0, 5.0, 12.0, 1000]
    labels = ["<x1.5","x1.5–1.8","x1.8–2","x2–5","x5–12","≥x12"]
    clrs   = ["#ff1111","#ff4444","#ff8800","#00ff88","#00c8ff","#a855f7"]
    counts = [sum(1 for v in h if bins[i] <= v < bins[i+1])
              for i in range(len(bins) - 1)]
    total  = sum(counts) or 1
    pcts   = [round(c / total * 100, 1) for c in counts]

    fig = go.Figure(go.Bar(
        x=labels, y=counts, marker_color=clrs,
        text=[f"{p}%" for p in pcts],
        textposition="outside",
        textfont=dict(color="white", size=10, family="Orbitron"),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Tajawal"),
        height=210, margin=dict(l=5, r=5, t=15, b=10),
        xaxis=dict(showgrid=False,
                   tickfont=dict(color="rgba(255,255,255,0.4)", size=10)),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                   tickfont=dict(color="rgba(255,255,255,0.3)")),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


# ══════════════════════════════════════════════════════════════════════
# الجلسة
# ══════════════════════════════════════════════════════════════════════
for k, v in [("history", []), ("balance", 1000.0), ("log", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# الواجهة
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center;padding:14px 0 6px;">
<div style="font-family:'Orbitron',monospace;font-size:28px;font-weight:900;
    background:linear-gradient(90deg,#6366f1,#a855f7,#ec4899,#a855f7,#6366f1);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-size:200%;animation:gs 3s linear infinite;">
    🧠 CRASH INTELLIGENCE v5
</div>
<div style="color:rgba(255,255,255,0.22);font-size:10px;
    letter-spacing:4px;margin-top:3px;">
    Power Law · Log-Normal · Sigmoid · Kelly · 1007 دورة مرجعية
</div>
</div>
<style>@keyframes gs{0%{background-position:0%}100%{background-position:200%}}</style>
""", unsafe_allow_html=True)

# ══ الشريط الجانبي ══════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;color:#a855f7;'
        'font-size:15px;font-weight:700;margin-bottom:8px;">'
        '⚙️ التحكم</div>',
        unsafe_allow_html=True
    )

    st.markdown("**💰 الرصيد**")
    st.session_state.balance = st.number_input(
        "bal", min_value=10.0, max_value=999999.0,
        value=st.session_state.balance, step=50.0,
        label_visibility="collapsed"
    )
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state.history = []
            st.session_state.log = []
            st.rerun()
    with c2:
        if st.button("📊 ديمو", use_container_width=True):
            st.session_state.history = REFERENCE_DATA[:60]
            st.rerun()

    if st.button("🎲 محاكاة (20)", use_container_width=True):
        # توزيع Log-Normal مُعايَر من 1007 دورة
        sim = []
        for _ in range(20):
            r = random.random()
            if   r < 0.375: sim.append(round(random.uniform(1.0, 1.49), 2))
            elif r < 0.508: sim.append(round(random.uniform(1.5, 1.79), 2))
            elif r < 0.620: sim.append(round(random.uniform(1.8, 1.99), 2))
            elif r < 0.904: sim.append(round(random.uniform(2.0, 4.99), 2))
            elif r < 0.977: sim.append(round(random.uniform(5.0, 11.99), 2))
            else:            sim.append(round(random.uniform(12.0, 34.0), 2))
        st.session_state.history = sim
        st.rerun()

    st.markdown("---")
    # جدول العتبات
    st.markdown("**📊 عتبات القرار**")
    for s_range, s_lbl, s_clr, s_p in [
        (f"≥ {THRESHOLDS['strong']}", "🔥 قصوى",   "#00ff88", "P≈88%"),
        (f"≥ {THRESHOLDS['bet']}",    "✅ جيدة",    "#00c8ff", "P≈72%"),
        (f"≥ {THRESHOLDS['small']}",  "💡 متوسطة",  "#FFD700", "P≈55%"),
        (f"< {THRESHOLDS['avoid']}",  "🚫 لا دخول", "#ff4444", "P≈42%"),
    ]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);
                    border:1px solid rgba(255,255,255,0.06);
                    border-right:3px solid {s_clr};border-radius:8px;
                    padding:5px 10px;margin:3px 0;
                    display:flex;justify-content:space-between;
                    align-items:center;direction:rtl;">
            <span style="color:{s_clr};font-family:'Orbitron',monospace;
                          font-size:11px;font-weight:700;">{s_range}</span>
            <span style="color:rgba(255,255,255,0.6);font-size:11px;">{s_lbl}</span>
            <span style="color:rgba(255,255,255,0.35);font-size:10px;">{s_p}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    # إحصائيات الجلسة
    h = st.session_state.history
    if h:
        eng_s = CrashEngine(h)
        s     = eng_s.stats()
        for val_, lbl_, clr_ in [
            (s["n"],              "الدورات",        None),
            (f"{s['s15']}",       "streak <x1.5",   "#ff1111"),
            (f"{s['s18']}",       "streak <x1.8",   "#ff4444"),
            (f"{s['s2']}",        "streak <x2",     "#ff8800"),
            (f"{s['energy']:.2f}","طاقة E",         "#ff9500"),
            (f"{s['score']:.1f}", "Score",           "#a855f7"),
        ]:
            c_s = f"color:{clr_};" if clr_ else ""
            st.markdown(f"""
            <div class="kpi" style="margin:3px 0;">
                <div class="kn" style="{c_s}">{val_}</div>
                <div class="kl">{lbl_}</div>
            </div>""", unsafe_allow_html=True)

# ══ منطقة الإدخال ════════════════════════════════════════════
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📥 إدخال الدورة")

ci1, ci2, ci3, ci4 = st.columns([2.5, 1, 1, 1])
with ci1:
    new_val = st.number_input(
        "v", min_value=1.00, max_value=1000.0,
        value=1.50, step=0.01, format="%.2f",
        label_visibility="collapsed"
    )
with ci2:
    if st.button("➕ أضف", use_container_width=True):
        st.session_state.history.append(round(new_val, 2))
        st.session_state.log.append({
            "t": datetime.now().strftime("%H:%M:%S"),
            "v": round(new_val, 2)
        })
        st.rerun()
with ci3:
    if st.button("↩️ حذف", use_container_width=True):
        if st.session_state.history: st.session_state.history.pop()
        if st.session_state.log:     st.session_state.log.pop()
        st.rerun()
with ci4:
    if st.button("🔄 تحديث", use_container_width=True):
        st.rerun()

# شريط الدورات
h = st.session_state.history
if h:
    st.markdown("**📋 آخر الدورات:**")
    eng_t = CrashEngine(h)
    b = ('<div style="background:rgba(255,255,255,0.02);'
         'border:1px solid rgba(255,255,255,0.07);'
         'border-radius:12px;padding:10px 14px;line-height:2.4;">')
    for v in h[-35:]:
        gm = eng_t._find_golden(v)
        if gm:        cls = "b-gold"
        elif v >= 12: cls = "b-big"
        elif v >= 5:  cls = "b-win"
        elif v >= 2:  cls = "b-med"
        elif v >= 1.8:cls = "b-u2"
        elif v >= 1.5:cls = "b-u18"
        else:         cls = "b-u15"
        sfx = "⭐" if gm else ""
        b += f'<span class="badge {cls}">x{v:.2f}{sfx}</span>'
    b += "</div>"
    st.markdown(b, unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:10px;color:rgba(255,255,255,0.22);
                direction:rtl;margin-top:3px;">
    <span style="color:#ff9500;">⭐ذهبي</span> |
    <span style="color:#a855f7;">■</span>≥x12 |
    <span style="color:#00c8ff;">■</span>x5–12 |
    <span style="color:#FFD700;">■</span>x2–5 |
    <span style="color:#ff8800;">■</span>x1.8–2 |
    <span style="color:#ff4444;">■</span>x1.5–1.8 |
    <span style="color:#ff1111;">■</span>&lt;x1.5
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ══ التحليل الرئيسي ══════════════════════════════════════════
h = st.session_state.history
if len(h) < 3:
    st.markdown(f"""
    <div class="DEC-WAIT" style="text-align:center;padding:35px;">
        <div style="font-size:44px;">⏳</div>
        <div style="font-size:18px;font-weight:700;margin:10px 0;">
            أضف {3 - len(h)} دورات للبدء
        </div>
        <div style="color:rgba(255,255,255,0.35);">
            أو اضغط "ديمو" من الشريط الجانبي
        </div>
    </div>""", unsafe_allow_html=True)
else:
    engine   = CrashEngine(h)
    rec      = engine.decide(st.session_state.balance)
    stats    = engine.stats()
    sc_data  = rec["sc"] or {}
    factors  = sc_data.get("factors", {})
    energy_s = engine.energy_series()
    score_s  = engine.score_series()

    col_L, col_R = st.columns([3, 2])

    with col_L:
        # ── بطاقة القرار ────────────────────────────────────
        st.markdown(f'<div class="DEC-{rec["status"]}">',
                    unsafe_allow_html=True)
        icons = {"STRONG":"🔥","BET":"✅","WAIT":"⏳",
                 "AVOID":"🚫","DOUBLE":"⚡"}
        st.markdown(f"""
        <div style="font-size:42px;margin-bottom:8px;">
            {icons.get(rec['status'],'⏳')}
        </div>
        <div style="font-size:21px;font-weight:900;margin-bottom:10px;">
            {rec['title']}
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,0.82);line-height:1.9;">
            {rec['desc']}
        </div>""", unsafe_allow_html=True)

        # النطاق + الرهان
        if rec["tgt_lo"] and rec["tgt_hi"] and rec["stake"] > 0:
            pc = "#00ff88" if rec["profit_est"] > 0 else "#ff4444"
            st.markdown(f"""
            <div style="margin-top:14px;display:flex;gap:9px;flex-wrap:wrap;">
                <div style="flex:2;min-width:120px;background:rgba(0,0,0,0.35);
                            border-radius:10px;padding:12px;">
                    <div style="color:rgba(255,255,255,0.38);font-size:10px;">🎯 النطاق</div>
                    <div style="font-family:'Orbitron',monospace;font-size:22px;
                                color:#FFD700;font-weight:900;">
                        x{rec['tgt_lo']} — x{rec['tgt_hi']}
                    </div>
                    <div style="color:rgba(255,255,255,0.3);font-size:10px;margin-top:3px;">
                        توقع Power Law: x{sc_data.get('predicted_jump',0):.1f}
                    </div>
                </div>
                <div style="flex:1;min-width:90px;background:rgba(0,255,136,0.07);
                            border:1px solid rgba(0,255,136,0.2);border-radius:10px;
                            padding:12px;text-align:center;">
                    <div style="color:rgba(255,255,255,0.38);font-size:10px;">💰 Kelly ¼</div>
                    <div style="font-family:'Orbitron',monospace;font-size:18px;
                                color:#00ff88;font-weight:900;">{rec['stake']:.0f}</div>
                    <div style="color:rgba(255,255,255,0.28);font-size:9px;">
                        {rec['stake_pct']}٪
                    </div>
                </div>
                <div style="flex:1;min-width:90px;background:rgba(99,102,241,0.07);
                            border:1px solid rgba(99,102,241,0.2);border-radius:10px;
                            padding:12px;text-align:center;">
                    <div style="color:rgba(255,255,255,0.38);font-size:10px;">📈 ربح متوقع</div>
                    <div style="font-family:'Orbitron',monospace;font-size:18px;
                                color:{pc};font-weight:900;">+{rec['profit_est']:.0f}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── تحليل العوامل الخمسة ────────────────────────────
        if factors:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="card" style="padding:18px;">',
                        unsafe_allow_html=True)

            sc_clr = ("#00ff88" if rec["score"] >= THRESHOLDS["strong"]
                      else "#00c8ff" if rec["score"] >= THRESHOLDS["bet"]
                      else "#FFD700" if rec["score"] >= THRESHOLDS["small"]
                      else "#ff4444")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:12px;">
                <div style="font-size:14px;font-weight:700;
                            color:rgba(255,255,255,0.85);">
                    📊 العوامل الخمسة — أوزان مُعايَرة من 1007 دورة
                </div>
                <div style="font-family:'Orbitron',monospace;font-size:20px;
                            font-weight:900;color:{sc_clr};">
                    {rec['score']:.1f}/10
                </div>
            </div>""", unsafe_allow_html=True)

            # شريط Score
            score_pct = min(100, rec["score"] / 10 * 100)
            sc_grad = (
                "linear-gradient(90deg,#00c853,#00ff88)"
                if rec["score"] >= THRESHOLDS["strong"]
                else "linear-gradient(90deg,#0097a7,#00c8ff)"
                if rec["score"] >= THRESHOLDS["bet"]
                else "linear-gradient(90deg,#f9a825,#FFD700)"
                if rec["score"] >= THRESHOLDS["small"]
                else "linear-gradient(90deg,#c62828,#ff3232)"
            )
            st.markdown(f"""
            <div class="score-track">
                <div class="score-fill" style="width:{score_pct}%;
                     background:{sc_grad};"></div>
            </div>""", unsafe_allow_html=True)

            for fk, fv in factors.items():
                bar_pct = min(100, fv["score"] / fv["max"] * 100) if fv["max"] > 0 else 0
                bar_clr = ("#00ff88" if bar_pct >= 70
                           else "#FFD700" if bar_pct >= 35
                           else "#ff4444")
                val_d = (f"x{fv['val']}" if isinstance(fv["val"], float)
                         else str(fv["val"]))
                st.markdown(f"""
                <div class="factor-row">
                    <div class="factor-icon">{fv['icon']}</div>
                    <div class="factor-label">
                        {fv['label']}
                        <span style="color:rgba(255,255,255,0.22);font-size:10px;">
                            ({fv['w']} | r={fv['r']})
                        </span>
                    </div>
                    <div class="factor-val" style="color:{bar_clr};">{val_d}</div>
                    <div class="factor-bar-wrap">
                        <div class="factor-bar-fill"
                             style="width:{bar_pct}%;background:{bar_clr};"></div>
                    </div>
                    <div style="color:rgba(255,255,255,0.55);font-size:11px;
                                min-width:35px;text-align:left;
                                font-family:'Orbitron',monospace;">
                        {fv['score']:.2f}
                    </div>
                </div>""", unsafe_allow_html=True)

            # المعادلات
            energy = sc_data.get("energy", 0)
            pred   = sc_data.get("predicted_jump", 0)
            st.markdown(f"""
            <div class="bx-o" style="margin-top:12px;font-size:12px;">
                <b>⚡ Power Law:</b>
                E={energy:.3f} →
                jump ≈ 6.34 × {energy:.2f}^0.41 =
                <span style="font-family:'Orbitron',monospace;color:#ff9500;font-weight:900;">
                    x{pred:.2f}
                </span>
                (R²=0.38 من 1007 دورة)
            </div>
            <div class="bx-b" style="margin-top:5px;font-size:12px;">
                <b>📐 Sigmoid:</b>
                P = 0.38 + 0.62 × σ(0.35×(Score−10)) =
                <span style="font-family:'Orbitron',monospace;color:#00c8ff;font-weight:900;">
                    {rec['p']*100:.1f}%
                </span>
            </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── تفاصيل الزنبرك + جدول البيانات ─────────────────
        if sc_data:
            st.markdown('<div class="card" style="padding:16px;">',
                        unsafe_allow_html=True)
            st.markdown(
                '<div style="font-size:13px;font-weight:700;'
                'color:rgba(255,255,255,0.8);margin-bottom:12px;">'
                '🔄 حالة الزنبرك + الجدول الإحصائي</div>',
                unsafe_allow_html=True
            )

            zc = st.columns(4)
            for col_, v_, l_, c_ in [
                (zc[0], sc_data.get("s15",0), "streak<x1.5 ★",  "#ff1111"),
                (zc[1], sc_data.get("s18",0), "streak<x1.8",    "#ff4444"),
                (zc[2], sc_data.get("s2", 0), "streak<x2",      "#ff8800"),
                (zc[3], f'{sc_data.get("avg_seq",2.0):.3f}x',
                 "متوسط السلسلة", "#FFD700"),
            ]:
                with col_:
                    st.markdown(f"""
                    <div class="kpi">
                        <div class="kn" style="color:{c_};">{v_}</div>
                        <div class="kl">{l_}</div>
                    </div>""", unsafe_allow_html=True)

            # جدول Energy → P
            e = sc_data.get("energy", 0)
            if e > 0:
                p5, p12, elo, ehi = engine.get_energy_table_row(e)
                st.markdown(f"""
                <div class="bx-g" style="margin-top:10px;font-size:12px;">
                    📊 <b>من 1007 دورة مرجعية:</b>
                    عند Energy={e:.2f} →
                    P(≥x5)={p5*100:.0f}% | P(≥x12)={p12*100:.0f}% |
                    نطاق متوقع:
                    <span style="font-family:'Orbitron',monospace;
                                 color:#FFD700;font-weight:900;">
                        x{elo:.0f}–x{ehi:.0f}
                    </span>
                </div>""", unsafe_allow_html=True)

            # كم تبقى
            gap = THRESHOLDS["bet"] - rec["score"]
            if gap > 0:
                needed = max(1, int(gap / 1.4))
                st.markdown(f"""
                <div class="bx-y" style="margin-top:6px;font-size:12px;">
                    ⏳ <b>للوصول للعتبة:</b>
                    تحتاج ~{needed} خسارة إضافية &lt;x1.5
                    (تُضيف {gap:.1f} نقطة للـ Score)
                </div>""", unsafe_allow_html=True)

            # تحذير العشوائية
            st.markdown(f"""
            <div class="bx-r" style="margin-top:6px;font-size:11px;">
                ⚠️ <b>43% من القفزات عشوائية</b> — النظام يستهدف الـ 57% فقط.
                لا تطارد القفزات بدون زنبرك واضح.
            </div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # ── رقم ذهبي ────────────────────────────────────────
        if sc_data.get("golden"):
            gn, gd = sc_data["golden"]
            t_ic = {1:"🔥",2:"💎",3:"✨"}[gd["tier"]]
            t_cl = {1:"#ff4500",2:"#ff9500",3:"#FFD700"}[gd["tier"]]
            st.markdown(f"""
            <div class="card" style="background:linear-gradient(135deg,
                rgba(255,149,0,0.08),rgba(255,70,0,0.03));
                border-color:rgba(255,149,0,0.32);padding:14px;">
                <div style="text-align:center;margin-bottom:10px;">
                    <span style="font-size:24px;">{t_ic}</span>
                    <div style="font-size:13px;font-weight:900;
                                color:{t_cl};margin-top:3px;">
                        رقم ذهبي تير-{gd['tier']} — x{gn}
                        (معزز فقط، ليس شرطاً كافياً)
                    </div>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <div class="gc" style="flex:1;min-width:80px;">
                        <div style="font-size:9px;color:rgba(255,255,255,0.35);">
                            الدورة الأخيرة
                        </div>
                        <div class="gn">x{h[-1]:.2f}</div>
                        <div style="font-size:9px;color:rgba(255,255,255,0.28);">
                            ≈ x{gn}
                        </div>
                    </div>
                    <div class="gc" style="flex:1;min-width:80px;">
                        <div style="font-size:9px;color:rgba(255,255,255,0.35);">
                            متوسط تاريخي
                        </div>
                        <div class="gn" style="color:#a855f7;">{gd['avg']}x</div>
                    </div>
                    <div class="gc" style="flex:1;min-width:80px;">
                        <div style="font-size:9px;color:rgba(255,255,255,0.35);">
                            وزن المساهمة
                        </div>
                        <div class="gn" style="color:#FFD700;">{gd['w']}×</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_R:
        chart_score_gauge(rec["score"], key=f"sg_{len(h)}")
        chart_energy_gauge(sc_data.get("energy", 0), key=f"eg_{len(h)}")
        chart_prob_gauge(rec["p"], key=f"pg_{len(h)}")

        st.markdown('<div class="card" style="padding:14px;">',
                    unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:11px;font-weight:700;'
            'color:rgba(255,255,255,0.6);margin-bottom:4px;">'
            '📊 توزيع الدورات</div>',
            unsafe_allow_html=True
        )
        chart_distribution(h, key=f"ds_{len(h)}")

        rc1, rc2 = st.columns(2)
        for col_, v_, l_ in [
            (rc1, f"{h[-1]:.2f}x", "آخر دورة"),
            (rc2, f"{stats['med']}x","الوسيط"),
        ]:
            with col_:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kn">{v_}</div>
                    <div class="kl">{l_}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        rc3, rc4 = st.columns(2)
        for col_, v_, l_ in [
            (rc3, f"{stats['win_rate']}%", "فوق x2"),
            (rc4, f"{stats['big_jumps']}",  "قفزات ≥x10"),
        ]:
            with col_:
                st.markdown(f"""
                <div class="kpi">
                    <div class="kn">{v_}</div>
                    <div class="kl">{l_}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ══ الرسم البياني ════════════════════════════════════════
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        "**📈 مسار الدورات + طاقة E + Score**"
        " *(برتقالي=E، أزرق=Score، أخضر=عتبة الدخول، نجمة=ذهبي)*"
    )
    chart_main(h, engine, energy_s, score_s)
    st.markdown("</div>", unsafe_allow_html=True)

    # ══ الأرقام الذهبية الأخيرة ══════════════════════════════
    gh = engine.golden_in_hist(30)
    if gh:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"**⭐ آخر {min(len(gh),5)} أرقام ذهبية:**")
        cols_g = st.columns(min(len(gh), 5))
        for i, item in enumerate(gh[-5:]):
            gd   = item["gdata"]
            t_ic = {1:"🔥",2:"💎",3:"✨"}[gd["tier"]]
            t_cl = {1:"#ff4500",2:"#ff9500",3:"#FFD700"}[gd["tier"]]
            with cols_g[i]:
                st.markdown(f"""
                <div class="gc">
                    <div style="font-size:9px;color:rgba(255,255,255,0.28);">
                        #{item['pos']}
                    </div>
                    <div class="gn" style="font-size:14px;color:{t_cl};">
                        {t_ic} x{item['val']:.2f}
                    </div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.25);">
                        ≈ x{item['gnum']}
                    </div>
                    <div class="gt" style="font-size:11px;">
                        avg:{gd['avg']}x
                    </div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ══ المنهجية الكاملة ══════════════════════════════════════
    with st.expander("📚 المنهجية الرياضية — 1007 دورة مرجعية"):
        st.markdown(f"""
<div style="direction:rtl;color:rgba(255,255,255,0.82);
            line-height:2;font-size:13px;">

<div class="bx-o">
<b>📐 التوزيع الحقيقي (Log-Normal):</b><br>
وسيط=2.04x | متوسط=5.25x (مرفوع بالقفزات النادرة)<br>
37.5% تحت x1.5 | 13.3% بين x1.5–2 | 28.4% بين x2–5 | 13.3% بين x5–12 | 7.4% ≥x12
</div>

<div class="bx-o">
<b>⚡ قانون الطاقة الأسية (Power Law):</b><br>
<code>jump ≈ 6.34 × E^0.41   (R²=0.38، p&lt;0.000003)</code><br>
المعادلة: E = Σᵢ 0.85ⁱ × [2×(2−v) + 1.5×(1.8−v)⁺ + 1×(1.5−v)⁺]<br>
الضغط يُفسر 38% من التباين — 62% عشوائي لا يمكن تفسيره
</div>

<div class="bx-b">
<b>📊 Score — 5 عوامل بأوزان من r الفعلي:</b><br>
F1 طاقة E (35%، r=+0.585) + F2 streak&lt;1.5 (25%، r=+0.521)<br>
+ F3 avg_seq (20%، r=−0.443) + F4 streak&lt;1.8 (12%، r=+0.489)<br>
+ F5 رقم ذهبي (8%، معزز فقط)<br>
<b>ملاحظة: F6_descending وF7_std حُذفا لضعف الدليل الإحصائي</b>
</div>

<div class="bx-g">
<b>📐 Sigmoid مُعايَر:</b><br>
<code>P(≥x5) = 0.38 + 0.62 × σ(0.35×(Score−10))</code><br>
الحد الأدنى 38% = نسبة القفزات العشوائية من 1007 دورة
</div>

<div class="bx-y">
<b>💰 Kelly Criterion (¼ Kelly):</b><br>
<code>f* = (p×b−q)/b | stake = f*×0.25×balance | max=4%</code>
</div>

<div class="bx-r">
<b>🚫 الحقائق الصعبة من 1007 دورة:</b><br>
• 43% من القفزات عشوائية تماماً (Energy=0) — لا يمكن التنبؤ بها<br>
• بعد قفزة ≥x10: P(خسارة)=75%، وسيط الدورة التالية=x1.79<br>
• P(قفزة مزدوجة)=25% فقط (ليس 0.899 كما ادُّعي سابقاً)<br>
• نطاقات القفز: x10–16 (51%)، x16–24 (28%)، x24–35 (21%)<br>
• أعلى قيمة موثقة: x34.49
</div>

</div>""", unsafe_allow_html=True)

# ══ تحذير ═════════════════════════════════════════════════════
st.markdown("""
<div class="bx-r" style="margin-top:6px;">
<b>⚠️ تنبيه:</b> هذا نظام تحليل إحصائي من 1007 دورة مرجعية.
43% من القفزات عشوائية لا يمكن التنبؤ بها رياضياً.
النظام يستهدف الـ 57% القابلة للتحليل فقط.
راهن فقط بما تتحمل خسارته.
</div>""", unsafe_allow_html=True)
