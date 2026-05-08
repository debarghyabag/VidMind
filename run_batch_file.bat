@echo off
title VidMind Backend

call deb\Scripts\activate.bat

echo Starting VidMind Backend...

fastapi dev .\app\main.py