import json

import pandas as pd
import streamlit as st

from connection import StreamPetConnection


@st.cache_data
def get_breeds(pet):
    with open("breeds.json") as f:
        breeds = json.load(f)
    return breeds[pet]


if __name__ == "__main__":
    page_title = "🐶StreamPet🐱"
    st.set_page_config(page_title=page_title, page_icon="🐶", layout="wide")
    st.markdown(
        f'<h1 style="text-align: center;">{page_title}</h1><br>', unsafe_allow_html=True
    )

    pet = st.sidebar.radio("Choose Pet:", options=["🐶", "🐱"], horizontal=True)
    pet = "cat" if pet == "🐱" else "dog"
    breeds = get_breeds(pet)
    limit = st.sidebar.slider("Choose Count:", min_value=5, max_value=100, step=10)
    selected_breeds = st.sidebar.multiselect(
        "Choose Breed:", options=breeds, default=list(breeds)[:3]
    )

    conn = st.experimental_connection("StreamPet", type=StreamPetConnection, pet=pet)
    api_key = st.secrets[f"{pet}_api_key"]
    params = {
        "limit": limit,
        "has_breeds": 1,
        "breed_ids": ",".join(
            str(v) for k, v in breeds.items() if k in selected_breeds
        ),
        "api_key": api_key,
    }
    url = f"https://api.the{pet}api.com/v1/images/search"

    response = conn.query(url, params=params, ttl=60 * 60)
    for index, pet in enumerate(response.json()):
        c1, c2, c3 = st.columns([0.5, 4, 3])
        breeds = pet["breeds"][0]
        c1.code(index + 1)
        c2.image(caption=breeds["name"], image=pet["url"], use_column_width=True)
        del breeds["id"]
        del breeds["name"]
        del breeds["reference_image_id"]
        df = pd.json_normalize(breeds)
        c3.dataframe(df.T, use_container_width=True)
