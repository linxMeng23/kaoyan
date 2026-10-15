import urllib.request, ssl, sys
url="https://img.zhinengdayi.com/imgServer/PVKZRL/2026-10-08/1k4cm1mop.pdf"
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE
req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=180, context=ctx) as r, open("cug2027_zsjz.pdf","wb") as f:
        data=r.read(); f.write(data); print("OK bytes=",len(data))
except Exception as e:
    print("ERR", type(e).__name__, e)
