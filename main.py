import os
import base64
from pathlib import Path

from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# ===== Paths and environment =====
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = os.getenv("MODEL")
if not MODEL:
    raise ValueError("MODEL is missing from your .env file.")

# ===== Prompt (change only this file name between iterations) =====
PROMPT_PATH = BASE_DIR / "prompts" / "v3.md"
if not PROMPT_PATH.exists():
    raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

# ===== Background image (must be in the images folder) =====
FRAME_PATH = BASE_DIR / "images" / "cyber-frame.png"
if not FRAME_PATH.exists():
    raise FileNotFoundError(
        "Background image not found: put cyber-frame.png inside the images folder."
    )
encoded_image = base64.b64encode(FRAME_PATH.read_bytes()).decode("ascii")
FRAME_BACKGROUND = f"data:image/png;base64,{encoded_image}"


# ===== Behind the scenes: send the text to the LLM, get a command back =====
def text_to_command(user_text):
    if not user_text or not user_text.strip():
        return ""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return response.choices[0].message.content.strip()


# ===== Design =====
CSS = r"""
/* ----- Theme ----- */
:root {
    color-scheme: dark;
    --body-background-fill: #080510;
    --background-fill-primary: rgba(8, 5, 17, .94);
    --background-fill-secondary: rgba(20, 12, 34, .88);
    --block-background-fill: rgba(15, 9, 27, .78);
    --block-border-color: rgba(194, 105, 255, .38);
    --input-background-fill: rgba(9, 6, 18, .94);
    --body-text-color: #f7efff;
    --body-text-color-subdued: #b9a8cc;
}

html, body {
    min-height: 100%;
    margin: 0 !important;
    background: #080510 !important;
}

/* Background image behind the whole page */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(5, 2, 13, .12), rgba(5, 2, 13, .28)),
        url("__FRAME_IMAGE__");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 100% 100%;
}

.gradio-container {
    position: relative !important;
    z-index: 1 !important;
    direction: rtl !important;
    width: 100% !important;
    max-width: 900px !important;
    min-height: 100vh !important;
    margin: 0 auto !important;
    padding: 20px 24px 45px !important;
    box-sizing: border-box !important;
    background: transparent !important;
    color: #f7efff !important;
    font-family: "Segoe UI", Tahoma, Arial, sans-serif !important;
}

.gradio-container .main,
.gradio-container .wrap,
.gradio-container .contain,
.gradio-container .form,
.gradio-container .block {
    background-color: transparent !important;
}
footer, .built-with { display: none !important; }

/* ----- Header ----- */
#hero {
    direction: ltr;
    text-align: center;
    padding: 26px 10px 24px;
}
#hero h1 {
    margin: 0;
    color: #fff;
    font-size: clamp(40px, 7vw, 64px);
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: 3px;
    text-shadow: 0 0 7px rgba(255, 255, 255, .75),
                 0 0 17px rgba(211, 89, 255, .95),
                 0 0 38px rgba(177, 40, 255, .8);
}
#hero .subtitle {
    direction: rtl;
    color: #ead8ff;
    font-size: 16px;
    margin-top: 12px;
    text-shadow: 0 0 12px rgba(190, 70, 255, .55);
}

/* ----- Main glass panel ----- */
#card {
    background: rgba(10, 6, 20, .78) !important;
    border: 1px solid rgba(190, 120, 255, .25) !important;
    border-radius: 22px !important;
    padding: 26px !important;
    box-shadow: 0 12px 45px rgba(0, 0, 0, .34) !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}
#card .block,
#card .form,
#card .wrap {
    border-color: transparent !important;
    box-shadow: none !important;
}

/* ----- Input ----- */
#user-input, #user-input > div { background: transparent !important; }
#user-input textarea {
    direction: rtl !important;
    text-align: right !important;
    color: #fff !important;
    background: linear-gradient(145deg, rgba(8, 5, 17, .98), rgba(27, 15, 43, .97)) !important;
    border: 1px solid rgba(196, 119, 255, .75) !important;
    border-radius: 17px !important;
    min-height: 112px !important;
    padding: 17px 19px !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
    box-shadow: inset 0 3px 16px rgba(0, 0, 0, .52),
                0 0 13px rgba(176, 70, 255, .16) !important;
}
#user-input textarea::placeholder { color: #b9a8cc !important; opacity: 1 !important; }
#user-input textarea:focus {
    border-color: #dc83ff !important;
    box-shadow: 0 0 0 2px rgba(194, 83, 255, .16),
                0 0 22px rgba(190, 65, 255, .38),
                inset 0 0 14px rgba(145, 55, 220, .13) !important;
}

/* ----- Buttons ----- */
#buttons-row { gap: 13px !important; margin: 20px 0 23px !important; }
#buttons-row,
#buttons-row > div,
#run-btn,
#clear-btn {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

.gradio-container #run-btn button,
.gradio-container #clear-btn button {
    appearance: none !important;
    min-height: 58px !important;
    border-radius: 16px !important;
    font-size: 16px !important;
    transition: all .2s ease !important;
}

/* Main button: 3D purple glass */
.gradio-container #run-btn button {
    color: #fff !important;
    font-weight: 750 !important;
    background: linear-gradient(180deg, #dc82ff 0%, #ad3cec 25%, #7924c6 75%, #4e167e 100%) !important;
    border: 1px solid rgba(239, 202, 255, .9) !important;
    box-shadow:
        0 7px 0 rgba(42, 12, 67, .95),
        0 10px 22px rgba(150, 44, 230, .4),
        0 0 20px rgba(195, 75, 255, .4),
        inset 0 2px 3px rgba(255, 255, 255, .55),
        inset 0 -7px 12px rgba(35, 0, 62, .4) !important;
    text-shadow: 0 1px 7px rgba(35, 0, 55, .55) !important;
}
.gradio-container #run-btn button:hover {
    filter: brightness(1.15) !important;
    transform: translateY(-2px) !important;
}

/* Clear button: dark glass */
.gradio-container #clear-btn button {
    color: #eee2ff !important;
    font-weight: 700 !important;
    background: linear-gradient(160deg, #4f4169, #251b37 55%, #0d0a18) !important;
    border: 1px solid rgba(177, 151, 211, .58) !important;
    box-shadow:
        0 7px 0 rgba(5, 3, 12, .95),
        0 10px 18px rgba(0, 0, 0, .32),
        inset 0 2px 3px rgba(255, 255, 255, .22),
        inset 0 -7px 12px rgba(0, 0, 0, .42) !important;
}
.gradio-container #clear-btn button:hover {
    filter: brightness(1.18) !important;
    transform: translateY(-2px) !important;
}

/* ----- Terminal (command output) ----- */
#cmd, #cmd > div { direction: ltr !important; text-align: left !important; }
#cmd label, #cmd label span {
    color: #ead8ff !important;
    font-size: 13px !important;
    letter-spacing: .5px;
}

#cmd,
#cmd > div,
#cmd .wrap,
#cmd .code-wrap,
#cmd .code-container,
#cmd .cm-editor,
#cmd .cm-scroller,
#cmd pre {
    background: rgba(7, 4, 16, .96) !important;
    color: #f3e5ff !important;
}
#cmd .code-wrap,
#cmd .code-container {
    border: 1px solid rgba(170, 104, 224, .42) !important;
    border-radius: 14px !important;
    box-shadow: 0 0 12px rgba(151, 54, 255, .12) !important;
}
#cmd .cm-editor,
#cmd .cm-scroller,
#cmd pre {
    border-radius: 14px !important;
    font-family: Consolas, "Courier New", monospace !important;
}
#cmd pre {
    border: none !important;
    padding: 16px !important;
    text-shadow: 0 0 7px rgba(204, 115, 255, .24);
}

/* ----- Small screens ----- */
@media (max-width: 650px) {
    .gradio-container { padding: 12px 12px 30px !important; }
    #hero { padding-top: 22px; }
    #card { padding: 17px !important; }
    #buttons-row { gap: 8px !important; }
    .gradio-container #run-btn button,
    .gradio-container #clear-btn button {
        min-height: 52px !important;
        padding: 0 14px !important;
        font-size: 14px !important;
        border-radius: 14px !important;
    }
}
"""
CSS = CSS.replace("__FRAME_IMAGE__", FRAME_BACKGROUND)


