import requests
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection


class StreamPetConnection(ExperimentalBaseConnection[requests.Session]):
    """Basic st.experimental_connection implementation for Pet API"""

    def __init__(self, connection_name: str, **kwargs):
        super().__init__(connection_name, **kwargs)

    def _connect(self, **kwargs) -> requests.Session:
        session = requests.Session()
        return session

    def cursor(self) -> requests.Session:
        return self._instance

    def query(self, url, params={}, ttl=600, **kwargs):
        @st.cache_data(ttl=ttl)
        def _query(params, **kwargs):
            response = self.cursor().get(url, params=params)
            response.raise_for_status()
            return response

        return _query(params, **kwargs)
