import urllib.request, ssl
url="https://img.zhinengdayi.com/imgServer/PVKZRL/2026-09-14/1k2fhm608.pdf"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=180, context=ctx) as r, open("cug2027_tuimian.pdf","wb") as f:
    d=r.read(); f.write(d); print("OK bytes=",len(d))
