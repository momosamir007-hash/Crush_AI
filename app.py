import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO
from move_engine import CandyEngine
import os

st.set_page_config(page_title="Candy Crush AI", layout="centered")
st.title("🍬 العرّاف: مساعد كاندي كراش")
st.markdown("---")

@st.cache_resource
def load_model():
    model_path = "best.pt"
    if not os.path.exists(model_path):
        return None
    return YOLO(model_path)

model = load_model()
if model is None:
    st.error("❌ ملف best.pt غير موجود! تأكد من رفعه.")
    st.stop()

st.sidebar.success("✅ النموذج جاهز للعمل!")

class_map = {
    0: 'red',
    1: 'blue',
    2: 'green',
    3: 'yellow',
    4: 'orange',
    5: 'purple',
    6: 'blocker'
}

st.info("💡 نصيحة: ارفع صورة مقصوصة تحتوي على لوحة اللعب فقط (9x9)")

uploaded_file = st.file_uploader("📷 ارفع صورة اللوحة...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    if st.button("🚀 تحليل ورسم أفضل حركة"):
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)
        h, w, _ = img_np.shape

        with st.spinner("الذكاء الاصطناعي يقرأ اللوحة..."):
            results = model.predict(img_np, conf=0.35)
            boxes = results[0].boxes
            grid = np.full((9, 9), 'empty', dtype=object)
            cell_w = w / 9.0
            cell_h = h / 9.0

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                cls = int(box.cls[0].item())
                cx = (x1 + x2) / 2.0
                cy = (y1 + y2) / 2.0
                col = int(cx // cell_w)
                row = int(cy // cell_h)
                col = min(max(col, 0), 8)
                row = min(max(row, 0), 8)
                grid[row, col] = class_map.get(cls, 'empty')

            engine = CandyEngine(grid)
            moves = engine.find_all_moves()

        st.markdown("---")
        st.subheader("💡 الحل البصري المقترح:")

        if moves:
            best_move = moves[0]
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            r1, c1 = best_move['pos1']
            r2, c2 = best_move['pos2']

            p1x = int((c1 + 0.5) * cell_w)
            p1y = int((r1 + 0.5) * cell_h)
            p2x = int((c2 + 0.5) * cell_w)
            p2y = int((r2 + 0.5) * cell_h)

            p1_pixel = (p1x, p1y)
            p2_pixel = (p2x, p2y)

            overlay = img_bgr.copy()
            radius = int(min(cell_w, cell_h) * 0.4)
            cv2.circle(overlay, p1_pixel, radius, (0, 255, 0), -1)
            img_bgr = cv2.addWeighted(img_bgr, 0.6, overlay, 0.4, 0)
            cv2.arrowedLine(
                img_bgr,
                p1_pixel,
                p2_pixel,
                (0, 255, 0),
                10,
                tipLength=0.4,
                line_type=cv2.LINE_AA
            )

            result_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
            st.image(result_img, caption="🥇 هذه هي الحركة الأفضل!", use_container_width=True)

            st.success(
                "حرك من الصف " + str(r1) + " العمود " + str(c1) + " ➜ " + best_move['direction']
            )
            st.info(
                "✨ النتيجة المتوقعة: " + str(best_move['score']) + " نقطة (" + best_move['details'] + ")"
            )
        else:
            st.image(image, use_container_width=True)
            st.warning("⚠️ لم يتم العثور على حركات مطابقة.")
