from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIG

CLIENT_ID = "859133170533640"
CLIENT_SECRET = "8d1841ce06b83bd51ff2f9a2fcf0735f"
REDIRECT_URI = "https://8e306486-9691-46dd-a826-0c081e5ea1a0-00-2qmudc6ii8xcv.sisko.replit.dev/auth/instagram/callback"

VERIFY_TOKEN = "test"


# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {"message": "Instagram Business OAuth Running"}


# -----------------------------
# STEP 1: LOGIN URL
# -----------------------------
@app.get("/auth/instagram/login")
def instagram_login():
    scope = ",".join([
        "instagram_business_basic",
        "instagram_manage_comments",
        "instagram_business_manage_messages",
        "pages_show_list",
        "business_management",
        "instagram_business_manage_insights"
    ])

    auth_url = (
        "https://www.instagram.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        f"&scope={scope}"
    )

    return {"auth_url": auth_url}


# -----------------------------
# STEP 2: CALLBACK
# -----------------------------
@app.get("/auth/instagram/callback")
def instagram_callback(code: str = None, error: str = None):

    if error:
        raise HTTPException(400, f"Instagram error: {error}")

    if not code:
        print("No code received")
    else:
        print(code)

    #step2
    token_res = requests.post(
        "https://api.instagram.com/oauth/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    print("STATUS:", token_res.status_code)
    print("RESPONSE:", token_res.text)

    if token_res.status_code != 200:
        raise HTTPException(400, token_res.text)

    access_token = token_res.json().get("access_token")

    if not access_token:
        raise HTTPException(400, "No access token")

    # STEP 2 get long lived access token
    url = "https://graph.instagram.com/access_token"

    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": CLIENT_SECRET,
        "access_token": access_token
    }

    response = requests.get(url, params=params)

    print("STATUS long token:", response.status_code)
    print("RESPONSE long token:", response.text)

    long_access = response.json().get("access_token")

    


# -----------------------------
# WEBHOOK VERIFY
# -----------------------------
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    raise HTTPException(403, "Verification failed")


# -----------------------------
# WEBHOOK RECEIVE
# -----------------------------
@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("Webhook Event:", body)
    return {"status": "ok"}


"""# STEP 3 — Get Instagram Business Account
    ig_res = requests.get(
        f"https://graph.facebook.com/v19.0/{page_id}",
        params={
            "fields": "instagram_business_account",
            "access_token": access_token,
        }
    )

    ig_data = ig_res.json()
    ig_id = ig_data.get("instagram_business_account", {}).get("id")

    if not ig_id:
        raise HTTPException(400, "No Instagram business account linked")

    # STEP 4 — Get Instagram Username
    user_res = requests.get(
        f"https://graph.facebook.com/v19.0/{ig_id}",
        params={
            "fields": "id,username",
            "access_token": access_token,
        }
    )

    ig_user = user_res.json()

    username = ig_user.get("username")

    # OPTIONAL: redirect back to frontend
    return RedirectResponse(
        url=f"https://YOUR-FRONTEND-URL?username={username}"
    )

    # OR return JSON:
    # return {"username": username}"""