# ===== The UI: one input box, one output box =====
with gr.Blocks(title="CLI Agent") as demo:
    gr.HTML("""
        <div id="hero">
            <h1>CLI AGENT</h1>
            <div class="subtitle">
                תארי בשפה טבעית את הפעולה, וקבלי פקודת CMD מוכנה להרצה
            </div>
        </div>
    """)

    with gr.Group(elem_id="card"):
        user_input = gr.Textbox(
            placeholder="מה תרצי לעשות? למשל: הצג את כל קובצי ה-log בתיקייה",
            lines=3,
            rtl=True,
            show_label=False,
            elem_id="user-input",
        )

        with gr.Row(elem_id="buttons-row"):
            run_btn = gr.Button("✦  חולל פקודה", variant="primary", elem_id="run-btn", scale=4)
            clear_btn = gr.Button("ניקוי", variant="secondary", elem_id="clear-btn", scale=1)

        output = gr.Code(
            label="CLI TERMINAL",
            language="shell",
            interactive=False,
            elem_id="cmd",
        )

    run_btn.click(text_to_command, inputs=user_input, outputs=output)
    user_input.submit(text_to_command, inputs=user_input, outputs=output)
    clear_btn.click(lambda: ("", ""), outputs=[user_input, output])


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Base(), css=CSS, show_error=True)