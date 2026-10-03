#!/data/data/com.termux/files/usr/bin/bash

# --- Color Definitions ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}[*] Initializing EVE_PRIME Termux Boot Sequence...${NC}"

# --- Step 1: Package Manager & Python Check ---
echo -e "${YELLOW}[*] Checking Python environment...${NC}"
if ! command -v python3 &> /dev/null || ! command -v pip &> /dev/null; then
    echo -e "${RED}[!] Installing python & core packages...${NC}"
    pkg update -y && pkg install -y python python-pip python-cryptography
fi

# --- Step 2: SDK Verification ---
echo -e "${YELLOW}[*] Verifying Google Generative AI SDK...${NC}"
if ! python3 -c "import google.generativeai" &> /dev/null; then
    echo -e "${YELLOW}[*] google-generativeai not imported. Attempting fast install via tur-repo...${NC}"
    pkg install -y tur-repo 2>/dev/null && pkg install -y python-pydantic 2>/dev/null
    pip install google-generativeai --quiet 2>/dev/null
fi

if python3 -c "import google.generativeai" &> /dev/null; then
    echo -e "${GREEN}[+] AI SDK Verified.${NC}"
else
    echo -e "${YELLOW}[!] Warning: google-generativeai not found. Running in fallback/simulated mode.${NC}"
fi

# --- Step 3: API Key Check ---
if [ -z "$GEMINI_API_KEY" ]; then
    echo -e "${YELLOW}[!] GEMINI_API_KEY is not set in this session.${NC}"
    echo -e "${YELLOW}[!] Dashboard will run in SIMULATED mode.${NC}"
    echo -e "    To use live AI: export GEMINI_API_KEY='your_key' then rerun."
    sleep 2
else
    echo -e "${GREEN}[+] GEMINI_API_KEY detected. Live AI active.${NC}"
fi

# --- Step 4: Launch Core Console ---
TARGET_SCRIPT=""
if [ -f "eve_console.py" ]; then
    TARGET_SCRIPT="eve_console.py"
elif [ -f "server.py" ]; then
    TARGET_SCRIPT="server.py"
fi

if [ -n "$TARGET_SCRIPT" ]; then
    echo -e "${GREEN}[*] Launching EVE_PRIME ($TARGET_SCRIPT)...${NC}"
    python3 "$TARGET_SCRIPT"
else
    echo -e "${RED}[!] Error: Neither eve_console.py nor server.py was found in $(pwd)${NC}"
    exit 1
fi
