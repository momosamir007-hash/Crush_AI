# prng_analysis.py
"""
تحليل مولد الأرقام الزائفة العشوائية
محاولة اكتشاف seed أو دورة التكرار
"""

import numpy as np
from scipy.fft import fft, fftfreq
import pandas as pd

class PRNGAnalyzer:
    """
    تحليل خصائص PRNG في لعبة Crash
    """
    
    def __init__(self, data: list):
        self.raw = np.array(data, dtype=float)
        self.log_data = np.log(np.maximum(self.raw, 1.0))
        self.binary = (self.raw >= 2.0).astype(int)
    
    def spectral_analysis(self) -> dict:
        """
        تحليل طيفي (FFT) لاكتشاف الدوريات
        إذا وُجدت ترددات مهيمنة = يوجد نمط
        """
        n = len(self.log_data)
        
        # تطبيق FFT
        fft_vals = np.abs(fft(self.log_data - np.mean(self.log_data)))
        freqs = fftfreq(n)
        
        # نصف الطيف (موجب)
        half = n // 2
        fft_magnitude = fft_vals[:half]
        frequencies = freqs[:half]
        
        # أقوى الترددات
        top_indices = np.argsort(fft_magnitude)[-10:][::-1]
        
        dominant_freqs = []
        for idx in top_indices:
            if frequencies[idx] > 0:
                period = 1 / frequencies[idx]
                dominant_freqs.append({
                    'frequency': round(float(frequencies[idx]), 6),
                    'period': round(float(period), 2),
                    'magnitude': round(float(fft_magnitude[idx]), 4),
                    'relative_power': round(
                        float(fft_magnitude[idx]) / fft_magnitude.max(), 4
                    )
                })
        
        # هل يوجد تردد مهيمن؟
        max_magnitude = fft_magnitude.max()
        mean_magnitude = fft_magnitude.mean()
        dominance_ratio = max_magnitude / mean_magnitude
        
        return {
            'analysis': 'Spectral (FFT) Analysis',
            'dominant_frequencies': dominant_freqs[:5],
            'dominance_ratio': round(dominance_ratio, 4),
            'has_dominant_pattern': dominance_ratio > 10,
            'interpretation': (
                f'🔴 يوجد تردد مهيمن! نسبة: {dominance_ratio:.1f}x - نمط محتمل'
                if dominance_ratio > 10
                else f'✅ لا ترددات مهيمنة - عشوائي طيفياً (نسبة: {dominance_ratio:.1f}x)'
            )
        }
    
    def cycle_detection(self, max_period: int = 100) -> dict:
        """
        اكتشاف دورات التكرار
        خوارزمية Floyd لاكتشاف الدورة
        """
        best_period = None
        best_correlation = 0
        correlations = []
        
        for period in range(2, min(max_period, len(self.raw) // 3)):
            # حساب الارتباط مع النفس بعد period
            x = self.log_data[:-period]
            y = self.log_data[period:]
            
            if len(x) < 10:
                break
                
            corr = np.corrcoef(x, y)[0, 1]
            correlations.append({
                'period': period,
                'correlation': round(float(corr), 6)
            })
            
            if abs(corr) > abs(best_correlation):
                best_correlation = corr
                best_period = period
        
        significant_periods = [
            c for c in correlations 
            if abs(c['correlation']) > 0.3
        ]
        
        return {
            'analysis': 'Cycle Detection',
            'best_period': best_period,
            'best_correlation': round(best_correlation, 4),
            'significant_periods': significant_periods[:5],
            'cycle_detected': abs(best_correlation) > 0.5,
            'interpretation': (
                f'🔴 دورة تكرار محتملة عند period={best_period}! corr={best_correlation:.3f}'
                if abs(best_correlation) > 0.5
                else f'✅ لا دورات واضحة (أقوى ارتباط: {best_correlation:.3f})'
            )
        }
    
    def birthday_paradox_test(self) -> dict:
        """
        اختبار مفارقة عيد الميلاد
        إذا تكررت أنماط أسرع من المتوقع = PRNG ضعيف
        """
        # تقطيع القيم إلى 100 فئة
        quantized = np.round(self.log_data, 1)
        n = len(quantized)
        
        # إيجاد أول تكرار
        seen = {}
        first_collision = None
        
        for i, val in enumerate(quantized):
            if val in seen:
                first_collision = {
                    'position': i,
                    'original_position': seen[val],
                    'value': float(val),
                    'gap': i - seen[val]
                }
                break
            seen[val] = i
        
        # التكرار المتوقع نظرياً
        unique_vals = len(np.unique(quantized))
        expected_collision = np.sqrt(np.pi * unique_vals / 2)
        
        return {
            'analysis': 'Birthday Paradox Test',
            'unique_values': unique_vals,
            'expected_first_collision': round(expected_collision, 1),
            'actual_first_collision': first_collision,
            'total_observations': n,
            'interpretation': (
                '✅ التكرار في حدوده الطبيعية'
                if first_collision is None or 
                   first_collision['position'] >= expected_collision * 0.5
                else f'🔴 تكرار مبكر عند position {first_collision["position"]}!'
            )
        }
    
    def linear_complexity_test(self, window: int = 50) -> dict:
        """
        تعقيد التسلسل الخطي (Berlekamp-Massey approximation)
        تسلسل عشوائي = تعقيد عالٍ
        تسلسل PRNG ضعيف = تعقيد منخفض
        """
        # حساب تعقيد نافذة منزلقة
        complexities = []
        
        for i in range(0, len(self.binary) - window, window // 2):
            segment = self.binary[i:i+window]
            
            # تقريب LFSR complexity
            n = len(segment)
            changes = sum(
                1 for j in range(1, n) 
                if segment[j] != segment[j-1]
            )
            
            # تعقيد تقريبي: عدد التغييرات / 2
            complexity = changes / 2
            complexities.append(complexity)
        
        avg_complexity = np.mean(complexities)
        theoretical = window / 2  # المتوقع للعشوائي التام
        
        complexity_ratio = avg_complexity / theoretical
        
        return {
            'analysis': 'Linear Complexity Test',
            'window_size': window,
            'avg_complexity': round(avg_complexity, 2),
            'theoretical_complexity': round(theoretical, 2),
            'complexity_ratio': round(complexity_ratio, 4),
            'passed': 0.4 <= complexity_ratio <= 0.6,
            'interpretation': (
                '✅ تعقيد طبيعي - يشبه العشوائي'
                if 0.4 <= complexity_ratio <= 0.6
                else f'🔴 تعقيد غير طبيعي ({complexity_ratio:.3f}) - PRNG قابل للتحليل!'
            )
        }
    
    def run_full_analysis(self) -> dict:
        """تشغيل التحليل الكامل"""
        print("\n🔐 تحليل PRNG المتقدم")
        print("=" * 60)
        
        results = {}
        
        analyses = [
            ('spectral', self.spectral_analysis),
            ('cycle', self.cycle_detection),
            ('birthday', self.birthday_paradox_test),
            ('complexity', self.linear_complexity_test)
        ]
        
        for name, fn in analyses:
            result = fn()
            results[name] = result
            print(f"\n📊 {result['analysis']}:")
            print(f"   {result['interpretation']}")
        
        return results
