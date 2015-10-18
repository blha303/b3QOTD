#!/usr/bin/env python2
from flask import Flask, request, render_template, redirect, url_for, flash
from config import SECRET_KEY

from subprocess import check_output

def get_git_describe():
    tag = check_output(["git", "describe", "--tags"]).strip()
    return tag

f = Flask(__name__)
f.debug = False
f.secret_key = SECRET_KEY
f.jinja_env.globals.update(info=get_git_describe)

def get_quotes():
    with open("quotes.txt") as f:
        return [u"\n{}\n\n".format(a.strip()) for a in f.read().split(u"\n\n")]

def add_quote(text):
    try:
        if len(text) > 4000:
            raise Exception("Message longer than 50 lines (80 chars per line)")
        if len(text) < 10:
            raise Exception("Message shorter than 10 chars, not adding")
        o = []
        while text > 80:
            if text[0] != u"<" or text[0] != u" ":
                raise Exception("Each line must start with either a <username>, or spaces for indentation")
            o.append(text[:81])
            text = text[81:]
        o.append(text)
        with open("quotes.txt", "a") as f:
            f.write(u"\n\n" + u"\n".join(text))
        return True, None
    except Exception, e:
        return False, e

def delete_quote(index):
    quotes = get_quotes()
    try:
        return quotes.pop(int(index)), None
    except Exception, e:
        return None, e
    finally:
        with open("quotes.txt", "w") as f:
            f.write(u"\n\n".join([a.strip() for a in quotes]))

@f.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def index():
    if request.method == "GET":
        return render_template("index.html", quotes=enumerate(get_quotes()))
    elif request.method in ["PUT", "POST", "DELETE"]:
        method = request.form["_method"] if "_method" in request.form else request.method
        if method in ["PUT", "POST"]:
            print(method, request.form)
            success, e = add_quote(request.form["quote"])
            if success:
                flash("Quote added")
            else:
                flash("Quote not added: {}".format(e.message))
            return redirect(url_for('index'))
        elif method == "DELETE":
            print(method, request.form)
            quote, e = delete_quote(request.form["index"])
            if quote:
                flash("Quote removed")
            elif e:
                flash("Quote not removed: {}".format(e.message))
            return redirect(url_for('index'))

if __name__ == "__main__":
    f.run(port=57432)
