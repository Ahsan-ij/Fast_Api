from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import openai

app = FastAPI()


openai.api_key = ""  
form_template = """
<!DOCTYPE html>
<html>
    <head>
        <title> Question Generation</title>
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
                width: 300px;
                padding: 20px;
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
            textarea {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                resize: none;
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
            <h2>Generate Questions and Answers</h2>
        </div>
        <div class="form-container">
            <form action="/get_answers" method="post">
                <label for="input_text">Enter your paragraph:</label><br>
                <textarea id="input_text" name="input_text" rows="4" placeholder="Type your paragraph here" required></textarea><br>
                <input type="submit" value="Get Answers">
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

@app.post("/get_answers", response_class=HTMLResponse)
async def get_answers(input_text: str = Form(...)):
    completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that generates questions and answers from a given paragraph."},
            {"role": "user", "content": f"Generate questions and answers from the following paragraph:\n\n{input_text}"}
            ],
            max_tokens=200
        )
    response_message = completion.choices[0].message.content
    return form_template.format(output_text=response_message)


