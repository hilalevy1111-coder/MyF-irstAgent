import os
import base64
from pathlib import Path

from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# Paths and environment
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = os.getenv("MODEL")
if not MODEL:
    raise ValueError("MODEL is missing from your .env file.")

PROMPT_PATH = BASE_DIR / "prompts" / "v1.md"
if not PROMPT_PATH.exists():
    raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
with PROMPT_PATH.open(encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Load the frame image. Keep cyber-frame.png in the project's images folder.
FRAME_PATH = BASE_DIR / "images" / "cyber-frame.png"
if not FRAME_PATH.exists():
    raise FileNotFoundError(
        "Background image not found: put cyber-frame.png inside the images folder."
    )
encoded_image = base64.b64encode(FRAME_PATH.read_bytes()).decode("ascii")
FRAME_BACKGROUND = f"data:image/png;base64,{encoded_image}"

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


CSS = r"""
:root {
    color-scheme: dark;
    --body-background-fill: #080510;
    --background-fill-primary: rgba(8, 5, 17, .94);
    --background-fill-secondary: rgba(20, 12, 34, .88);
    --block-background-fill: rgba(15, 9, 27, .78);
    --block-border-color: rgba(194, 105, 255, .38);
    --input-background-fill: rgba(9, 6, 18, .94);
    --button-primary-background-fill: linear-gradient(135deg, #a92cf0, #7020bd 55%, #c13cff);
    --button-primary-background-fill-hover: linear-gradient(135deg, #c34cff, #8d2bd9 55%, #dc62ff);
    --button-primary-text-color: #fff;
    --button-secondary-background-fill: rgba(38, 25, 57, .94);
    --button-secondary-background-fill-hover: rgba(76, 43, 105, .98);
    --button-secondary-text-color: #f2e5ff;
    --body-text-color: #f7efff;
    --body-text-color-subdued: #b9a8cc;
}

html, body {
    min-height: 100%;
    margin: 0 !important;
    background: #080510 !important;
}

/* Put the actual supplied image behind the entire page. */
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

/* Header */
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
    text-shadow: 0 0 7px rgba(255,255,255,.75),
                 0 0 17px rgba(211,89,255,.95),
                 0 0 38px rgba(177,40,255,.8);
}
#hero .subtitle {
    direction: rtl;
    color: #ead8ff;
    font-size: 16px;
    margin-top: 12px;
    text-shadow: 0 0 12px rgba(190,70,255,.55);
}

/* Main glass panel */
#card {
    background: linear-gradient(145deg, rgba(29,17,48,.88), rgba(8,5,18,.91)) !important;
    border: 1px solid rgba(211,145,255,.72) !important;
    border-radius: 24px !important;
    padding: 24px !important;
    box-shadow: 0 0 14px rgba(190,62,255,.30),
                0 0 38px rgba(145,42,255,.20),
                inset 0 1px 1px rgba(255,255,255,.16),
                inset 0 0 28px rgba(138,54,190,.10) !important;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

/* Input */
#user-input, #user-input > div { background: transparent !important; }
#user-input textarea {
    direction: rtl !important;
    text-align: right !important;
    color: #fff !important;
    background: linear-gradient(145deg, rgba(8,5,17,.98), rgba(27,15,43,.97)) !important;
    border: 1px solid rgba(196,119,255,.75) !important;
    border-radius: 17px !important;
    min-height: 112px !important;
    padding: 17px 19px !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
    box-shadow: inset 0 3px 16px rgba(0,0,0,.52),
                0 0 13px rgba(176,70,255,.16) !important;
}
#user-input textarea::placeholder { color: #b9a8cc !important; opacity: 1 !important; }
#user-input textarea:focus {
    border-color: #dc83ff !important;
    box-shadow: 0 0 0 2px rgba(194,83,255,.16),
                0 0 22px rgba(190,65,255,.38),
                inset 0 0 14px rgba(145,55,220,.13) !important;
}

/* Buttons */
#buttons-row { gap: 13px !important; margin: 20px 0 23px !important; background: transparent !important; }
#run-btn, #clear-btn { background: transparent !important; }
#run-btn button, #clear-btn button {
    min-height: 54px !important;
    border-radius: 14px !important;
    font-size: 16px !important;
    font-weight: 750 !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}

/* Primary button: purple luminous glass */
#run-btn button, #run-btn button.primary {
    color: #fff !important;
    background: linear-gradient(135deg, #b83cf4 0%, #8126cb 52%, #c94bff 100%) !important;
    background-color: #922bd7 !important;
    border: 1px solid rgba(244,205,255,.9) !important;
    box-shadow: 0 5px 18px rgba(160,48,255,.40),
                0 0 21px rgba(192,68,255,.43),
                inset 0 1px 2px rgba(255,255,255,.48),
                inset 0 -5px 12px rgba(45,0,90,.25) !important;
    text-shadow: 0 1px 7px rgba(35,0,55,.55) !important;
}
#run-btn button:hover, #run-btn button.primary:hover {
    filter: brightness(1.14) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 25px rgba(178,54,255,.52),
                0 0 28px rgba(206,85,255,.58),
                inset 0 1px 2px rgba(255,255,255,.5) !important;
}

/* Secondary button: smoked-purple glass */
#clear-btn button, #clear-btn button.secondary {
    color: #ead9ff !important;
    background: linear-gradient(145deg, rgba(67,48,91,.94), rgba(20,13,34,.98)) !important;
    background-color: #241633 !important;
    border: 1px solid rgba(190,145,226,.58) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,.30),
                inset 0 1px 1px rgba(255,255,255,.19) !important;
}
#clear-btn button:hover, #clear-btn button.secondary:hover {
    color: #fff !important;
    border-color: rgba(220,155,255,.9) !important;
    box-shadow: 0 0 19px rgba(175,76,255,.36) !important;
    transform: translateY(-2px) !important;
}

/* Terminal */
#cmd, #cmd > div { direction: ltr !important; text-align: left !important; background: transparent !important; }
#cmd label, #cmd label span { color: #ead8ff !important; font-size: 13px !important; letter-spacing: .5px; }
#cmd .code-wrap, #cmd .code-container, #cmd .cm-editor, #cmd .cm-scroller, #cmd pre {
    color: #f1dfff !important;
    background: rgba(6,4,15,.97) !important;
    border-color: rgba(174,92,255,.62) !important;
    border-radius: 14px !important;
    font-family: Consolas, "Courier New", monospace !important;
}
#cmd .code-wrap, #cmd .code-container {
    border: 1px solid rgba(174,92,255,.62) !important;
    box-shadow: inset 0 0 22px rgba(120,35,180,.15),
                0 0 16px rgba(151,54,255,.20) !important;
}
#cmd pre { padding: 16px !important; text-shadow: 0 0 7px rgba(204,115,255,.24); }

@media (max-width: 650px) {
    .gradio-container { padding: 12px 12px 30px !important; }
    #hero { padding-top: 22px; }
    #card { padding: 16px !important; border-radius: 19px !important; }
    #buttons-row { gap: 8px !important; }
    #run-btn button, #clear-btn button { min-height: 50px !important; font-size: 14px !important; }
}
"""
CSS = CSS.replace("__FRAME_IMAGE__", FRAME_BACKGROUND)


with gr.Blocks(title="CLI Agent", theme=gr.themes.Base()) as demo:
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
            placeholder="מה תרצי לעשות? למשל: מצא את כל קובצי ה-log ומחק אותם",
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
    demo.launch(css=CSS, show_error=True)
