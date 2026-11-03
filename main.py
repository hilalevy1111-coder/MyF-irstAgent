import os
from dotenv import load_dotenv
import gradio as gr
from openai import OpenAI

# 1. Load the secret key from .env
load_dotenv()

# 2. Connect to Gemini through the OpenAI library
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
MODEL = os.getenv("MODEL")

# 3. Read the prompt from its file
with open("prompts/v1.md", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 4. Behind the scenes: send the text to the LLM, get a command back
def text_to_command(user_text):
    if not user_text.strip():
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

# 5. The UI: Cyberpunk Neon Design 
CSS = """
/* רקע סייברפאנק עם רשת ניאון עדינה */
body, .gradio-container { 
    background-color: #07030e !important; 
    background-image: 
        linear-gradient(rgba(180, 50, 255, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(180, 50, 255, 0.07) 1px, transparent 1px) !important;
    background-size: 30px 30px !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

.gradio-container { direction: rtl; max-width: 780px !important; margin: 0 auto !important; }

/* העלמת כל המסגרות הלבנות והרקעים המכוערים של Gradio */
.block { 
    border: none !important; 
    background: transparent !important; 
    box-shadow: none !important; 
}

/* כותרת מרכזית מאירה */
#hero { text-align: center; padding: 40px 0 20px; direction: ltr; }
#hero h1 { 
    font-size: 64px; font-weight: 900; margin: 0 0 10px;
    color: #ffffff;
    text-shadow: 0 0 10px #df00ff, 0 0 20px #df00ff, 0 0 40px #df00ff;
    letter-spacing: 2px;
}
#hero p { color: #00ffff; font-size: 18px; text-shadow: 0 0 8px rgba(0, 255, 255, 0.6); margin: 0; }

/* הקופסה החיצונית - מסגרת ניאון סגולה בדיוק כמו ברפרנס */
#card {
    background: rgba(10, 0, 20, 0.8) !important;
    border: 2px solid #df00ff !important;
    border-radius: 20px !important;
    padding: 30px !important;
    box-shadow: 0 0 15px #df00ff, inset 0 0 15px rgba(223, 0, 255, 0.5) !important;
    margin-top: 15px;
}

/* תיבת הקלט */
#user-input textarea { 
    background: rgba(0, 0, 0, 0.7) !important; 
    border: 1px solid #00ffff !important;
    border-radius: 10px !important; 
    color: #ffffff !important;
    font-size: 16px !important;
    padding: 16px !important;
    box-shadow: inset 0 0 12px rgba(0, 255, 255, 0.2) !important;
    transition: all 0.3s;
}
#user-input textarea:focus {
    border: 1px solid #00ffff !important;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.6), inset 0 0 10px rgba(0, 255, 255, 0.3) !important;
}
#user-input label span { display: none !important; } /* הסתרת הכותרת הקטנה של התיבה */

#buttons-row { margin: 25px 0; gap: 15px; }

/* כפתור הפעלה - סגנון סייברפאנק עם הילה סגולה */
#run-btn { 
    background: #000000 !important;
    border: 2px solid #df00ff !important;
    color: #df00ff !important;
    font-weight: 800 !important; 
    font-size: 18px !important;
    border-radius: 10px !important;
    height: 55px !important;
    text-shadow: 0 0 8px #df00ff;
    box-shadow: 0 0 15px rgba(223, 0, 255, 0.4), inset 0 0 10px rgba(223, 0, 255, 0.4) !important;
    transition: all 0.2s;
}
#run-btn:hover { 
    background: #df00ff !important; 
    color: #000000 !important; 
    box-shadow: 0 0 25px #df00ff, inset 0 0 10px #df00ff !important;
    text-shadow: none;
    transform: scale(1.02);
}

/* כפתור ניקוי - מסגרת תכלת זוהרת */
#clear-btn { 
    background: #000000 !important;
    border: 1px solid #00ffff !important;
    color: #00ffff !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    text-shadow: 0 0 5px #00ffff;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.2) !important;
}
#clear-btn:hover { 
    background: #00ffff !important; 
    color: #000000 !important; 
    text-shadow: none; 
}

/* פלט ה-CLI - מסך האקרים ירוק */
#cmd, #cmd * { direction: ltr !important; text-align: left !important; font-family: Consolas, monospace !important; }
#cmd .code-wrap { 
    background: #000000 !important; 
    border: 1px solid #00ff00 !important; 
    border-radius: 10px !important;
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.2), inset 0 0 10px rgba(0, 255, 0, 0.1) !important;
    padding: 10px !important;
}
#cmd .code-wrap pre { color: #00ff00 !important; text-shadow: 0 0 4px #00ff00; }
#cmd label span { color: #00ff00 !important; text-shadow: 0 0 5px #00ff00; font-size: 13px !important;}

footer { display: none !important; }
"""

# שימי לב: הסרנו את נושא ה-theme וה-css מ-gr.Blocks כדי להתאים לגרסה 6.0 של Gradio!
with gr.Blocks(title="AI CLI Agent") as demo:
    gr.HTML("""
        <div id="hero">
            <h1>CLI Agent</h1>
            <p>תארי בשפה טבעית את הפעולה, וקבלי פקודת CMD מוכנה להרצה</p>
        </div>
    """)

    # כאן הגדרנו מחדש את ה-Group כולל הכפתורים
    with gr.Group(elem_id="card"):
        user_input = gr.Textbox(
            placeholder="מה תרצי לעשות? (לדוגמה: מצא את כל קובצי ה-log ומחק אותם)",
            lines=2,
            rtl=True,
            elem_id="user-input"
        )
        
        with gr.Row(elem_id="buttons-row"):
            run_btn = gr.Button("🚀 חולל פקודה", variant="primary", elem_id="run-btn", scale=4)
            clear_btn = gr.Button("ניקוי", variant="secondary", elem_id="clear-btn", scale=1)
            
        output = gr.Code(
            label="CLI Terminal Output",
            language="shell",
            interactive=False,
            elem_id="cmd",
        )

    # החיבורים ללוגיקה
    run_btn.click(text_to_command, inputs=user_input, outputs=output)
    user_input.submit(text_to_command, inputs=user_input, outputs=output)
    clear_btn.click(lambda: ("", ""), outputs=[user_input, output])

# כאן קוראים ל-CSS כדי שזה יעבוד בלי שגיאות (כמו שראינו קודם)
demo.launch(css=CSS, show_error=True)