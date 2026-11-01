---
title: SuperKart Retail Intelligence
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
tags:
- streamlit
- react
- typescript
pinned: false
short_description: Retail sales prediction and analysis
---

# SuperKart Retail Intelligence

SuperKart combines a Streamlit application with React and TypeScript custom components. The application runs as a Docker Space on Hugging Face.

## Architecture

- Streamlit owns the application shell, navigation, Python workflows, uploads, and session state.
- React + TypeScript components provide interactive visual elements through Streamlit Components v2.
- The existing Flask API continues to serve predictions from the trained model pipeline.

## Deployment

The Docker build uses Node 24 to compile the React component assets, then copies those assets into the Python 3.11 Streamlit image. Hugging Face runs Streamlit on port 8501.

The React component layer does not contain model logic and does not call the Flask API directly. Python passes the actual prediction response into the component.
