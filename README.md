# Cloudflare FLUX.1 Schnell + Streamlit test

## Streamlit Secrets

In your Streamlit app's Secrets settings, add:

```toml
CLOUDFLARE_ACCOUNT_ID = "YOUR_ACCOUNT_ID"
CLOUDFLARE_API_TOKEN = "YOUR_WORKERS_AI_API_TOKEN"
```

Do NOT put the real token in `app.py` or commit it to GitHub.

The Cloudflare token should have Workers AI permissions as required by Cloudflare.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or deploy the repository to Streamlit Community Cloud and set the same secrets there.

The app calls:

`@cf/black-forest-labs/flux-1-schnell`

through the Cloudflare Workers AI REST API and displays the generated image.
