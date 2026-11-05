#!/usr/bin/env bash
set -e

pip install -r requirements.txt
streamlit run src/main.py
