import urllib.request, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
url="https://xjjsyjy.cug.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=2115221115&wbfileid=E83678EA3F6228F58841EA377986CF5E"
req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://xjjsyjy.cug.edu.cn/"})
with urllib.request.urlopen(req,timeout=180,context=ctx) as r, open("fs2027.zip","wb") as f:
    d=r.read(); f.write(d); print("OK",len(d), r.headers.get("Content-Type"))
