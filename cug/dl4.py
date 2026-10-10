import urllib.request, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
jobs=[("cug2025_fenshuxian.pdf","https://img.zhinengdayi.com/imgServer/PVKZRL/2025-09-25/1j5v6vocp.pdf")]
for name,url in jobs:
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=180,context=ctx) as r, open(name,"wb") as f:
            d=r.read(); f.write(d); print("OK",name,len(d))
    except Exception as e:
        print("ERR",name,type(e).__name__,e)
