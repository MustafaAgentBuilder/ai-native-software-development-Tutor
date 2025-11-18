# SSL Handshake Timeout - Troubleshooting Guide

## Problem

You're seeing this error:
```
[non-fatal] Tracing: request failed: _ssl.c:989: The handshake operation timed out
```

This means your computer **cannot connect to OpenAI's servers**.

---

## ✅ Quick Fixes (Try These in Order)

### Fix 1: Check Internet Connection

**Test if you can reach OpenAI:**

1. Open browser
2. Go to: https://api.openai.com
3. You should see a page (even if it says "error", that's OK)
4. If page doesn't load → **Internet/firewall blocking OpenAI**

---

### Fix 2: Disable Antivirus/Firewall Temporarily

**Windows Defender Firewall:**

1. Open Windows Security
2. Click "Firewall & network protection"
3. Temporarily disable for "Private network"
4. Try running backend again
5. If it works → Add Python to firewall exceptions

**Antivirus (Kaspersky, Norton, McAfee, etc.):**

1. Temporarily disable antivirus
2. Try running backend again
3. If it works → Add exception for Python/OpenAI API

---

### Fix 3: Use VPN (if OpenAI is blocked in your region)

**Some countries/networks block OpenAI. Try:**

1. Install a VPN (ProtonVPN, NordVPN, ExpressVPN)
2. Connect to USA, UK, or European server
3. Try running backend again

**Free VPN options:**
- ProtonVPN (free tier)
- Windscribe (10GB/month free)
- TunnelBear (limited free)

---

### Fix 4: Check Corporate/School Network

**If you're on work/school network:**

1. Your network might block OpenAI API
2. Try connecting to mobile hotspot
3. Or ask IT department to whitelist:
   - `api.openai.com`
   - `*.openai.com`

---

### Fix 5: Configure Proxy (if behind corporate firewall)

**If your network uses a proxy:**

Create file: `Tutor-Agent/.env` and add:

```bash
HTTP_PROXY=http://your-proxy:port
HTTPS_PROXY=http://your-proxy:port
```

**Find your proxy settings:**
- Windows: Settings → Network & Internet → Proxy
- Copy the proxy address and port

---

### Fix 6: Increase System Timeout (Windows)

**Run this in PowerShell as Administrator:**

```powershell
# Increase TCP timeout
netsh interface tcp set global autotuninglevel=normal
netsh interface tcp set global congestionprovider=ctcp

# Restart network adapter
Disable-NetAdapter -Name "Ethernet" -Confirm:$false
Enable-NetAdapter -Name "Ethernet" -Confirm:$false
```

*(Replace "Ethernet" with your adapter name - find it with `Get-NetAdapter`)*

---

## 🧪 Test Your Connection

**Run this test script:**

```powershell
cd Tutor-Agent
uv run python test_openai_connection.py
```

**Expected output if working:**
```
✓ API Key loaded: sk-proj-RKVrPE16H...
✓ OpenAI client initialized
✓ API call successful!
Response: hello
```

**If test fails:**
- Your network is blocking OpenAI
- Try VPN (Fix 3 above)

---

## 🔄 Alternative: Use Mock/Cached Responses (Development)

**If you can't fix the network issue**, I can create a development mode that:
1. Returns pre-generated sample content
2. Doesn't need OpenAI API
3. Useful for testing frontend

**Would you like me to add this fallback mode?**

---

## 🌐 Check OpenAI Status

**Verify OpenAI isn't having issues:**

1. Go to: https://status.openai.com
2. Check if there are any outages
3. If "All Systems Operational" → Issue is on your end

---

## 📞 Still Not Working?

**Tell me which fix you tried and what happened:**

1. ✅ Internet works, can access api.openai.com?
2. ✅ Disabled antivirus/firewall?
3. ✅ Tried VPN?
4. ✅ Not on corporate/school network?
5. ✅ Test script result?

**I'll help you debug further based on your answers.**

---

## 🚀 Once Fixed

**After connection works:**

1. Restart backend: `uv run python -m tutor_agent.main`
2. Go to browser: http://localhost:3000
3. Click Personalized tab
4. ✅ Should work!

---

**Most Common Cause**: Firewall/antivirus blocking OpenAI

**Most Common Fix**: Disable antivirus temporarily or use VPN
