#!/usr/bin/env python2
import flask

f = flask.Flask(__name__)
f.debug = False

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
        return flask.render_template("index.html", quotes=enumerate(get_quotes()))
    elif flask.request.method in ["PUT", "POST", "DELETE"]:
        method = flask.request.form["_method"] if "_method" in flask.request.form else flask.request.method
        if method in ["PUT", "POST"]:
            print(method, flask.request.form)
            return "Not yet implemented"
        elif method == "DELETE":
            print(method, flask.request.form)
            return "Not yet implemented"

if __name__ == "__main__":
    f.run(port=57432)
