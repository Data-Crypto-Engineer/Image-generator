import base64
import io
import requests
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Cloudflare FLUX Test", page_icon="🖼️")
st.title("Cloudflare Workers AI — FLUX.1 Schnell Test")

st.write("This app sends one text-to-image request to Cloudflare Workers AI.")

# Secrets are stored in Streamlit, not in this source code.
try:
    account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
except Exception:
    st.error(
        "Missing Streamlit Secrets. Add CLOUDFLARE_ACCOUNT_ID and "
        "CLOUDFLARE_API_TOKEN in your app's Secrets settings."
    )
    st.stop()

prompt = st.text_area(
    "Image prompt",
    value="A peaceful cinematic mountain valley at sunrise, soft mist, "
          "natural realistic photography, wide composition, 16:9 feeling",
    height=120,
)

steps = st.slider("Steps", min_value=1, max_value=8, value=4)

if st.button("Generate test image", type="primary"):
    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    )

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt,
        "steps": steps,
    }

    with st.spinner("Generating image..."):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=120,
            )
        except requests.RequestException as e:
            st.error(f"Network request failed: {e}")
            st.stop()

    if not response.ok:
        st.error(f"Cloudflare HTTP {response.status_code}")
        try:
            st.json(response.json())
        except Exception:
            st.code(response.text)
        st.stop()

    try:
        data = response.json()
    except ValueError:
        st.error("Cloudflare returned a non-JSON response.")
        st.code(response.text[:2000])
        st.stop()

    if not data.get("success", False):
        st.error("Cloudflare reported that the request failed.")
        st.json(data)
        st.stop()

    # FLUX.1 Schnell returns the generated image as Base64.
    image_b64 = data.get("result", {}).get("image")

    if not image_b64:
        st.error("Request succeeded, but no image was found in result.image.")
        st.json(data)
        st.stop()

    try:
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        st.error(f"Could not decode the generated image: {e}")
        st.stop()

    st.success("Success — Cloudflare generated the image.")
    st.image(image, caption="FLUX.1 Schnell result", use_container_width=True)

    st.download_button(
        "Download image",
        data=image_bytes,
        file_name="cloudflare_flux_test.jpg",
        mime="image/jpeg",
    )

st.caption(
    "Model: @cf/black-forest-labs/flux-1-schnell. "
    "Do not put your API token directly in this file."
)
