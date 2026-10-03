import os
import sys

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print("[+] EVE_PRIME Core Server starting with live Gemini API...")
else:
    print("[!] EVE_PRIME Core Server starting in SIMULATED mode...")

print("[*] EVE_PRIME Server online. Core Axiom: 101100111101111.")
