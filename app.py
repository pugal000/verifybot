from flask import Flask, request
import instaloader
import random, string

app = Flask(__name__)
L = instaloader.Instaloader()

user_codes = {}

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/generate/<discord_id>")
def generate(discord_id):
    code = generate_code()
    user_codes[discord_id] = code
    return {"code": code}

@app.route("/verify", methods=["POST"])
def verify():
    data = request.json
    username = data["username"]
    discord_id = data["discord_id"]

    if discord_id not in user_codes:
        return {"status": "error"}

    code = user_codes[discord_id]

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        bio = profile.biography

        if code in bio:
            return {"status": "success"}
        else:
            return {"status": "fail"}
    except:
        return {"status": "error"}

app.run(host="0.0.0.0", port=3000)
