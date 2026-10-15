import urllib.request, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
url="https://img.zhinengdayi.com/imgServer/NJBCYO/2025-09-30/1j6c58216.pdf"
req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req,timeout=180,context=ctx) as r, open("cug2026_zsjz.pdf","wb") as f:
    d=r.read(); f.write(d); print("OK",len(d))
