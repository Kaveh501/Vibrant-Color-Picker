import streamlit as st
import json
from PIL import Image, ImageDraw
from io import BytesIO

st.set_page_config(
    page_title="🎨 Vibrant Color Picker | انتخاب رنگ جیغ", layout="centered")

# انتخاب زبان
lang = st.radio("Language | زبان", ["English", "فارسی"], horizontal=True)

# دیکشنری ترجمه
text = {
    "English": {
        "title": "🎨 Vibrant Color Picker",
        "select_category": "Choose a vibrant palette:",
        "pick_one": "💎 Pick one:",
        "choose_btn": "Choose",
        "you_chose": "You chose:",
        "copy": "📋 Copy HEX",
        "download_palette": "⬇️ Download Full Palette as Image",
        "feedback_question": "How much did you like this interface?",
        "feedback_options": ["Loved it!", "It’s okay", "Meh"],
        "feedback_thanks": "Thanks for your feedback! 🙏",
        "thanks_button": "🙏 Thanks!",
        "thanks_msg": "Thanks for choosing this app! 🙏"
    },
    "فارسی": {
        "title": "🎨 انتخاب رنگ جیغ",
        "select_category": "یک پالت پرانرژی انتخاب کن:",
        "pick_one": "💎 یکی رو انتخاب کن:",
        "choose_btn": "انتخاب",
        "you_chose": "تو انتخاب کردی:",
        "copy": "📋 کپی رنگ",
        "download_palette": "⬇️ دانلود تصویر کامل پالت",
        "feedback_question": "چقدر این رابط کاربری رو دوست داشتی؟",
        "feedback_options": ["زیاد دوست داشتم", "متوسط بود", "خیلی خوشم نیومد"],
        "feedback_thanks": "مرسی بابت نظرت 🙏",
        "thanks_button": "🙏 مرسی!",
        "thanks_msg": "از انتخاب این اپ ممنونیم 🙏"
    }
}

t = text[lang]

st.title(t["title"])

palettes = {
    "🔥 Energetic (پرانرژی)": ["#FF007F", "#FF6F00", "#FFD700", "#FF1493", "#FF4500"],
    "🌈 Pop & Neon (نئون)": ["#39FF14", "#00FFFF", "#FF00FF", "#FFFF00", "#FF5F1F"],
    "🍭 Candy Vibes (آب‌نباتی)": ["#FF69B4", "#FFB6C1", "#FFA07A", "#F08080", "#DB7093"],
    "🌞 Sunshine (آفتابی)": ["#FFC300", "#FFA500", "#FF6347", "#FFEC8B", "#FFDAB9"]
}

selected_palette = st.selectbox(t["select_category"], list(palettes.keys()))
colors = palettes[selected_palette]

st.markdown(f"### {t['pick_one']}")
selected_color = None

cols = st.columns(len(colors))
for i, color in enumerate(colors):
    with cols[i]:
        st.markdown(
            f"""
            <div style="background-color:{color}; width:100px; height:100px; border-radius:12px;
                        border:2px solid #333; margin-bottom:8px; box-shadow: 1px 1px 6px #000;"></div>
            """, unsafe_allow_html=True
        )
        if st.button(t["choose_btn"], key=color):
            selected_color = color

if selected_color:
    st.success(f"{t['you_chose']} {selected_color}")
    st.code(selected_color)


def generate_palette_image(colors):
    block_size = 100
    padding = 10
    width = len(colors) * (block_size + padding)
    height = block_size + 50

    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    for i, hex_color in enumerate(colors):
        x = i * (block_size + padding)
        draw.rectangle(
            [x, 0, x + block_size, block_size],
            fill=hex_color
        )
        draw.text((x + 10, block_size + 10), hex_color, fill="black")

    return image


img = generate_palette_image(colors)
buffered = BytesIO()
img.save(buffered, format="PNG")
st.download_button(
    label=t["download_palette"],
    data=buffered.getvalue(),
    file_name="palette.png",
    mime="image/png"
)

st.markdown("---")
st.subheader("🗣️ " + (t["feedback_question"]))
feedback_choice = st.radio(t["feedback_question"],
                           t["feedback_options"], horizontal=True)

if feedback_choice:
    if st.button(t["thanks_button"]):
        st.success(t["thanks_msg"])
