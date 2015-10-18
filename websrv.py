#!/usr/bin/env python2
import flask

f = flask.Flask(__name__)

def get_quotes():
    with open("quotes.txt") as f:
        return ["\n{}\n\n".format(a.strip()) for a in f.read().split("\n\n")]

def add_quote(text):
    try:
        o = []
        while text > 80:
            o.append(text[:81])
            text = text[81:]
        o.append(text)
        with open("quotes.txt", "a") as f:
            f.write("\n\n" + "\n".join(text))
        return True, None
    except Exception, e:
        return False, e

def delete_quote(index):
    quotes = get_quotes()
    try:
        return quotes.pop(index)
    except Exception, e:
        return None, e
    finally:
        with open("quotes.txt", "w") as f:
            f.write("\n\n".join([a.strip() for a in quotes]))

@f.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index():
    if flask.request.method == "GET":
        return flask.render_template("index.html", quotes=enumerate(quotes))
    elif flask.request.method in ["PUT", "POST"]:
        return "Not yet implemented"
    elif flask.request.method in ["DELETE"]:
        return "Not yet implemented"

if __name__ == "__main__":
    f.run(port=57432)
