# randomness_tests.py
"""
مجموعة اختبارات إحصائية لتحليل العشوائية
المرجع: NIST SP 800-22 Standard Tests
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2, kstest, runs
import matplotlib.pyplot as plt
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class RandomnessTestSuite:
    """
    مجموعة اختبارات NIST للعشوائية
    مطبقة على بيانات Crash
    """
    
    def __init__(self, data: list):
        self.raw = np.array(data, dtype=float)
        self.binary = (self.raw >= 2.0).astype(int)
        self.log_data = np.log(np.maximum(self.raw, 1.0))
        self.results = {}
    
    # ==================== Test 1: Frequency Test ====================
    def frequency_test(self) -> dict:
        """
        NIST Test 1: Monobit Frequency Test
        H0: النسبة بين 0 و 1 متساوية
        """
        n = len(self.binary)
        n1 = self.binary.sum()  # عدد المرتفعات
        n0 = n - n1             # عدد المنخفضات
        
        # إحصائية الاختبار
        s_obs = abs(n1 - n0) / np.sqrt(n)
        p_value = 2 * (1 - stats.norm.cdf(s_obs))
        
        result = {
            'test_name': 'Frequency (Monobit) Test',
            'n_high': int(n1),
            'n_low': int(n0),
            'ratio_high': round(n1/n, 4),
            'theoretical_ratio': 0.5,
            'statistic': round(s_obs, 4),
            'p_value': round(p_value, 4),
            'passed': p_value >= 0.01,
            'interpretation': (
                '✅ عشوائي - التوزيع متوازن' 
                if p_value >= 0.01 
                else '🔴 غير عشوائي - خلل في التوزيع'
            )
        }
        self.results['frequency'] = result
        return result
    
    # ==================== Test 2: Runs Test ====================
    def runs_test(self) -> dict:
        """
        NIST Test 3: Runs Test
        H0: التسلسلات المتتالية عشوائية
        """
        n = len(self.binary)
        pi = self.binary.mean()
        
        # شرط المعيار
        tau = 2 / np.sqrt(n)
        if abs(pi - 0.5) > tau:
            return {
                'test_name': 'Runs Test',
                'passed': False,
                'p_value': 0.0,
                'interpretation': '🔴 فشل الاختبار المبدئي - نسبة غير متوازنة'
            }
        
        # حساب التشغيلات
        runs_count = 1 + sum(
            1 for i in range(1, n) 
            if self.binary[i] != self.binary[i-1]
        )
        
        # إحصائية الاختبار
        expected_runs = 2 * n * pi * (1 - pi)
        var_runs = 2 * n * pi * (1 - pi) * (2 * pi * (1-pi) - 1/n)
        
        if var_runs <= 0:
            p_value = 1.0
        else:
            z = (runs_count - expected_runs) / np.sqrt(var_runs)
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
        
        result = {
            'test_name': 'Runs Test',
            'runs_observed': int(runs_count),
            'runs_expected': round(expected_runs, 2),
            'statistic': round(z if var_runs > 0 else 0, 4),
            'p_value': round(p_value, 4),
            'passed': p_value >= 0.01,
            'interpretation': (
                '✅ عشوائي - التسلسلات طبيعية'
                if p_value >= 0.01
                else '🔴 غير عشوائي - أنماط في التسلسلات'
            )
        }
        self.results['runs'] = result
        return result
    
    # ==================== Test 3: Autocorrelation Test ====================
    def autocorrelation_test(self, max_lag: int = 20) -> dict:
        """
        اختبار الارتباط الذاتي
        H0: لا يوجد ارتباط بين النتائج المتتالية
        """
        n = len(self.binary)
        significant_lags = []
        autocorrs = []
        
        # حد الدلالة الإحصائية
        significance_bound = 1.96 / np.sqrt(n)
        
        for lag in range(1, max_lag + 1):
            # حساب الارتباط الذاتي
            acf = np.corrcoef(
                self.binary[lag:], 
                self.binary[:-lag]
            )[0, 1]
            
            autocorrs.append({
                'lag': lag,
                'autocorrelation': round(float(acf), 6),
                'significant': abs(acf) > significance_bound,
                'bound': round(significance_bound, 4)
            })
            
            if abs(acf) > significance_bound:
                significant_lags.append(lag)
        
        result = {
            'test_name': 'Autocorrelation Test',
            'max_lag_tested': max_lag,
            'significance_bound': round(significance_bound, 4),
            'significant_lags': significant_lags,
            'n_significant': len(significant_lags),
            'autocorrelations': autocorrs,
            'passed': len(significant_lags) == 0,
            'interpretation': (
                '✅ عشوائي - لا ارتباط بين النتائج'
                if len(significant_lags) == 0
                else f'🔴 وُجد ارتباط في Lags: {significant_lags}'
            )
        }
        self.results['autocorrelation'] = result
        return result
    
    # ==================== Test 4: Chi-Square Distribution Test ====================
    def distribution_test(self) -> dict:
        """
        اختبار انطباق التوزيع
        H0: البيانات تتبع توزيع Power Law (1/x)
        """
        # الفئات
        bins = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0, float('inf')]
        labels = ['1-1.5x', '1.5-2x', '2-3x', '3-5x', '5-10x', '>10x']
        
        n = len(self.raw)
        
        # التوزيع النظري لـ Crash (Power Law)
        # P(X >= x) = house_edge / x ≈ 0.99/x
        house_edge = 0.99
        theoretical_probs = []
        for i in range(len(bins) - 1):
            p_low = min(house_edge / bins[i], 1.0)
            p_high = min(house_edge / bins[i+1], 1.0) if bins[i+1] != float('inf') else 0.0
            theoretical_probs.append(p_low - p_high)
        
        # تطبيع
        total_p = sum(theoretical_probs)
        theoretical_probs = [p/total_p for p in theoretical_probs]
        
        # التوزيع الفعلي
        observed = []
        for i in range(len(bins) - 1):
            if bins[i+1] == float('inf'):
                count = (self.raw >= bins[i]).sum()
            else:
                count = ((self.raw >= bins[i]) & (self.raw < bins[i+1])).sum()
            observed.append(int(count))
        
        # اختبار Chi-Square
        expected = [p * n for p in theoretical_probs]
        
        # تجميع الفئات الصغيرة
        chi2_stat, p_value = stats.chisquare(observed, expected)
        
        result = {
            'test_name': 'Chi-Square Distribution Test',
            'categories': [
                {
                    'range': labels[i],
                    'observed': observed[i],
                    'expected': round(expected[i], 1),
                    'observed_pct': round(observed[i]/n*100, 1),
                    'expected_pct': round(theoretical_probs[i]*100, 1)
                }
                for i in range(len(labels))
            ],
            'chi2_statistic': round(chi2_stat, 4),
            'p_value': round(p_value, 4),
            'degrees_of_freedom': len(labels) - 1,
            'passed': p_value >= 0.01,
            'interpretation': (
                '✅ البيانات تتبع التوزيع النظري'
                if p_value >= 0.01
                else '🔴 انحراف عن التوزيع النظري - قد يوجد نمط!'
            )
        }
        self.results['distribution'] = result
        return result
    
    # ==================== Test 5: Longest Run Test ====================
    def longest_run_test(self) -> dict:
        """
        NIST Test 4: Longest Run of Ones
        H0: أطول تسلسل متتالي ضمن الحدود الطبيعية
        """
        # إيجاد التسلسلات
        max_run_high = 0
        max_run_low = 0
        current_high = 0
        current_low = 0
        
        run_lengths_high = []
        run_lengths_low = []
        
        for val in self.binary:
            if val == 1:
                current_high += 1
                current_low = 0
                max_run_high = max(max_run_high, current_high)
            else:
                current_low += 1
                current_high = 0
                max_run_low = max(max_run_low, current_low)
            
            if current_high > 0:
                run_lengths_high.append(current_high)
            if current_low > 0:
                run_lengths_low.append(current_low)
        
        n = len(self.binary)
        # الحد النظري (3 * log2(n))
        theoretical_max = 3 * np.log2(n) if n > 0 else 10
        
        result = {
            'test_name': 'Longest Run Test',
            'max_consecutive_high': int(max_run_high),
            'max_consecutive_low': int(max_run_low),
            'theoretical_max_normal': round(theoretical_max, 1),
            'high_exceeds_limit': max_run_high > theoretical_max,
            'low_exceeds_limit': max_run_low > theoretical_max,
            'passed': (max_run_high <= theoretical_max * 1.5 and 
                      max_run_low <= theoretical_max * 1.5),
            'interpretation': (
                '✅ التسلسلات ضمن الحدود الطبيعية'
                if max_run_high <= theoretical_max * 1.5
                else f'🔴 تسلسل غير طبيعي: {max_run_high} متتالية!'
            )
        }
        self.results['longest_run'] = result
        return result
    
    # ==================== Test 6: Entropy Test ====================
    def entropy_test(self) -> dict:
        """
        اختبار الإنتروبيا (Shannon Entropy)
        H0: الإنتروبيا تقترب من القيمة النظرية
        """
        # إنتروبيا ثنائية
        p_high = self.binary.mean()
        p_low = 1 - p_high
        
        if p_high > 0 and p_low > 0:
            entropy_binary = -(
                p_high * np.log2(p_high) + 
                p_low * np.log2(p_low)
            )
        else:
            entropy_binary = 0
        
        # الإنتروبيا النظرية (عشوائي تام = 1.0 bit)
        max_entropy = 1.0
        
        # إنتروبيا القيم المستمرة (بعد التقطيع)
        n_bins = 20
        hist, _ = np.histogram(self.log_data, bins=n_bins)
        hist = hist[hist > 0]
        probs = hist / hist.sum()
        entropy_continuous = -np.sum(probs * np.log2(probs))
        max_continuous = np.log2(n_bins)
        
        result = {
            'test_name': 'Shannon Entropy Test',
            'binary_entropy': round(entropy_binary, 6),
            'max_binary_entropy': max_entropy,
            'entropy_efficiency': round(entropy_binary / max_entropy * 100, 2),
            'continuous_entropy': round(entropy_continuous, 4),
            'max_continuous_entropy': round(max_continuous, 4),
            'passed': entropy_binary >= 0.95,
            'interpretation': (
                '✅ إنتروبيا عالية - يشبه العشوائي'
                if entropy_binary >= 0.95
                else f'🔴 إنتروبيا منخفضة ({entropy_binary:.3f}) - قد يوجد نمط!'
            )
        }
        self.results['entropy'] = result
        return result
    
    # ==================== Test 7: Serial Test ====================
    def serial_test(self) -> dict:
        """
        اختبار الأزواج المتتالية
        H0: توزيع الأزواج المتتالية متساوي
        """
        pairs = Counter(zip(self.binary[:-1], self.binary[1:]))
        n_pairs = len(self.binary) - 1
        
        expected = n_pairs / 4  # 4 أزواج ممكنة: (0,0),(0,1),(1,0),(1,1)
        
        observed_counts = [
            pairs.get((0,0), 0),
            pairs.get((0,1), 0),
            pairs.get((1,0), 0),
            pairs.get((1,1), 0)
        ]
        
        chi2_stat = sum(
            (o - expected)**2 / expected 
            for o in observed_counts
        )
        p_value = 1 - chi2.cdf(chi2_stat, df=3)
        
        result = {
            'test_name': 'Serial (Pairs) Test',
            'pair_counts': {
                'low_low': pairs.get((0,0), 0),
                'low_high': pairs.get((0,1), 0),
                'high_low': pairs.get((1,0), 0),
                'high_high': pairs.get((1,1), 0)
            },
            'expected_each': round(expected, 1),
            'chi2_statistic': round(chi2_stat, 4),
            'p_value': round(p_value, 4),
            'passed': p_value >= 0.01,
            'interpretation': (
                '✅ توزيع الأزواج عشوائي'
                if p_value >= 0.01
                else '🔴 أنماط في الأزواج المتتالية!'
            )
        }
        self.results['serial'] = result
        return result
    
    # ==================== تشغيل جميع الاختبارات ====================
    def run_all_tests(self) -> dict:
        """تشغيل المجموعة الكاملة"""
        print("🔬 تشغيل مجموعة اختبارات العشوائية NIST...")
        print("=" * 60)
        
        tests = [
            self.frequency_test,
            self.runs_test,
            self.autocorrelation_test,
            self.distribution_test,
            self.longest_run_test,
            self.entropy_test,
            self.serial_test
        ]
        
        passed = 0
        total = len(tests)
        
        for test_fn in tests:
            result = test_fn()
            status = "✅" if result.get('passed', False) else "❌"
            print(f"{status} {result['test_name']}: p={result.get('p_value', 'N/A')}")
            if result.get('passed', False):
                passed += 1
        
        print("=" * 60)
        print(f"📊 النتيجة: {passed}/{total} اختبار نجح")
        
        verdict = (
            "عشوائي إحصائياً" if passed >= total * 0.8
            else "يحتوي على أنماط إحصائية قابلة للاكتشاف"
        )
        print(f"🎯 الحكم: {verdict}")
        
        return {
            'passed_tests': passed,
            'total_tests': total,
            'pass_rate': round(passed/total, 3),
            'verdict': verdict,
            'details': self.results
        }
