from main import  ScrapA , Filter



selector = {"css":["#faq-89","#faq-77"]}
urllist = ["https://jainelibrary.org/","https://jainelibrary.org/"]
ScrapA.CaptureData(url=urllist,mode="m",captureType="dynamic",filename="test",selector=selector)

# filt = Filter("test.html","a")
# filt.parse()
# a = filt.Get("target")
# # print(a)
# b = filt.Text()
# # print(b)

# data = {"link":a,"title":b}
# print(data)

# a = File.Html.read(filename="test.html")
# print(a)
