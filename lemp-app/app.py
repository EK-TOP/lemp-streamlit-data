from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <style>
                body {
                    background-color: black;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .message {
                    color: white;
                    font-size: 48px;
                    font-weight: bold;
                    text-align: center;
                }
                a {
                    color: #00aaff;
                    text-decoration: none;
                    font-size: 32px;
                    display: block;
                    margin-top: 20px;
                }
                a:hover {
                    color: #66d0ff;
                }
            </style>
        </head>
        <body>
            <div class="message">
                TURHAA DATAA – KLIKKAA LINKKIÄ
                <br>
                <a href="/data-analysis">SIIRRY DATA-ANALYYSIIN</a>
            </div>
        </body>
    </html>
    """
