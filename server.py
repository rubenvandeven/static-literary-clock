# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import datetime, time
import json
import random
from dataclasses import dataclass

hostName = ""
serverPort = 8080

json_dir = Path("./literature-clock/docs/times/")


@dataclass
class Quote:
    time: str
    quote_first: str
    quote_time_case: str
    quote_last: str
    title: str
    author: str
    sfw: bool


def validate_dir(json_dir):
    for h in range(24):
        for m in range(60):
            fname = json_dir / f"{h:02d}_{m:02d}.json"
            
            if not fname.exists():
                print(f"No file for {h:02d}_{m:02d}")

def parse_template(quote: Quote, delay = 60) -> str:
    return f"""
    <html>
    <head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
    <meta content="utf-8" http-equiv="encoding">
    <meta http-equiv="refresh" content="{delay}">
    <style type="text/css">
    body{{
        font-family: sans-serif;
        padding: 3em;
        font-size: 35pt;
        background: black;
        color: white
    }}
    blockquote{{
        color: lightgray;
        font-weight: light;
    }}
    strong{{
        color: white;
        text-decoration: underline;
        font-weight: bold;
    }}
    figcaption{{
        color: gray;
        font-size: 25pt;
    }}
    </style>
    </head>
    <body>
    <figure>
        <blockquote>{quote.quote_first}<strong>{quote.quote_time_case}</strong>{quote.quote_last}
        </blockquote>
        <figcaption>
        <span class='title'>{quote.title}</span>
        <span class='dash'>&mdash;</span>
        <span class='author'>{quote.author}</span>
        </figcaption>
    </figure>


    </body>
    </html>
    """

class LiteratureRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        now = datetime.datetime.now()
        # now = datetime.datetime(2024,12,12,21,31)
        
        fname = json_dir / f"{now.hour:02d}_{now.minute:02d}.json"

        # reload as close to the minute mark as possible.
        
        diff = max(1, 60 - now.second)
        
        print(self.client_address, fname, fname.exists(), diff)
        
        if not fname.exists():
            # TODO: handle better
            quote = Quote("","", f"{now.hour}:{now.minute}", "", "", "", True)
        else:
            with fname.open('r') as fp:
                options = json.load(fp)
            # dict with: time, quote_first, quote_time_case, quote_last, title, author, sfw
            kwargs = random.choice(options)
            quote = Quote(**kwargs)
        output = parse_template(quote, diff)
        
        self.wfile.write(bytes(output, "utf-8"))


def serve():
    validate_dir(json_dir)

    webServer = HTTPServer((hostName, serverPort), LiteratureRequestHandler)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    serve()