import urllib.request, ssl, pypdf, io
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
url="https://img.zhinengdayi.com/imgServer/PVKZRL/2025-09-28/1k2fhm608.pdf"
# find 2026 catalog link from article 63652
req=urllib.request.Request("https://yz.cug.edu.cn/page/detail/PVKZRL/697/63652", headers={"User-Agent":"Mozilla/5.0"})
h=urllib.request.urlopen(req,timeout=60,context=ctx).read().decode("utf-8","ignore")
import re
pdfs=set(re.findall(r'https://img\.zhinengdayi\.com/imgServer/[^"\s]+\.pdf', h))
print("PDFS:", pdfs)
