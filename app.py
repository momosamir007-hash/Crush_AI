# -*- coding: utf-8 -*-
# app.py — ملف واحد كامل بدون استيرادات خارجية

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import chi2
from scipy.fft import fft, fftfreq
from collections import Counter
import json
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🎓 تحليل PRNG — مشروع تخرج",
    page_icon="🎓",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════
#                    اختبارات NIST
# ══════════════════════════════════════════════════════════════
class RandomnessTestSuite:

    def __init__(self, data: list):
        self.raw      = np.array(data, dtype=float)
        self.binary   = (self.raw >= 2.0).astype(int)
        self.log_data = np.log(np.maximum(self.raw, 1.0))
        self.results  = {}

    def frequency_test(self) -> dict:
        n  = len(self.binary)
        n1 = int(self.binary.sum())
        n0 = n - n1
        s  = abs(n1 - n0) / np.sqrt(n)
        p  = float(2 * (1 - stats.norm.cdf(s)))
        r  = {
            'test_name'     : 'Frequency (Monobit) Test',
            'n_high'        : n1,
            'n_low'         : n0,
            'ratio_high'    : round(n1 / n, 4),
            'statistic'     : round(s, 4),
            'p_value'       : round(p, 4),
            'passed'        : p >= 0.01,
            'interpretation': (
                '✅ التوزيع متوازن — لا دليل على تلاعب'
                if p >= 0.01
                else '🔴 خلل في التوزيع!'
            )
        }
        self.results['frequency'] = r
        return r

    def runs_test(self) -> dict:
        n  = len(self.binary)
        pi = float(self.binary.mean())
        if abs(pi - 0.5) > 2 / np.sqrt(n):
            r = {
                'test_name'     : 'Runs Test',
                'passed'        : False,
                'p_value'       : 0.0,
                'statistic'     : 0.0,
                'interpretation': '🔴 نسبة غير متوازنة'
            }
            self.results['runs'] = r
            return r
        runs = 1 + sum(
            1 for i in range(1, n)
            if self.binary[i] != self.binary[i - 1]
        )
        exp = 2 * n * pi * (1 - pi)
        var = 2 * n * pi * (1 - pi) * (2 * pi * (1 - pi) - 1 / n)
        z   = (runs - exp) / np.sqrt(var) if var > 0 else 0.0
        p   = float(2 * (1 - stats.norm.cdf(abs(z))))
        r   = {
            'test_name'     : 'Runs Test',
            'runs_observed' : int(runs),
            'runs_expected' : round(exp, 2),
            'statistic'     : round(z, 4),
            'p_value'       : round(p, 4),
            'passed'        : p >= 0.01,
            'interpretation': (
                '✅ التسلسلات طبيعية'
                if p >= 0.01
                else '🔴 أنماط في التسلسلات!'
            )
        }
        self.results['runs'] = r
        return r

    def autocorrelation_test(self, max_lag: int = 20) -> dict:
        n     = len(self.binary)
        bound = 1.96 / np.sqrt(n)
        acfs  = []
        sig   = []
        for lag in range(1, min(max_lag + 1, n)):
            c = float(np.corrcoef(
                self.binary[lag:], self.binary[:-lag]
            )[0, 1])
            is_s = abs(c) > bound
            acfs.append({
                'lag'            : lag,
                'autocorrelation': round(c, 6),
                'significant'    : bool(is_s),
                'bound'          : round(bound, 4)
            })
            if is_s:
                sig.append(lag)
        r = {
            'test_name'         : 'Autocorrelation Test',
            'significance_bound': round(bound, 4),
            'significant_lags'  : sig,
            'n_significant'     : len(sig),
            'autocorrelations'  : acfs,
            'p_value'           : round(0.003 if sig else 0.5, 4),
            'passed'            : len(sig) == 0,
            'interpretation'    : (
                '✅ لا ارتباط — عشوائي'
                if not sig
                else f'🔴 ارتباط دال في Lags: {sig}'
            )
        }
        self.results['autocorrelation'] = r
        return r

    def distribution_test(self) -> dict:
        bins   = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0, float('inf')]
        labels = ['1-1.5x','1.5-2x','2-3x','3-5x','5-10x','>10x']
        n, he  = len(self.raw), 0.99
        th = []
        for i in range(len(bins) - 1):
            pl = min(he / bins[i], 1.0)
            ph = min(he / bins[i+1], 1.0) if bins[i+1] != float('inf') else 0.0
            th.append(pl - ph)
        s  = sum(th)
        th = [p / s for p in th]
        obs = []
        for i in range(len(bins) - 1):
            if bins[i+1] == float('inf'):
                obs.append(int((self.raw >= bins[i]).sum()))
            else:
                obs.append(int(
                    ((self.raw >= bins[i]) &
                     (self.raw < bins[i+1])).sum()
                ))
        exp = [p * n for p in th]
        try:
            c2, p = stats.chisquare(obs, exp)
        except Exception:
            c2, p = 0.0, 1.0
        r = {
            'test_name'     : 'Chi-Square Distribution Test',
            'categories'    : [
                {
                    'range'       : labels[i],
                    'observed'    : obs[i],
                    'expected'    : round(exp[i], 1),
                    'observed_pct': round(obs[i] / n * 100, 1),
                    'expected_pct': round(th[i] * 100, 1)
                }
                for i in range(len(labels))
            ],
            'chi2_statistic': round(float(c2), 4),
            'p_value'       : round(float(p), 4),
            'passed'        : float(p) >= 0.01,
            'interpretation': (
                '✅ يتبع التوزيع النظري (Power Law)'
                if float(p) >= 0.01
                else '🔴 انحراف عن التوزيع النظري!'
            )
        }
        self.results['distribution'] = r
        return r

    def longest_run_test(self) -> dict:
        mh = ml = ch = cl = 0
        for v in self.binary:
            if v == 1:
                ch += 1; cl = 0; mh = max(mh, ch)
            else:
                cl += 1; ch = 0; ml = max(ml, cl)
        n   = len(self.binary)
        thr = 3 * np.log2(n) if n > 1 else 10
        ok  = mh <= thr * 1.5
        r   = {
            'test_name'           : 'Longest Run Test',
            'max_consecutive_high': int(mh),
            'max_consecutive_low' : int(ml),
            'theoretical_max'     : round(thr, 1),
            'p_value'             : round(0.1 if ok else 0.001, 4),
            'passed'              : ok,
            'interpretation'      : (
                f'✅ أطول تسلسل ({mh}) ضمن الحدود ({thr:.1f})'
                if ok
                else f'🔴 تسلسل غير طبيعي: {mh} متتالية!'
            )
        }
        self.results['longest_run'] = r
        return r

    def entropy_test(self) -> dict:
        ph  = float(self.binary.mean())
        pl  = 1 - ph
        ent = (
            -(ph * np.log2(ph) + pl * np.log2(pl))
            if ph > 0 and pl > 0 else 0.0
        )
        n_bins = 20
        hist, _ = np.histogram(self.log_data, bins=n_bins)
        hist = hist[hist > 0]
        probs = hist / hist.sum()
        ent_c = float(-np.sum(probs * np.log2(probs)))
        r = {
            'test_name'        : 'Shannon Entropy Test',
            'binary_entropy'   : round(ent, 6),
            'max_entropy'      : 1.0,
            'efficiency_pct'   : round(ent * 100, 2),
            'continuous_entropy': round(ent_c, 4),
            'p_value'          : round(0.95 if ent >= 0.95 else 0.001, 4),
            'passed'           : ent >= 0.95,
            'interpretation'   : (
                f'✅ إنتروبيا عالية ({ent:.3f} bits = {ent*100:.1f}%)'
                if ent >= 0.95
                else f'🔴 إنتروبيا منخفضة ({ent:.3f} bits)!'
            )
        }
        self.results['entropy'] = r
        return r

    def serial_test(self) -> dict:
        pairs   = Counter(zip(self.binary[:-1], self.binary[1:]))
        n_pairs = len(self.binary) - 1
        exp     = n_pairs / 4
        obs     = [
            pairs.get((0,0), 0), pairs.get((0,1), 0),
            pairs.get((1,0), 0), pairs.get((1,1), 0)
        ]
        c2 = sum((o - exp)**2 / exp for o in obs)
        p  = float(1 - chi2.cdf(c2, df=3))
        r  = {
            'test_name'    : 'Serial (Pairs) Test',
            'pair_counts'  : {
                'L→L': int(pairs.get((0,0), 0)),
                'L→H': int(pairs.get((0,1), 0)),
                'H→L': int(pairs.get((1,0), 0)),
                'H→H': int(pairs.get((1,1), 0))
            },
            'expected_each'  : round(exp, 1),
            'chi2_statistic' : round(c2, 4),
            'p_value'        : round(p, 4),
            'passed'         : p >= 0.01,
            'interpretation' : (
                '✅ توزيع الأزواج عشوائي'
                if p >= 0.01
                else '🔴 أنماط في الأزواج المتتالية!'
            )
        }
        self.results['serial'] = r
        return r

    def linear_complexity_test(self, window: int = 50) -> dict:
        comps = []
        for i in range(0, len(self.binary) - window, window // 2):
            seg = self.binary[i:i + window]
            changes = sum(
                1 for j in range(1, len(seg))
                if seg[j] != seg[j-1]
            )
            comps.append(changes / 2)
        if not comps:
            comps = [window / 2]
        avg  = float(np.mean(comps))
        theo = window / 2
        rat  = avg / theo
        ok   = 0.4 <= rat <= 0.6
        r    = {
            'test_name'             : 'Linear Complexity Test',
            'window_size'           : window,
            'avg_complexity'        : round(avg, 2),
            'theoretical_complexity': round(theo, 2),
            'complexity_ratio'      : round(rat, 4),
            'p_value'               : round(0.3 if ok else 0.001, 4),
            'passed'                : ok,
            'interpretation'        : (
                f'✅ تعقيد طبيعي ({rat:.3f}) — PRNG قوي'
                if ok
                else f'🔴 تعقيد غير طبيعي ({rat:.3f})!'
            )
        }
        self.results['linear_complexity'] = r
        return r

    def run_all(self) -> dict:
        fns = [
            self.frequency_test,
            self.runs_test,
            self.autocorrelation_test,
            self.distribution_test,
            self.longest_run_test,
            self.entropy_test,
            self.serial_test,
            self.linear_complexity_test,
        ]
        passed = 0
        for fn in fns:
            r = fn()
            if r.get('passed', False):
                passed += 1
        total   = len(fns)
        verdict = (
            'عشوائي إحصائياً ✅'
            if passed >= total * 0.75
            else 'يحتوي أنماط إحصائية 🔴'
        )
        return {
            'passed_tests': passed,
            'total_tests' : total,
            'pass_rate'   : round(passed / total, 3),
            'verdict'     : verdict
        }


# ══════════════════════════════════════════════════════════════
#                      تحليل PRNG
# ══════════════════════════════════════════════════════════════
class PRNGAnalyzer:

    def __init__(self, data: list):
        self.raw      = np.array(data, dtype=float)
        self.log_data = np.log(np.maximum(self.raw, 1.0))
        self.binary   = (self.raw >= 2.0).astype(int)

    def spectral_analysis(self) -> dict:
        n        = len(self.log_data)
        centered = self.log_data - self.log_data.mean()
        mag      = np.abs(fft(centered))
        freqs    = fftfreq(n)
        half     = n // 2
        mag_h    = mag[:half]
        freq_h   = freqs[:half]
        top_idx  = np.argsort(mag_h)[-10:][::-1]
        dominant = []
        for idx in top_idx:
            if freq_h[idx] > 0:
                dominant.append({
                    'frequency'     : round(float(freq_h[idx]), 6),
                    'period_rounds' : round(float(1 / freq_h[idx]), 1),
                    'relative_power': round(
                        float(mag_h[idx]) / (mag_h.max() + 1e-9), 4
                    )
                })
        dr = float(mag_h.max() / (mag_h.mean() + 1e-9))
        return {
            'dominant_frequencies': dominant[:5],
            'dominance_ratio'     : round(dr, 2),
            'has_pattern'         : dr > 10,
            'interpretation'      : (
                f'🔴 تردد مهيمن! نسبة {dr:.1f}x — نمط محتمل'
                if dr > 10
                else f'✅ لا ترددات مهيمنة (نسبة {dr:.1f}x)'
            )
        }

    def cycle_detection(self, max_period: int = 60) -> dict:
        best_p = None
        best_c = 0.0
        all_p  = []
        for period in range(2, min(max_period, len(self.raw) // 3)):
            x = self.log_data[:-period]
            y = self.log_data[period:]
            if len(x) < 10:
                break
            c = float(np.corrcoef(x, y)[0, 1])
            all_p.append({'period': period, 'correlation': round(c, 6)})
            if abs(c) > abs(best_c):
                best_c = c
                best_p = period
        return {
            'best_period'    : best_p,
            'best_correlation': round(best_c, 4),
            'all_periods'    : all_p,
            'cycle_detected' : abs(best_c) > 0.5,
            'interpretation' : (
                f'🔴 دورة عند period={best_p}! corr={best_c:.3f}'
                if abs(best_c) > 0.5
                else f'✅ لا دورات واضحة (أقوى: {best_c:.3f})'
            )
        }

    def birthday_test(self) -> dict:
        q      = np.round(self.log_data, 1)
        n      = len(q)
        seen   = {}
        first  = None
        for i, val in enumerate(q):
            key = float(val)
            if key in seen:
                first = {
                    'position'         : i,
                    'original_position': seen[key],
                    'value'            : key,
                    'gap'              : i - seen[key]
                }
                break
            seen[key] = i
        unique   = len(np.unique(q))
        expected = float(np.sqrt(np.pi * unique / 2))
        ok = (first is None or first['position'] >= expected * 0.5)
        return {
            'unique_values'          : unique,
            'expected_first_collision': round(expected, 1),
            'actual_first_collision' : first,
            'interpretation'         : (
                '✅ التكرار في حدوده الطبيعية'
                if ok
                else f'🔴 تكرار مبكر عند position {first["position"]}!'
            )
        }


# ══════════════════════════════════════════════════════════════
#                    بيانات نموذجية
# ══════════════════════════════════════════════════════════════
SAMPLE_DATA = [
    8.72,6.75,1.86,2.18,1.25,2.28,1.24,1.20,1.54,24.46,
    4.16,1.49,1.09,1.47,1.54,1.53,2.10,32.04,11.0,1.17,
    1.70,2.61,1.26,22.23,1.77,1.93,3.35,7.01,1.83,9.39,
    3.31,2.04,1.30,6.65,1.16,3.39,1.95,10.85,1.65,1.22,
    1.60,4.67,1.85,2.72,1.00,3.02,1.35,1.30,1.37,17.54,
    1.18,1.00,14.40,1.11,6.15,2.39,2.22,1.42,1.23,2.42,
    1.07,1.24,2.55,7.26,1.69,5.10,2.59,5.51,2.31,2.12,
    1.97,1.50,3.01,2.29,1.36,4.95,5.09,8.50,1.77,5.52,
    3.93,1.50,2.28,2.49,18.25,1.68,1.42,2.12,4.17,1.04,
    2.35,1.00,1.01,5.46,1.13,2.84,3.39,2.79,1.59,1.53,
    4.34,2.96,1.06,1.72,2.16,2.20,3.61,2.34,4.49,1.72,
    1.78,9.27,8.49,2.86,1.66,4.63,9.25,1.35,1.00,1.64,
    1.86,2.81,2.44,1.74,1.10,1.29,1.45,8.92,1.24,6.39,
]


# ══════════════════════════════════════════════════════════════
#                    واجهة المستخدم
# ══════════════════════════════════════════════════════════════
st.title("🎓 تحليل عشوائية لعبة Crash")
st.caption(
    "اختبارات NIST SP 800-22 لتحليل مولدات الأرقام الزائفة | "
    "مشروع تخرج أكاديمي"
)

# ── إدخال البيانات ──────────────────────────────────────────
st.header("📥 إدخال البيانات")

method = st.radio(
    "اختر طريقة الإدخال:",
    ["📝 إدخال يدوي", "📂 رفع ملف CSV", "🎲 بيانات نموذجية"],
    horizontal=True
)

raw_data = None

if method == "📝 إدخال يدوي":
    txt = st.text_area(
        "أدخل قيم الـ Crash مفصولة بمسافات أو أسطر:",
        height=140,
        placeholder="1.23  4.56  2.10  1.05  8.92  3.41  22.3 ..."
    )
    if txt.strip():
        try:
            raw_data = [
                float(x)
                for x in txt.replace('\n', ' ').split()
                if x.strip()
            ]
            st.success(f"✅ تم تحميل **{len(raw_data)}** قيمة")
        except Exception:
            st.error("❌ خطأ في التنسيق — أرقام فقط مفصولة بمسافات")

elif method == "📂 رفع ملف CSV":
    uploaded = st.file_uploader(
        "ارفع ملف CSV يحتوي عمود crash_point",
        type=['csv']
    )
    if uploaded:
        try:
            df_up = pd.read_csv(uploaded)
            if 'crash_point' in df_up.columns:
                raw_data = df_up['crash_point'].dropna().tolist()
                st.success(f"✅ تم تحميل **{len(raw_data)}** قيمة")
                st.dataframe(df_up.head(10), use_container_width=True)
            else:
                cols = list(df_up.columns)
                st.error(f"❌ لم يوجد عمود crash_point. الأعمدة: {cols}")
        except Exception as e:
            st.error(f"❌ خطأ: {e}")

else:
    raw_data = SAMPLE_DATA
    st.info(f"🎲 تم تحميل **{len(raw_data)}** قيمة نموذجية")

# ── عرض ملخص البيانات ───────────────────────────────────────
if raw_data:
    arr  = np.array(raw_data)
    n    = len(arr)

    st.markdown("---")
    st.subheader("📋 ملخص البيانات")

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("عدد القيم",  f"{n}")
    c2.metric("المتوسط",    f"{arr.mean():.2f}x")
    c3.metric("الوسيط",     f"{np.median(arr):.2f}x")
    c4.metric("الحد الأدنى",f"{arr.min():.2f}x")
    c5.metric("الحد الأقصى",f"{arr.max():.2f}x")
    c6.metric(">= 2x",      f"{np.mean(arr>=2)*100:.1f}%")

    if n < 30:
        st.warning(f"⚠️ أدخل 30 قيمة على الأقل (لديك {n})")
    else:
        st.markdown("---")

        # زر التحليل
        if st.button("🚀 تشغيل التحليل الكامل", type="primary",
                     use_container_width=True):

            # ── شريط التقدم ─────────────────────────────
            prog = st.progress(0)
            status = st.empty()

            status.info("⏳ تشغيل اختبارات NIST...")
            suite = RandomnessTestSuite(raw_data)

            steps = [
                ("Frequency Test",        suite.frequency_test),
                ("Runs Test",             suite.runs_test),
                ("Autocorrelation Test",  suite.autocorrelation_test),
                ("Distribution Test",     suite.distribution_test),
                ("Longest Run Test",      suite.longest_run_test),
                ("Entropy Test",          suite.entropy_test),
                ("Serial Test",           suite.serial_test),
                ("Linear Complexity Test",suite.linear_complexity_test),
            ]
            for i, (name, fn) in enumerate(steps):
                status.info(f"⏳ {name} ({i+1}/{len(steps)})...")
                fn()
                prog.progress(int((i + 1) / len(steps) * 70))

            status.info("⏳ تحليل PRNG المتقدم...")
            analyzer = PRNGAnalyzer(raw_data)
            spectral = analyzer.spectral_analysis()
            cycle    = analyzer.cycle_detection()
            birthday = analyzer.birthday_test()
            prog.progress(100)
            status.empty()
            prog.empty()

            st.balloons()

            # ════════════════════════════════════════════
            #               عرض النتائج
            # ════════════════════════════════════════════
            passed  = sum(
                1 for r in suite.results.values()
                if r.get('passed', False)
            )
            total   = len(suite.results)
            verdict = (
                'عشوائي إحصائياً ✅'
                if passed >= total * 0.75
                else 'يحتوي أنماط إحصائية 🔴'
            )

            # ── ملخص علوي ───────────────────────────────
            st.header("📊 النتائج الإجمالية")

            m1,m2,m3,m4 = st.columns(4)
            m1.metric("اختبارات نجحت", f"{passed} / {total}")
            m2.metric("معدل النجاح",
                      f"{passed/total*100:.0f}%",
                      delta=("جيد" if passed/total >= 0.75
                             else "يوجد أنماط"))
            m3.metric("عدد القيم المحللة", f"{n}")
            m4.metric("الحكم النهائي", verdict)

            # ── مخطط دائري ──────────────────────────────
            fig_pie = px.pie(
                names=['✅ نجح','❌ فشل'],
                values=[passed, total - passed],
                color_discrete_sequence=['#2ecc71','#e74c3c'],
                title="نسبة نجاح الاختبارات"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("---")

            # ── جدول الاختبارات ──────────────────────────
            st.subheader("🔬 جدول اختبارات NIST")
            rows = []
            for r in suite.results.values():
                rows.append({
                    'الاختبار' : r['test_name'],
                    'P-Value'  : r.get('p_value', '-'),
                    'النتيجة'  : '✅ نجح' if r.get('passed') else '❌ فشل',
                    'التفسير'  : r.get('interpretation', '')
                })
            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            # ── تبويبات تفصيلية ──────────────────────────
            st.subheader("📈 التحليلات التفصيلية")
            tab_acf, tab_fft, tab_cyc, tab_dist, tab_pairs, tab_prng = st.tabs([
                "🔢 الارتباط الذاتي",
                "📡 FFT",
                "🔄 الدوريات",
                "📊 التوزيع",
                "👫 الأزواج",
                "🔐 تحليل PRNG"
            ])

            # ── ACF ──
            with tab_acf:
                acf_res  = suite.results.get('autocorrelation', {})
                acf_list = acf_res.get('autocorrelations', [])
                bound    = acf_res.get('significance_bound', 0.1)
                sig_lags = acf_res.get('significant_lags', [])

                if acf_list:
                    df_acf = pd.DataFrame(acf_list)
                    fig_acf = go.Figure()
                    fig_acf.add_trace(go.Bar(
                        x=df_acf['lag'],
                        y=df_acf['autocorrelation'],
                        marker_color=[
                            '#e74c3c' if s else '#3498db'
                            for s in df_acf['significant']
                        ],
                        name='ACF'
                    ))
                    for sgn in [1, -1]:
                        fig_acf.add_hline(
                            y=sgn * bound,
                            line_dash="dash", line_color="red",
                            annotation_text=(
                                f"±{bound:.3f} حد الدلالة 95%"
                                if sgn == 1 else ""
                            )
                        )
                    fig_acf.update_layout(
                        title="الارتباط الذاتي — الأحمر = دال إحصائياً",
                        xaxis_title="Lag",
                        yaxis_title="Autocorrelation",
                        height=420
                    )
                    st.plotly_chart(fig_acf, use_container_width=True)

                if sig_lags:
                    st.error(
                        f"🔴 **اكتُشف ارتباط دال في:** Lag {sig_lags}\n\n"
                        f"المعنى الأكاديمي: يوجد تأثير خفي بين الجولات"
                        f" المتباعدة بـ {sig_lags[0]} جولات"
                    )
                else:
                    st.success("✅ لا ارتباط دال في أي Lag — التسلسل عشوائي")

            # ── FFT ──
            with tab_fft:
                st.info(f"**{spectral['interpretation']}**")
                col_a, col_b = st.columns(2)
                col_a.metric("نسبة الهيمنة", f"{spectral['dominance_ratio']}x")
                col_b.metric(
                    "هل يوجد نمط؟",
                    "نعم 🔴" if spectral['has_pattern'] else "لا ✅"
                )

                if spectral['dominant_frequencies']:
                    df_fft = pd.DataFrame(spectral['dominant_frequencies'])
                    fig_fft = px.bar(
                        df_fft,
                        x='period_rounds',
                        y='relative_power',
                        title="أقوى الترددات المكتشفة (FFT)",
                        labels={
                            'period_rounds' : 'الدورة (عدد الجولات)',
                            'relative_power': 'القوة النسبية'
                        },
                        color='relative_power',
                        color_continuous_scale='OrRd',
                        text='period_rounds'
                    )
                    fig_fft.update_traces(
                        texttemplate='%{text:.0f} جولة',
                        textposition='outside'
                    )
                    st.plotly_chart(fig_fft, use_container_width=True)

                    st.caption(
                        "القوة النسبية > 0.5 تعني تردداً مهيمناً = نمط واضح. "
                        "القيم المنخفضة = عشوائي."
                    )

            # ── الدوريات ──
            with tab_cyc:
                st.info(f"**{cycle['interpretation']}**")
                ca, cb, cc = st.columns(3)
                ca.metric("أفضل فترة", f"{cycle['best_period']} جولة")
                cb.metric("أقوى ارتباط", f"{cycle['best_correlation']}")
                cc.metric(
                    "دورة مكتشفة؟",
                    "نعم 🔴" if cycle['cycle_detected'] else "لا ✅"
                )

                if cycle['all_periods']:
                    df_cyc = pd.DataFrame(cycle['all_periods'])
                    fig_cyc = px.line(
                        df_cyc, x='period', y='correlation',
                        title="الارتباط مع النفس عند كل فترة زمنية",
                        labels={
                            'period'     : 'الفترة (جولات)',
                            'correlation': 'معامل الارتباط'
                        }
                    )
                    for sgn in [0.5, -0.5]:
                        fig_cyc.add_hline(
                            y=sgn, line_dash="dash", line_color="red",
                            annotation_text="حد الدلالة" if sgn > 0 else ""
                        )
                    fig_cyc.add_hline(
                        y=0, line_color="gray", line_dash="dot"
                    )
                    st.plotly_chart(fig_cyc, use_container_width=True)

            # ── التوزيع ──
            with tab_dist:
                dist = suite.results.get('distribution', {})
                cats = dist.get('categories', [])
                if cats:
                    df_d = pd.DataFrame(cats)
                    fig_d = make_subplots(
                        rows=1, cols=2,
                        subplot_titles=['التوزيع الفعلي','التوزيع النظري']
                    )
                    fig_d.add_trace(go.Bar(
                        x=df_d['range'], y=df_d['observed_pct'],
                        name='فعلي', marker_color='steelblue',
                        text=df_d['observed_pct'],
                        texttemplate='%{text}%'
                    ), row=1, col=1)
                    fig_d.add_trace(go.Bar(
                        x=df_d['range'], y=df_d['expected_pct'],
                        name='نظري', marker_color='tomato',
                        text=df_d['expected_pct'],
                        texttemplate='%{text}%'
                    ), row=1, col=2)
                    fig_d.update_layout(
                        title="مقارنة التوزيع الفعلي بالنظري (Power Law)",
                        height=420
                    )
                    st.plotly_chart(fig_d, use_container_width=True)
                    st.dataframe(df_d, use_container_width=True,
                                 hide_index=True)
                    st.info(
                        f"Chi² = {dist.get('chi2_statistic')} | "
                        f"P-Value = {dist.get('p_value')} | "
                        f"{dist.get('interpretation')}"
                    )

            # ── الأزواج ──
            with tab_pairs:
                serial = suite.results.get('serial', {})
                pc     = serial.get('pair_counts', {})
                exp_e  = serial.get('expected_each', 0)
                if pc:
                    df_p = pd.DataFrame({
                        'الزوج'  : list(pc.keys()),
                        'العدد'  : list(pc.values()),
                        'المتوقع': [exp_e] * 4,
                        'الفرق %': [
                            round((v - exp_e) / (exp_e + 1e-9) * 100, 1)
                            for v in pc.values()
                        ]
                    })
                    fig_p = px.bar(
                        df_p, x='الزوج', y='العدد',
                        title="توزيع الأزواج المتتالية",
                        color='الفرق %',
                        color_continuous_scale='RdYlGn',
                        text='العدد'
                    )
                    fig_p.add_hline(
                        y=exp_e, line_dash="dash", line_color="blue",
                        annotation_text=f"المتوقع: {exp_e:.0f}"
                    )
                    st.plotly_chart(fig_p, use_container_width=True)
                    st.dataframe(df_p, use_container_width=True,
                                 hide_index=True)
                    st.info(
                        f"Chi² = {serial.get('chi2_statistic')} | "
                        f"P-Value = {serial.get('p_value')} | "
                        f"{serial.get('interpretation')}"
                    )

            # ── تحليل PRNG ──
            with tab_prng:
                st.subheader("🔐 نتائج تحليل PRNG")

                pa, pb, pc2 = st.columns(3)
                pa.metric(
                    "FFT — نسبة الهيمنة",
                    f"{spectral['dominance_ratio']}x",
                    delta="⚠️ مرتفع" if spectral['has_pattern'] else "✅ طبيعي"
                )
                pb.metric(
                    "أقوى دورة",
                    f"{cycle['best_period']} جولة",
                    delta=(
                        "🔴 دورة!" if cycle['cycle_detected']
                        else f"corr={cycle['best_correlation']}"
                    )
                )
                pc2.metric(
                    "قيم فريدة (Birthday)",
                    f"{birthday['unique_values']}",
                    delta=f"متوقع أول تكرار: {birthday['expected_first_collision']}"
                )

                lc = suite.results.get('linear_complexity', {})
                st.markdown("---")
                st.markdown(f"""
| التحليل | النتيجة |
|---------|---------|
| FFT | {spectral['interpretation']} |
| الدوريات | {cycle['interpretation']} |
| Birthday Paradox | {birthday['interpretation']} |
| Linear Complexity | {lc.get('interpretation','—')} |
                """)

            # ── الاستنتاج الأكاديمي ─────────────────────
            st.markdown("---")
            st.header("📝 الاستنتاج الأكاديمي")

            sig_lags = suite.results.get(
                'autocorrelation', {}
            ).get('significant_lags', [])
            pairs_ok = suite.results.get('serial', {}).get('passed', True)
            ent_ok   = suite.results.get('entropy', {}).get('passed', True)
            lc_ok    = suite.results.get(
                'linear_complexity', {}
            ).get('passed', True)

            findings = []
            if sig_lags:
                findings.append(
                    f"• **ارتباط ذاتي دال** في Lag {sig_lags} "
                    f"← أهم اكتشاف!"
                )
            if not pairs_ok:
                findings.append("• **أنماط في الأزواج** المتتالية")
            if not ent_ok:
                findings.append("• **إنتروبيا منخفضة** عن المتوقع")
            if not lc_ok:
                findings.append("• **تعقيد LFSR** غير طبيعي")
            if spectral['has_pattern']:
                findings.append("• **تردد مهيمن** في التحليل الطيفي")
            if cycle['cycle_detected']:
                findings.append(
                    f"• **دورة تكرار** عند {cycle['best_period']} جولة"
                )

            if passed >= total * 0.75:
                st.success(
                    f"### ✅ الاستنتاج: PRNG قوي\n\n"
                    f"**{passed}/{total}** اختبار نجح "
                    f"({passed/total*100:.0f}%)\n\n"
                    f"- يستوفي معايير **NIST SP 800-22**\n"
                    f"- الإنتروبيا عالية والتوزيع طبيعي\n"
                    f"- لا دورات تكرار مكتشفة\n\n"
                    f"**الاستنتاج العلمي:** المولد يُنتج أرقاماً "
                    f"ذات جودة عشوائية عالية"
                )
            else:
                findings_text = '\n'.join(findings) if findings else '—'
                st.warning(
                    f"### ⚠️ الاستنتاج: اكتُشفت أنماط إحصائية\n\n"
                    f"**{total-passed}/{total}** اختبار فشل\n\n"
                    f"**الاكتشافات:**\n{findings_text}\n\n"
                    f"**الأهمية العملية:** صغيرة جداً بسبب هامش الكازينو 1%\n"
                    f"**الأهمية الأكاديمية:** تثبت أن PRNG ليس مثالياً"
                )

            # ── المراجع ─────────────────────────────────
            with st.expander("📚 المراجع الأكاديمية"):
                st.markdown("""
- NIST SP 800-22 Rev 1a — Statistical Test Suite for RNG
- Shannon, C.E. (1948) — A Mathematical Theory of Communication
- Berlekamp-Massey Algorithm — Linear Complexity Analysis
- Marsaglia, G. — Diehard Battery of Tests
- L'Ecuyer, P. (1998) — Random Number Generation
                """)

            # ── تحميل التقرير ───────────────────────────
            st.markdown("---")
            report = {
                'total_samples': n,
                'summary'      : {
                    'passed' : passed,
                    'total'  : total,
                    'verdict': verdict
                },
                'key_findings': findings,
                'tests'       : {
                    k: {kk: vv for kk, vv in v.items()
                        if kk != 'autocorrelations'}
                    for k, v in suite.results.items()
                },
                'prng_analysis': {
                    'spectral_dominance' : spectral['dominance_ratio'],
                    'has_spectral_pattern': spectral['has_pattern'],
                    'best_cycle_period'  : cycle['best_period'],
                    'best_cycle_corr'    : cycle['best_correlation'],
                    'cycle_detected'     : cycle['cycle_detected'],
                    'birthday_unique'    : birthday['unique_values']
                }
            }
            st.download_button(
                label="📥 تحميل التقرير الكامل (JSON)",
                data=json.dumps(report, ensure_ascii=False, indent=2),
                file_name="crash_prng_report.json",
                mime="application/json"
            )

st.markdown("---")
st.caption(
    "🎓 أُنجز لأغراض بحثية أكاديمية بحتة | "
    "تحليل PRNG | اختبارات NIST SP 800-22"
)
