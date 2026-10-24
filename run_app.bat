@echo off
title DMGT Topic 14 - Huffman Coding Interactive Dashboard
cd /d "%~dp0"
echo =======================================================================
echo   LAUNCHING DMGT EXPERIENTIAL LEARNING INTERACTIVE DASHBOARD
echo   Topic 14: Optimal Prefix Codes and Data Compression (Huffman Coding)
echo   JAIN (Deemed-to-be University) - CSE Blockchain Technology
echo =======================================================================
echo.
python -m streamlit run app.py
pause
