from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import openai

app = FastAPI()


openai.api_key = ""


form_template = """
<!DOCTYPE html>
<html>
    <head>
        <title>OpenAI Question Form</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }}
            body, html {{
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background-color: #f4f4f9;
            }}
            .heading-container {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .form-container {{
                text-align: center;
                width: 700px;
                padding: 40px;
                border-radius: 8px;
                background: #ffffff;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }}
            h2 {{
                font-size: 24px;
                color: #333;
            }}
            label {{
                font-size: 14px;
                color: #333;
            }}
            input[type="text"] {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            input[type="submit"] {{
                width: 100%;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
            .output-box {{
                margin-top: 20px;
                padding: 15px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 4px;
                color: #555;
                min-height: 50px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="heading-container">
            <h2>Ask OpenAI</h2>
        </div>
        <div class="form-container">
            <form action="/get_answer" method="get">
                <label for="input_text">Enter your question:</label><br>
                <input type="text" id="input_text" name="input_text" placeholder="Type your question here" required><br><br>
                <input type="submit" value="Get Answer">
            </form>
            <div class="output-box">
                <p>{output_text}</p>
            </div>
        </div>
    </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return form_template.format(output_text="")


@app.get("/get_answer", response_class=HTMLResponse)
async def get_answer(input_text: str = Query(...)):
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": input_text}],
        max_tokens=100
        )
    response_message = completion.choices[0].message.content
    return form_template.format(output_text=response_message)


