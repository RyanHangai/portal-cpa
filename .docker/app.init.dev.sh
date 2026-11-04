#!/usr/bin/env bash

pip install -r requirements.txt
goose up
streamlit run src/main.py
