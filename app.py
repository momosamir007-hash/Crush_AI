# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from collections import deque
import random
from datetime import datetime

st.set_page_config(
    page_title="🚀 Crash Predictor PRO - Golden Edition",
    page_icon="🌟",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    * { font-family: 'Tajawal', sans-serif !important; }
    body, .main { background: #060610 !important; }
    
    /* ===== بطاقات رئيسية ===== */
    .crash-card {
        background: linear-gradient(145deg, rgba(10,10,25,0.97), rgba(15,15,35,0.99));
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.8), inset 0 1px 0 rgba(99,102,241,0.2);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        direction: rtl;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .crash-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #FFD700, #ff8c00, #FFD700, transparent);
    }
    
    /* ===== الحالة الرئيسية ===== */
    .status-golden {
        background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,140,0,0.08));
        border: 2px solid #FFD700;
        box-shadow: 0 0 40px rgba(255,215,0,0.4), inset 0 0 20px rgba(255,215,0,0.1);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        animation: goldenPulse 1.5s ease-in-out infinite;
    }
    @keyframes goldenPulse { 0%,100% { box-shadow: 0 0 30px rgba(255,215,0,0.3); } 50% { box-shadow: 0 0 60px rgba(255,215,0,0.6); } }

    .status-safe {
        background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,200,100,0.06));
        border: 2px solid #00ff88;
        box-shadow: 0 0 30px rgba(0,255,136,0.3), inset 0 0 20px rgba(0,255,136,0.05);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        animation: safePulse 2s ease-in-out infinite;
    }
    @keyframes safePulse { 0%,100% { box-shadow: 0 0 20px rgba(0,255,136,0.2); } 50% { box-shadow: 0 0 50px rgba(0,255,136,0.5); } }
    
    .status-danger {
        background: linear-gradient(135deg, rgba(255,50,50,0.12), rgba(200,0,0,0.06));
        border: 2px solid #ff3232;
        box-shadow: 0 0 30px rgba(255,50,50,0.3), inset 0 0 20px rgba(255,50,50,0.05);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        animation: dangerPulse 1s ease-in-out infinite;
    }
    @keyframes dangerPulse { 0%,100% { box-shadow: 0 0 20px rgba(255,50,50,0.3); } 50% { box-shadow: 0 0 60px rgba(255,50,50,0.7); } }
    
    .status-caution {
        background: linear-gradient(135deg, rgba(255,200,0,0.12), rgba(255,140,0,0.06));
        border: 2px solid #FFD700;
        box-shadow: 0 0 25px rgba(255,215,0,0.25);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
    }
    .status-recover {
        background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(99,102,241,0.08));
        border: 2px solid #8b5cf6;
        box-shadow: 0 0 30px rgba(139,92,246,0.3);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        animation: recoverPulse 1.5s ease-in-out infinite;
    }
    @keyframes recoverPulse { 0%,100% { box-shadow: 0 0 25px rgba(139,92,246,0.25); } 50% { box-shadow: 0 0 55px rgba(139,92,246,0.55); } }
    
    /* ===== شارات الدورات ===== */
    .round-badge-win {
        display: inline-block;
        background: linear-gradient(135deg, #003d1f, #006b37);
        border: 1px solid #00ff88;
        color: #00ff88;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 900;
        margin: 4px;
        cursor: pointer;
        transition: all 0.2s;
        font-family: 'Orbitron', monospace !important;
        box-shadow: 0 4px 15px rgba(0,255,136,0.2);
    }
    .round-badge-loss {
        display: inline-block;
        background: linear-gradient(135deg, #3d0000, #6b0000);
        border: 1px solid #ff4444;
        color: #ff6666;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 900;
        margin: 4px;
        font-family: 'Orbitron', monospace !important;
        box-shadow: 0 4px 15px rgba(255,50,50,0.2);
    }
    .round-badge-medium {
        display: inline-block;
        background: linear-gradient(135deg, #1a1200, #2a2000);
        border: 1px solid #FFD700;
        color: #FFD700;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 900;
        margin: 4px;
        font-family: 'Orbitron', monospace !important;
        box-shadow: 0 4px 15px rgba(255,215,0,0.2);
    }
    
    /* ===== توصية الرهان ===== */
    .bet-target {
        background: linear-gradient(135deg, #0a0a2e, #12124a);
        border: 2px solid #6366f1;
        border-radius: 14px;
        padding: 18px 22px;
        margin: 8px 0;
        direction: rtl;
        box-shadow: 0 8px 25px rgba(99,102,241,0.2);
        transition: all 0.3s;
    }
    .bet-target:hover {
        border-color: #a855f7;
        box-shadow: 0 12px 35px rgba(168,85,247,0.3);
        transform: translateY(-2px);
    }
    .multiplier-tag {
        font-family: 'Orbitron', monospace !important;
        font-size: 26px;
        font-weight: 900;
        color: #00ff88;
        text-shadow: 0 0 15px rgba(0,255,136,0.5);
    }
    .prob-bar {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }
    .prob-fill {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
        transition: width 0.5s ease;
    }
    
    /* ===== إحصائيات ===== */
    .stat-box {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        direction: rtl;
    }
    .stat-number {
        font-family: 'Orbitron', monospace !important;
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #FFD700, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        color: rgba(255,255,255,0.4);
        font-size: 12px;
        margin-top: 5px;
        letter-spacing: 1px;
    }
    
    /* ===== قائمة الاسترداد / القناص ===== */
    .recover-item {
        background: rgba(139,92,246,0.08);
        border: 1px solid rgba(139,92,246,0.3);
        border-radius: 10px;
        padding: 12px 18px;
        margin: 5px 0;
        direction: rtl;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* ===== تحذير ===== */
    .warning-box {
        background: rgba(255,100,0,0.08);
        border: 1px solid rgba(255,100,0,0.4);
        border-right: 4px solid #ff6400;
        border-radius: 12px;
        padding: 15px 20px;
        color: rgba(255,200,150,0.9);
        font-size: 14px;
        direction: rtl;
        margin: 10px 0;
    }
    
    /* ===== ليبل السيناريو ===== */
    .scenario-tag {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 3px;
    }
    .tag-avoid { background: rgba(255,50,50,0.2); color: #ff6666; border: 1px solid #ff4444; }
    .tag-bet { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid #00cc70; }
    .tag-wait { background: rgba(255,215,0,0.15); color: #FFD700; border: 1px solid #cc9900; }
    .tag-golden { background: rgba(255,215,0,0.25); color: #FFD700; border: 1px solid #FFD700; }
    
    /* ===== شريط التاريخ ===== */
    .history-bar {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 15px 20px;
        direction: rtl;
        margin: 10px 0;
    }
    
    /* ===== زر الإدخال ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #ff8c00) !important;
        color: #060610 !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        padding: 12px 30px !important;
        box-shadow: 0 8px 25px rgba(255,215,0,0.4) !important;
        transition: all 0.3s !important;
        font-family: 'Tajawal' !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(255,215,0,0.6) !important;
    }
    .stNumberInput > div > div > input, .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,215,0,0.4) !important;
        border-radius: 10px !important;
        font-family: 'Tajawal' !important;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# ثوابت وإعدادات الاستراتيجية الذهبية الصارمة
# ══════════════════════════════════════════════════════
# الأرقام الذهبية المفلترة والمؤكدة
GOLDEN_NUMBERS = [1.01, 1.05, 1.12, 1.24, 1.54, 1.77]

# حدود الأنماط
PATTERN_THRESHOLDS = {
    "big_crash_after_12": 12.90,
    "crash_after_big_1x9": 1.90,
    "three_losses_limit": 1.80, # الحد الصارم للخسائر المتتالية
    "after_loss_range_low": 2.10,
    "after_loss_range_high": 2.90,
    "rocket_surge_low": 5.00,
    "rocket_surge_high": 6.00,
    "surge_avoid_rounds": 5,
    "medium_rise": 3.00,
    "medium_avoid": 4,
    "double_rise_limit": 2.00,
    "double_consecutive": 2,
    "long_loss_streak": 7,
}

# ══════════════════════════════════════════════════════
# منطق التحليل المتقدم
# ══════════════════════════════════════════════════════
class CrashAnalyzer:
    """
    المحرك الذكي لتحليل أنماط Crash وتوليد التوصيات مع تطبيق الاستراتيجية الذهبية
    """
    def __init__(self, history: list):
        self.history = history
        self.n = len(history)

    # ──────────────────────────────────────────
    # 1. كشف الأنماط
    # ──────────────────────────────────────────
    def _last(self, count: int) -> list:
        return self.history[-count:] if self.n >= count else self.history[:]

    def _is_rise(self, val: float, threshold: float = 2.0) -> bool:
        return val >= threshold

    def detect_patterns(self) -> list:
        patterns = []
        if self.n == 0:
            return patterns

        last1 = self.history[-1]
        last2 = self._last(2)
        last3 = self._last(3)
        
        # ── الاستراتيجية الذهبية الأقوى: إشارة الدخول ──────────────────
        if self.n >= 4:
            last4 = self._last(4)
            if all(v < PATTERN_THRESHOLDS["three_losses_limit"] for v in last4[:3]) and last4[3] in GOLDEN_NUMBERS:
                patterns.append({
                    "id": "GOLD_1",
                    "icon": "🌟",
                    "name": "إشارة الدخول الذهبية!",
                    "action": "golden_bet",
                    "rounds_to_avoid": 0,
                    "confidence": 99,
                    "reason": f"تحققت الاستراتيجية الصارمة: 3 خسائر تحت 1.8 تلاها الرقم الذهبي ({last4[3]}). ادخل الآن برهان صغير!",
                    "predicted_range": (3.0, 5.0),
                    "bet_suggestion": None,
                })

        # ── الاستراتيجية الذهبية: فخ الأرقام الوهمية (الضعيفة) ──────────
        if self.n >= 4:
            last4 = self._last(4)
            if all(v < PATTERN_THRESHOLDS["three_losses_limit"] for v in last4[:3]) and last4[3] < 2.0 and last4[3] not in GOLDEN_NUMBERS:
                patterns.append({
                    "id": "GOLD_TRAP",
                    "icon": "🚫",
                    "name": "فخ الرقم الضعيف",
                    "action": "danger",
                    "rounds_to_avoid": 1,
                    "confidence": 95,
                    "reason": f"ظهر رقم ضعيف ({last4[3]}) بعد سلسلة الخسائر وليس ضمن الأرقام الذهبية. إياك والدخول، الخوارزمية تستنزف الرصيد.",
                    "predicted_range": (1.0, 1.5),
                    "bet_suggestion": None,
                })

        # ── الاستراتيجية الذهبية: وضع القناص (الانتظار) ──────────────────
        if self.n >= 3:
            if all(v < PATTERN_THRESHOLDS["three_losses_limit"] for v in last3):
                patterns.append({
                    "id": "GOLD_WAIT",
                    "icon": "🎯",
                    "name": "وضع القناص مفعل",
                    "action": "golden_wait",
                    "rounds_to_avoid": 0,
                    "confidence": 92,
                    "reason": f"رصدنا 3 خسائر متتالية تحت x1.80. لا تراهن! راقب الشاشة وانتظر ظهور أحد الأرقام الذهبية لتدخل بعدها.",
                    "predicted_range": None,
                    "bet_suggestion": None,
                })

        # ── الأنماط الكلاسيكية المساندة ──────────────────
        if last1 >= PATTERN_THRESHOLDS["big_crash_after_12"]:
            patterns.append({
                "id": "P1",
                "icon": "💥",
                "name": "ما بعد الانفجار الكبير",
                "action": "danger",
                "rounds_to_avoid": 1,
                "confidence": 88,
                "reason": f"الدورة الأخيرة كانت x{last1:.2f}. الدورة القادمة ستنفجر مبكراً غالباً.",
                "predicted_range": (1.50, 1.90),
                "bet_suggestion": None,
            })

        if last1 >= PATTERN_THRESHOLDS["rocket_surge_low"] and last1 < 12.0:
            patterns.append({
                "id": "P3",
                "icon": "🚀",
                "name": "استكمال الصعود العالي",
                "action": "bet_range",
                "rounds_to_avoid": 0,
                "confidence": 72,
                "reason": f"احتمالية استكمال الصعود في نطاق x5-x6 (نمط ثانوي، الأولوية للاستراتيجية الذهبية).",
                "predicted_range": (5.0, 6.0),
                "bet_suggestion": 4.80,
            })

        if self.n >= 2:
            second_last = self.history[-2] if self.n >= 2 else 0
            if second_last >= 5.0 and last1 < 2.0:
                patterns.append({
                    "id": "P4",
                    "icon": "⚠️",
                    "name": "صعود ملحوظ فاتك",
                    "action": "avoid",
                    "rounds_to_avoid": PATTERN_THRESHOLDS["surge_avoid_rounds"],
                    "confidence": 75,
                    "reason": f"صعود كبير تلاه هبوط. احتمالات الخسارة عالية في الدورات القادمة.",
                    "predicted_range": (1.0, 2.0),
                    "bet_suggestion": None,
                })

        return patterns

    # ──────────────────────────────────────────
    # 2. حساب الاحتمالات
    # ──────────────────────────────────────────
    def calculate_probabilities(self, patterns: list) -> dict:
        if self.n == 0:
            return {"danger": 0.5, "safe": 0.3, "medium": 0.2, "golden": 0.0}

        losses = sum(1 for v in self.history if v < 2.0)
        wins_medium = sum(1 for v in self.history if 2.0 <= v < 5.0)
        wins_high = sum(1 for v in self.history if v >= 5.0)

        base_danger = losses / max(self.n, 1)
        base_medium = wins_medium / max(self.n, 1)
        base_high = wins_high / max(self.n, 1)

        danger_boost, safe_boost, golden_boost = 0.0, 0.0, 0.0

        for p in patterns:
            if p["action"] in ["danger", "avoid"]:
                danger_boost += 0.30 * (p["confidence"] / 100)
            elif p["action"] == "bet_range":
                safe_boost += 0.20 * (p["confidence"] / 100)
            elif p["action"] in ["golden_bet", "golden_wait"]:
                golden_boost += 0.40 * (p["confidence"] / 100)

        danger = min(0.95, base_danger + danger_boost)
        safe = min(0.90, base_medium + safe_boost)
        golden = min(0.95, golden_boost)

        total = danger + safe + golden + 0.05
        return {
            "danger": round(danger / total, 3),
            "safe": round(safe / total, 3),
            "medium": round(base_high / total, 3),
            "golden": round(golden / total, 3),
        }

    # ──────────────────────────────────────────
    # 3. التوصية النهائية
    # ──────────────────────────────────────────
    def get_recommendation(self) -> dict:
        patterns = self.detect_patterns()
        probs = self.calculate_probabilities(patterns)

        if not patterns:
            return {
                "status": "neutral",
                "main_action": "انتظر",
                "icon": "⏳",
                "css_class": "status-caution",
                "title": "لا يوجد نمط واضح",
                "description": "الخوارزمية في حالة عشوائية. أضف المزيد من الدورات.",
                "patterns": [],
                "probs": probs,
                "bet_targets": [],
                "golden_wait_mode": False,
                "avoid_rounds": 0,
                "predicted_range": None,
            }

        # الأولوية القصوى للاستراتيجية الذهبية
        priority_order = {
            "golden_bet": 0,
            "danger": 1,
            "golden_wait": 2,
            "avoid": 3,
            "recover": 4,
            "bet_range": 5,
            "neutral": 6
        }
        sorted_patterns = sorted(patterns, key=lambda p: priority_order.get(p["action"], 7))
        top = sorted_patterns[0]

        status_map = {
            "golden_bet": ("safe", "🌟 دخول ذهبي", "🌟", "status-golden", "شروط الاستراتيجية اكتملت — ادخل!"),
            "golden_wait": ("caution", "🎯 وضع القناص", "🎯", "status-recover", "ترقب ظهور رقم ذهبي"),
            "danger": ("danger", "🚫 لا تراهن", "⛔", "status-danger", "خطر عالٍ — فخ أو انفجار مبكر"),
            "avoid": ("caution", "⏭️ تجنب", "⚠️", "status-caution", "تجنب هذه الدورات"),
            "recover": ("recover", "💜 استرداد", "💜", "status-recover", "وضع استرداد"),
            "bet_range": ("safe", "✅ فرصة عادية", "🚀", "status-safe", "فرصة للرهان"),
        }
        
        st_key, action, icon, css, title_sfx = status_map.get(
            top["action"], ("neutral", "⏳ انتظر", "⏳", "status-caution", "انتظر إشارة أوضح")
        )

        golden_wait_mode = top["action"] == "golden_wait"
        bet_targets = []

        if top["action"] == "golden_bet":
            bet_targets = [3.00, 5.00] # الأهداف الصارمة للاستراتيجية
        elif top["action"] == "bet_range" and top.get("predicted_range"):
            low, high = top["predicted_range"]
            safe_exit = max(round(low * 0.88, 2), 1.05)
            bet_targets = [safe_exit, round(low * 0.92, 2)]

        return {
            "status": st_key,
            "main_action": action,
            "icon": icon,
            "css_class": css,
            "title": f"{icon} {title_sfx}",
            "description": top["reason"],
            "patterns": sorted_patterns,
            "probs": probs,
            "bet_targets": bet_targets,
            "golden_wait_mode": golden_wait_mode,
            "avoid_rounds": top.get("rounds_to_avoid", 0),
            "predicted_range": top.get("predicted_range"),
            "top_confidence": top["confidence"],
        }


# ══════════════════════════════════════════════════════
# دوال الرسم البياني
# ══════════════════════════════════════════════════════
def render_history_chart(history: list):
    if len(history) < 2:
        return

    x = list(range(1, len(history) + 1))
    colors = []
    for v in history:
        if v >= 5.0:
            colors.append("#FFD700")
        elif v >= 2.0:
            colors.append("#00ff88")
        else:
            colors.append("#ff4444")

    fig = go.Figure()

    fig.add_hrect(y0=0, y1=1.80, fillcolor="rgba(255,50,50,0.05)", line_width=0,
                  annotation_text="منطقة الخسارة القوية", annotation_position="left")
    fig.add_hrect(y0=1.80, y1=3.0, fillcolor="rgba(0,255,136,0.03)", line_width=0)
    fig.add_hrect(y0=3.0, y1=max(max(history)*1.1, 10), fillcolor="rgba(255,215,0,0.05)", line_width=0,
                  annotation_text="أهداف الاستراتيجية", annotation_position="left")

    fig.add_trace(go.Scatter(
        x=x, y=history, mode="lines+markers+text",
        line=dict(color="rgba(255,215,0,0.6)", width=2, shape="spline"),
        marker=dict(color=colors, size=12, line=dict(color="rgba(255,255,255,0.3)", width=1)),
        text=[f"x{v:.2f}" for v in history],
        textposition="top center",
        textfont=dict(color="white", size=10, family="Orbitron"),
    ))

    fig.add_hline(y=1.80, line_dash="dash", line_color="rgba(255,50,50,0.4)", line_width=1)
    fig.add_hline(y=3.00, line_dash="dash", line_color="rgba(0,255,136,0.4)", line_width=1)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Tajawal"),
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(showgrid=False, title="الدورة", tickfont=dict(color="rgba(255,255,255,0.4)")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="المضاعف",
                   tickprefix="x", tickfont=dict(color="rgba(255,255,255,0.4)")),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, key=f"hist_{len(history)}")


def render_probability_chart(probs: dict):
    labels = ["خطر (< x2)", "عادي (x2-x5)", "عالي (> x5)", "ذهبي"]
    values = [probs["danger"]*100, probs["safe"]*100, probs["medium"]*100, probs["golden"]*100]
    colors_pie = ["#ff4444", "#00ff88", "#a855f7", "#FFD700"]

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.65,
        marker=dict(colors=colors_pie, line=dict(color="rgba(0,0,0,0.5)", width=2)),
        textfont=dict(color="white", size=12, family="Tajawal"),
        textinfo="label+percent",
    ))

    fig.add_annotation(
        text=f"<b>{max(values):.0f}%</b><br>أعلى<br>احتمال",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="white", family="Tajawal"),
        align="center"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="Tajawal"),
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.2,
            font=dict(size=11, color="rgba(255,255,255,0.6)"),
            bgcolor="rgba(0,0,0,0)"
        ),
    )
    st.plotly_chart(fig, use_container_width=True, key=f"prob_{sum(v for v in probs.values())}")


def render_confidence_bar(confidence: int, label: str, key: str):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        title={"text": label, "font": {"size": 13, "color": "rgba(255,255,255,0.7)", "family": "Tajawal"}},
        number={"suffix": "%", "font": {"size": 30, "color": "#FFD700", "family": "Orbitron"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "rgba(255,255,255,0.2)"},
            "bar": {"color": "#FFD700", "thickness": 0.35},
            "bgcolor": "rgba(0,0,0,0.2)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 50], "color": "rgba(255,50,50,0.1)"},
                {"range": [50, 80], "color": "rgba(255,215,0,0.1)"},
                {"range": [80, 100], "color": "rgba(0,255,136,0.1)"},
            ],
        }
    ))
    fig.update_layout(
        height=200, margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True, key=key)


# ══════════════════════════════════════════════════════
# إدارة الحالة
# ══════════════════════════════════════════════════════
if "crash_history" not in st.session_state:
    st.session_state.crash_history = []
if "balance" not in st.session_state:
    st.session_state.balance = 1000.0
if "session_log" not in st.session_state:
    st.session_state.session_log = []

# ══════════════════════════════════════════════════════
# الواجهة الرئيسية
# ══════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding: 20px 0 10px;">
    <div style="font-family:'Orbitron',monospace; font-size:42px; font-weight:900; background: linear-gradient(90deg, #FFD700, #ff8c00, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-size: 200%; animation: gradientShift 3s linear infinite;">
        🚀 CRASH PRO - GOLDEN STRATEGY
    </div>
    <div style="color:rgba(255,255,255,0.4); font-size:14px; letter-spacing:3px; margin-top:5px;">
        نظام التطبيق الصارم للاستراتيجية
    </div>
</div>
<style>
    @keyframes gradientShift { 0%{background-position:0%} 100%{background-position:200%} }
</style>
""", unsafe_allow_html=True)

# ── الشريط الجانبي ──────────────────────────────────
with st.sidebar:
    st.markdown('<div style="text-align:center; color:#FFD700; font-size:20px; font-weight:900; margin-bottom:15px;">⚙️ لوحة التحكم الذهبية</div>', unsafe_allow_html=True)

    st.markdown("**💰 الرصيد المخصص للعب**")
    st.session_state.balance = st.number_input(
        "رصيدك الحالي", min_value=10.0, max_value=1_000_000.0,
        value=st.session_state.balance, step=50.0, label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**🔧 أدوات**")
    if st.button("🗑️ مسح السجل", use_container_width=True):
        st.session_state.crash_history = []
        st.session_state.session_log = []
        st.rerun()

    if st.button("🎲 محاكاة سريعة (تجريبي)", use_container_width=True):
        sim = [1.50, 1.15, 1.22, 1.54] # محاكاة لظهور الإشارة الذهبية
        st.session_state.crash_history.extend(sim)
        st.rerun()

    st.markdown("---")
    h = st.session_state.crash_history
    if h:
        losses = sum(1 for v in h if v < 1.80)
        wins = len(h) - losses
        avg = np.mean(h)
        st.markdown(f"""
        <div class="stat-box" style="margin:5px 0;">
            <div class="stat-number">{len(h)}</div>
            <div class="stat-label">إجمالي الدورات المسجلة</div>
        </div>
        <div class="stat-box" style="margin:5px 0;">
            <div class="stat-number" style="color:#ff4444;">{losses}</div>
            <div class="stat-label">دورات تحت 1.80</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# منطقة الإدخال
# ══════════════════════════════════════════════════════
st.markdown('<div class="crash-card">', unsafe_allow_html=True)
st.markdown("### 📥 أدخل نتيجة الدورة الأخيرة بدقة")

col_in1, col_in2, col_in3 = st.columns([2, 1, 1])
with col_in1:
    new_value = st.number_input(
        "مضاعف الانفجار (مثال: 1.45 أو 7.20)",
        min_value=1.00, max_value=1000.0, value=1.50, step=0.01,
        format="%.2f", label_visibility="collapsed"
    )
with col_in2:
    if st.button("➕ أضف الدورة", use_container_width=True):
        st.session_state.crash_history.append(round(new_value, 2))
        st.session_state.session_log.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "value": round(new_value, 2),
            "index": len(st.session_state.crash_history),
        })
        st.rerun()
with col_in3:
    if st.button("↩️ تراجع", use_container_width=True):
        if st.session_state.crash_history:
            st.session_state.crash_history.pop()
        if st.session_state.session_log:
            st.session_state.session_log.pop()
        st.rerun()

h = st.session_state.crash_history
if h:
    badges_html = '<div class="history-bar">'
    for i, v in enumerate(h[-20:]):
        if v in GOLDEN_NUMBERS:
            cls = "round-badge-medium"
            style = "border-color:#FFD700; color:#FFD700;"
        elif v >= 2.0:
            cls = "round-badge-win"
            style = ""
        else:
            cls = "round-badge-loss"
            style = ""
        idx = max(0, len(h) - 20) + i + 1
        badges_html += f'<span class="{cls}" style="{style}" title="الدورة {idx}">x{v:.2f}</span>'
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# التحليل والتوصية
# ══════════════════════════════════════════════════════
if len(h) < 3:
    st.markdown(f"""
    <div class="status-caution" style="text-align:center; padding:30px;">
        <div style="font-size:50px;">⏳</div>
        <div style="font-size:22px; font-weight:700; margin:10px 0;">أضف المزيد من الدورات</div>
        <div style="color:rgba(255,255,255,0.5);">يجب إدخال 3 دورات على الأقل لبدء ترقب الاستراتيجية</div>
    </div>
    """, unsafe_allow_html=True)
else:
    analyzer = CrashAnalyzer(h)
    rec = analyzer.get_recommendation()

    col_main, col_prob = st.columns([3, 2])

    with col_main:
        st.markdown(f'<div class="{rec["css_class"]}">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:50px; margin-bottom:10px;">{rec['icon']}</div>
        <div style="font-size:28px; font-weight:900; margin-bottom:12px;">{rec['title']}</div>
        <div style="font-size:16px; color:rgba(255,255,255,0.9); line-height:1.7;">{rec['description']}</div>
        """, unsafe_allow_html=True)

        if rec.get("predicted_range"):
            low, high = rec["predicted_range"]
            st.markdown(f"""
            <div style="margin-top:15px; padding:12px; background:rgba(0,0,0,0.3); border-radius:10px;">
                <span style="color:rgba(255,255,255,0.5); font-size:13px;">الهدف المقترح:</span><br>
                <span style="font-family:'Orbitron',monospace; font-size:24px; color:#FFD700; font-weight:900;">
                    x{low:.2f} — x{high:.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)

        if rec.get("avoid_rounds", 0) > 0:
            st.markdown(f"""
            <div style="margin-top:12px; background:rgba(255,50,50,0.15); border-radius:8px; padding:10px 15px;">
                ⏭️ <b>توقف تماماً وتجنب {rec['avoid_rounds']} دورة قادمة</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if rec["patterns"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**🔍 تفصيل الأنماط الحالية:**")
            for p in rec["patterns"]:
                action_tag = {
                    "danger": '<span class="scenario-tag tag-avoid">⛔ فخ/خطر</span>',
                    "avoid": '<span class="scenario-tag tag-wait">⚠️ تجنب</span>',
                    "golden_bet": '<span class="scenario-tag tag-golden">🌟 إشارة ذهبية</span>',
                    "golden_wait": '<span class="scenario-tag tag-wait">🎯 قناص</span>',
                    "bet_range": '<span class="scenario-tag tag-bet">✅ ثانوي</span>',
                }.get(p["action"], "")
                st.markdown(f"""
                <div class="bet-target">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            {action_tag}
                            <span style="font-weight:700; font-size:16px; margin-right:8px;">{p['icon']} {p['name']}</span>
                        </div>
                        <div style="text-align:left;">
                            <div style="color:#FFD700; font-size:13px;">تأكيد: {p['confidence']}%</div>
                            <div class="prob-bar"><div class="prob-fill" style="width:{p['confidence']}%; background:linear-gradient(90deg, #FFD700, #ff8c00);"></div></div>
                        </div>
                    </div>
                    <div style="color:rgba(255,255,255,0.7); font-size:14px; margin-top:8px; line-height:1.6;">
                        {p['reason']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with col_prob:
        st.markdown("**📊 قراءة الخوارزمية:**")
        render_probability_chart(rec["probs"])
        render_confidence_bar(
            rec.get("top_confidence", 50),
            "قوة الإشارة الحالية",
            key=f"conf_{len(h)}"
        )

    # ── مناطق التنفيذ ────────────────────────────────────
    if rec["golden_wait_mode"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="crash-card" style="border-color:#FFD700;">
            <div style="text-align:center; font-size:24px; font-weight:900; color:#FFD700; margin-bottom:20px;">
                🎯 وضع القناص — راقب هذه الأرقام فقط!
            </div>
            <div class="warning-box" style="border-color:#FFD700; background:rgba(255,215,0,0.05); color:#FFD700;">
                ⚠️ <b>تنبيه صارم:</b> إياك والرهان الآن. راقب الشاشة فقط. إذا ظهر أحد الأرقام التالية كـ "نتيجة نهائية للدورة"، قم بإدخاله هنا لتفعيل إشارة الدخول.
            </div>
        """, unsafe_allow_html=True)
        
        cols_rec = st.columns(len(GOLDEN_NUMBERS))
        for i, target in enumerate(GOLDEN_NUMBERS):
            with cols_rec[i]:
                st.markdown(f"""
                <div class="recover-item" style="justify-content:center; background:rgba(255,215,0,0.1); border:1px solid #FFD700;">
                    <div class="multiplier-tag" style="color:#FFD700; font-size:22px;">x{target}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif rec["bet_targets"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="crash-card">
            <div style="text-align:center; font-size:22px; font-weight:900; color:#00ff88; margin-bottom:20px;">
                🎯 أهداف جني الأرباح للاستراتيجية
            </div>
        """, unsafe_allow_html=True)
        
        cols_bet = st.columns(len(rec["bet_targets"]))
        for i, target in enumerate(rec["bet_targets"]):
            # إدارة رأس مال صارمة (1% للهدف الأول، 0.5% للهدف الثاني)
            stake_pct = 0.01 if i == 0 else 0.005
            suggested_stake = max(1.0, st.session_state.balance * stake_pct)
            potential = round(suggested_stake * target, 2)
            profit = round(potential - suggested_stake, 2)
            
            with cols_bet[i]:
                label = "✅ الهدف الآمن (أساسي)" if i == 0 else "🔥 الهدف المتقدم (نصف الكمية)"
                color = "#00ff88" if i == 0 else "#FFD700"
                
                st.markdown(f"""
                <div style="background:rgba(0,255,136,0.05); border:1px solid {color}; border-radius:14px; padding:20px; text-align:center;">
                    <div style="font-size:14px; font-weight:700; color:{color}; margin-bottom:8px;">{label}</div>
                    <div class="multiplier-tag" style="font-size:32px; color:{color};">x{target:.2f}</div>
                    <div style="margin-top:12px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
                        <span style="color:rgba(255,255,255,0.5); font-size:12px;">مبلغ الدخول المقترح (إدارة مخاطر):</span><br>
                        <span style="color:white; font-size:22px; font-weight:900;">{suggested_stake:.1f}</span>
                        <span style="color:rgba(255,255,255,0.4); font-size:12px;">$</span>
                    </div>
                    <div style="color:{color}; font-size:15px; margin-top:6px; font-weight:700;">
                        الربح الصافي: +{profit:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="crash-card">', unsafe_allow_html=True)
    st.markdown("**📈 مسار الدورات والمراقبة**")
    render_history_chart(h)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
    <b>⚠️ قانون الاستراتيجية الذهبية:</b> الالتزام الكامل بالصبر. لا تدخل أبداً خارج الإشارات المحددة. حافظ على رهان صغير (1% إلى 2% كحد أقصى) لحماية رصيدك من تقلبات الخوارزمية.
</div>
""", unsafe_allow_html=True)
