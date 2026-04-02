# grid_visualizer.py
"""
╔═══════════════════════════════════════════════════╗
║ 🎨 Candy Crush Grid Visualizer ║
║ رسم الأسهم + تلوين الشبكة + عرض الحركات ║
╚═══════════════════════════════════════════════════╝
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Optional
import math

# ═══════════════════════════════════
# ألوان الحلوى (BGR لـ OpenCV)
# ═══════════════════════════════════
CANDY_COLORS_BGR = {
    'red': (60, 60, 220),
    'blue': (220, 120, 40),
    'green': (60, 200, 60),
    'yellow': (40, 220, 220),
    'orange': (40, 160, 240),
    'purple': (180, 60, 180),
    'empty': (180, 180, 180),
}

CANDY_COLORS_RGB = {
    'red': (220, 60, 60),
    'blue': (40, 120, 220),
    'green': (60, 200, 60),
    'yellow': (220, 220, 40),
    'orange': (240, 160, 40),
    'purple': (180, 60, 180),
    'empty': (180, 180, 180),
}

CANDY_EMOJI = {
    'red': '🔴',
    'blue': '🔵',
    'green': '🟢',
    'yellow': '🟡',
    'orange': '🟠',
    'purple': '🟣',
    'empty': '⬜',
    'unknown': '❓'
}

def draw_arrows_on_image(
    image: np.ndarray,
    grid: np.ndarray,
    moves: List[Dict],
    top_n: int = 3
) -> np.ndarray:
    """رسم أسهم الحركات المقترحة على صورة اللوحة

    Args:
        image: صورة اللوحة (BGR أو RGB)
        grid: مصفوفة الشبكة 9×9
        moves: قائمة الحركات من المحرك
        top_n: عدد الحركات المراد رسمها

    Returns:
        صورة مع الأسهم مرسومة عليها
    """
    result = image.copy()
    h, w = result.shape[:2]
    rows, cols = grid.shape
    cell_h = h // rows
    cell_w = w // cols

    # ═══ ألوان الأسهم حسب الترتيب ═══
    arrow_styles = [
        {   # أفضل حركة - ذهبي كبير
            'color': (0, 215, 255),
            'thickness': 4,
            'tip_length': 0.35,
            'glow_color': (0, 180, 255),
            'label': '1st',
            'badge_color': (0, 200, 255),
        },
        {   # ثاني أفضل - فضي
            'color': (192, 192, 192),
            'thickness': 3,
            'tip_length': 0.3,
            'glow_color': (160, 160, 160),
            'label': '2nd',
            'badge_color': (192, 192, 192),
        },
        {   # ثالث - برونزي
            'color': (80, 127, 205),
            'thickness': 2,
            'tip_length': 0.3,
            'glow_color': (60, 100, 170),
            'label': '3rd',
            'badge_color': (80, 127, 205),
        },
    ]

    selected_moves = moves[:top_n]

    for idx, move in enumerate(selected_moves):
        style = arrow_styles[min(idx, len(arrow_styles) - 1)]
        r1, c1 = move['pos1']
        r2, c2 = move['pos2']

        # مركز كل خلية
        x1 = c1 * cell_w + cell_w // 2
        y1 = r1 * cell_h + cell_h // 2
        x2 = c2 * cell_w + cell_w // 2
        y2 = r2 * cell_h + cell_h // 2

        # ═══ رسم التوهج (Glow Effect) ═══
        cv2.arrowedLine(
            result, (x1, y1), (x2, y2),
            style['glow_color'],
            thickness=style['thickness'] + 4,
            tipLength=style['tip_length'],
            line_type=cv2.LINE_AA
        )

        # ═══ رسم السهم الرئيسي ═══
        cv2.arrowedLine(
            result, (x1, y1), (x2, y2),
            style['color'],
            thickness=style['thickness'],
            tipLength=style['tip_length'],
            line_type=cv2.LINE_AA
        )

        # ═══ دائرة عند نقطة البداية ═══
        cv2.circle(result, (x1, y1), 8, style['color'], -1, cv2.LINE_AA)
        cv2.circle(result, (x1, y1), 8, (255, 255, 255), 2, cv2.LINE_AA)

        # ═══ شارة الترتيب ═══
        badge_x = min(x1, x2) + abs(x2 - x1) // 2
        badge_y = min(y1, y2) + abs(y2 - y1) // 2 - 15

        # خلفية الشارة
        cv2.rectangle(
            result,
            (badge_x - 18, badge_y - 10),
            (badge_x + 18, badge_y + 10),
            style['badge_color'],
            -1,
            cv2.LINE_AA
        )
        cv2.rectangle(
            result,
            (badge_x - 18, badge_y - 10),
            (badge_x + 18, badge_y + 10),
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

        # نص الترتيب
        cv2.putText(
            result, style['label'],
            (badge_x - 14, badge_y + 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35,
            (0, 0, 0), 1, cv2.LINE_AA
        )

        # ═══ نص النقاط ═══
        score_text = f"{move['score']}pts"
        score_x = badge_x - 15
        score_y = badge_y + 25

        # خلفية النقاط
        (tw, th), _ = cv2.getTextSize(
            score_text, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1
        )
        cv2.rectangle(
            result,
            (score_x - 2, score_y - th - 2),
            (score_x + tw + 2, score_y + 4),
            (0, 0, 0),
            -1
        )
        cv2.putText(
            result, score_text,
            (score_x, score_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35,
            (255, 255, 255), 1, cv2.LINE_AA
        )

    return result

def draw_grid_overlay(
    image: np.ndarray,
    grid: np.ndarray,
    show_labels: bool = True,
    opacity: float = 0.3
) -> np.ndarray:
    """رسم شبكة ملونة شفافة فوق الصورة"""
    result = image.copy()
    overlay = image.copy()
    h, w = result.shape[:2]
    rows, cols = grid.shape
    cell_h = h // rows
    cell_w = w // cols

    for r in range(rows):
        for c in range(cols):
            candy = grid[r, c]
            color = CANDY_COLORS_BGR.get(candy, (128, 128, 128))
            x1 = c * cell_w
            y1 = r * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            # مربع ملون شفاف
            cv2.rectangle(overlay, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), color, -1)

            if show_labels:
                # حرف اللون
                label = candy[0].upper() if candy != 'empty' else '.'
                font_scale = min(cell_w, cell_h) / 80.0
                cv2.putText(
                    overlay, label,
                    (x1 + cell_w // 3, y1 + cell_h * 2 // 3),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                    (255, 255, 255), 2, cv2.LINE_AA
                )

    # خطوط الشبكة
    for r in range(rows + 1):
        y = min(r * cell_h, h - 1)
        cv2.line(overlay, (0, y), (w, y), (255, 255, 255), 1)
    for c in range(cols + 1):
        x = min(c * cell_w, w - 1)
        cv2.line(overlay, (x, 0), (x, h), (255, 255, 255), 1)

    # دمج شفاف
    cv2.addWeighted(overlay, opacity, result, 1 - opacity, 0, result)
    return result

def create_grid_image(
    grid: np.ndarray,
    cell_size: int = 60,
    show_coords: bool = True
) -> np.ndarray:
    """إنشاء صورة نظيفة للشبكة من الصفر (بدون صورة خلفية)"""
    rows, cols = grid.shape
    margin = 30 if show_coords else 5
    w = cols * cell_size + margin
    h = rows * cell_size + margin
    img = np.ones((h, w, 3), dtype=np.uint8) * 40  # خلفية داكنة

    for r in range(rows):
        for c in range(cols):
            candy = grid[r, c]
            color = CANDY_COLORS_BGR.get(candy, (128, 128, 128))
            x1 = margin + c * cell_size
            y1 = margin + r * cell_size
            x2 = x1 + cell_size - 3
            y2 = y1 + cell_size - 3

            # مربع الحلوى مع حواف مستديرة (تقريب)
            cv2.rectangle(img, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), color, -1, cv2.LINE_AA)
            # حدود
            cv2.rectangle(img, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), (255, 255, 255), 1, cv2.LINE_AA)

            # حرف اللون
            label = candy[0].upper() if candy not in ['empty', 'unknown'] else ''
            if label:
                cv2.putText(
                    img, label,
                    (x1 + cell_size // 3, y1 + cell_size * 2 // 3),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 1, cv2.LINE_AA
                )

    # أرقام الصفوف
    if show_coords:
        for r in range(rows):
            cv2.putText(
                img, str(r),
                (5, margin + r * cell_size + cell_size // 2 + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                (200, 200, 200), 1
            )
        for c in range(cols):
            cv2.putText(
                img, str(c),
                (margin + c * cell_size + cell_size // 3, margin - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                (200, 200, 200), 1
            )

    return img

def create_move_diagram(
    grid: np.ndarray,
    move: Dict,
    cell_size: int = 60
) -> np.ndarray:
    """إنشاء رسم تخطيطي لحركة واحدة مع سهم"""
    # إنشاء صورة الشبكة
    img = create_grid_image(grid, cell_size, show_coords=True)
    margin = 30
    r1, c1 = move['pos1']
    r2, c2 = move['pos2']

    # مركز كل خلية
    x1 = margin + c1 * cell_size + cell_size // 2
    y1 = margin + r1 * cell_size + cell_size // 2
    x2 = margin + c2 * cell_size + cell_size // 2
    y2 = margin + r2 * cell_size + cell_size // 2

    # تمييز الخليتين
    cv2.rectangle(
        img,
        (margin + c1 * cell_size + 1, margin + r1 * cell_size + 1),
        (margin + (c1 + 1) * cell_size - 2, margin + (r1 + 1) * cell_size - 2),
        (0, 255, 255), 3, cv2.LINE_AA
    )
    cv2.rectangle(
        img,
        (margin + c2 * cell_size + 1, margin + r2 * cell_size + 1),
        (margin + (c2 + 1) * cell_size - 2, margin + (r2 + 1) * cell_size - 2),
        (0, 255, 255), 3, cv2.LINE_AA
    )

    # سهم ذهبي كبير
    cv2.arrowedLine(
        img, (x1, y1), (x2, y2),
        (0, 215, 255), 4,
        tipLength=0.35, line_type=cv2.LINE_AA
    )

    # دائرة البداية
    cv2.circle(img, (x1, y1), 6, (0, 255, 255), -1, cv2.LINE_AA)
    return img

def highlight_matches(
    image: np.ndarray,
    grid: np.ndarray,
    move: Dict,
    engine  # CandyEngine instance
) -> np.ndarray:
    """تمييز الحلوى التي ستختفي بعد الحركة"""
    result = image.copy()
    h, w = result.shape[:2]
    rows, cols = grid.shape
    cell_h = h // rows
    cell_w = w // cols

    # محاكاة التبديل
    temp = np.copy(grid)
    r1, c1 = move['pos1']
    r2, c2 = move['pos2']
    temp[r1, c1], temp[r2, c2] = temp[r2, c2], temp[r1, c1]

    # إيجاد الخلايا المطابقة
    matched_cells = set()
    for r in range(rows):
        for c in range(cols):
            color = temp[r, c]
            if color in ['empty', 'unknown']:
                continue
            # أفقي
            count_h = 1
            cc = c + 1
            while cc < cols and temp[r, cc] == color:
                count_h += 1
                cc += 1
            if count_h >= 3:
                for ci in range(c, c + count_h):
                    matched_cells.add((r, ci))
            # عمودي
            count_v = 1
            rr = r + 1
            while rr < rows and temp[rr, c] == color:
                count_v += 1
                rr += 1
            if count_v >= 3:
                for ri in range(r, r + count_v):
                    matched_cells.add((ri, c))

    # رسم التمييز
    overlay = result.copy()
    for (r, c) in matched_cells:
        x1 = c * cell_w + 3
        y1 = r * cell_h + 3
        x2 = x1 + cell_w - 6
        y2 = y1 + cell_h - 6
        # هالة متوهجة
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 255), -1)
        # علامة X
        cv2.line(result, (x1 + 5, y1 + 5), (x2 - 5, y2 - 5), (0, 0, 255), 2, cv2.LINE_AA)
        cv2.line(result, (x2 - 5, y1 + 5), (x1 + 5, y2 - 5), (0, 0, 255), 2, cv2.LINE_AA)

    cv2.addWeighted(overlay, 0.25, result, 0.75, 0, result)

    # عدد الحلوى المحذوفة
    text = f"{len(matched_cells)} candies matched!"
    cv2.putText(
        result, text,
        (10, h - 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
        (0, 255, 255), 2, cv2.LINE_AA
    )
    return result
