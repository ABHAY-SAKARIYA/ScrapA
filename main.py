from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import json
from rich import print as rprint


# Declaring Common Error :

class modeErr(Exception):

    def __init__(self,mode) -> None:
        self.mode = mode
        self.message = f"You Have Entered The Wrong Mode {self.mode} \n Expecting 's' - for Single Page or 'm' for Multiple Page. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class captureErr(Exception):

    def __init__(self,captureType) -> None:
        self.captureType = captureType
        self.message = f"You Have Entered Wrong Capture type {self.captureType} \n Expecting 'static' for static websites or 'dynamic' for dynamic websites. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class selectorTypeErr(Exception):

    def __init__(self,selector) -> None:
        self.selector = selector
        self.message = f"Wrong Selector type {self.selector} \n Expecting dict Not {type(self.selector)}. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class selectorKeyerr(Exception):

    def __init__(self, selector) -> None:
        self.selector = selector
        self.message = f"Wrong Selector type {self.selector} \n Expecting 'css' or 'xpath'. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class staticUrlErr(Exception):

    def __init__(self, url) -> None:
        self.url = url
        self.message = f"Wrong Url Provided {self.url} \n Expecting str got {type(self.url)}. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class dynamicUrlErr(Exception):

    def __init__(self, url) -> None:
        self.url = url
        self.message = f"Wrong Url Provided {self.url} \n Expecting list got {type(self.url)}. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class encodingErr(Exception):

    def __init__(self) -> None:
        self.message = "Error In The Encoding of The Webpage While Saving Data To Html File Try Adding 'encoding='utf-16'' To Resolve This Error And Re Run The Program. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)

class EleNotFoundErr(Exception):

    def __init__(self,ele) -> None:
        self.message = f"Element Your Have Given {ele} Not Found In The Given Webpage"
        super().__init__(self.message)

class GetErr(Exception):

    def __init__(self) -> None:
        self.message = "Error Get is Not Defined Firstly Use filter() method to resolve this error. \n Or Read The Documentation For More Details.."
        super().__init__(self.message)


# creating File manager For Convient Handle of Files

class File:
    
    class Json:
        def write(filename : str,
                  data : str=None) -> None:
            with open(filename,"a+") as writeJson:
                writeJson.write(json.dumps(data,indent=4))
        def read(filename : str) -> str:
            with open(filename,"r") as readJson:
                Jsondata = json.load(readJson)
            return Jsondata
        
    class Html:
        def write(filename : str,
                  data : str = None,
                  encoding : str = "utf-8") -> None:
            with open(filename,"a+",encoding=encoding) as writehtml:
                writehtml.write(data)
        def read(filename : str,
                 encoding : str = "utf-8") -> str:
            with open(filename,"r",encoding=encoding) as readhtml:
                Htmldata = readhtml.read()
            return Htmldata
        
    class Csv:
        def write(filename : str,
                  data : dict = None) -> None:
            dataFrame = pd.DataFrame(data)
            dataFrame.to_csv(filename)
        def read(filename : str) -> any:
            datacsv = pd.read_csv(filename)
            return datacsv
    
    class Excel:
        def write(filename : str,
                  data : dict = None) -> None:
            dataFrame = pd.DataFrame(data)
            dataFrame.to_excel(filename)
        def read(filename : str) -> dict:
            dataexcel = pd.read_excel(filename)
            return dataexcel
        
    class Text:
        def write(filename : str,
                  data : str) -> None:
            with open(filename,"a+") as writeText:
                writeText.write(data)
        def read(filename : str) -> str:
            with open(filename,"r") as readText:
                dataText = readText.read()
            return dataText


# creating Web Scraper 

class ScrapA:

    def __init__(self) -> None:
        pass

    def CaptureData(self,
                    mode : str,
                    url : any,
                    captureType : str,
                    filename : str,
                    selector : object,
                    encoding : str = "utf-8") :
        self.mode = mode
        self.url = url
        self.captureType = captureType
        self.filename = filename
        self.selector = selector
        self.encoding = encoding

        # Prompting Errors Else Running Program

        if type(self.selector) != dict:
            raise selectorTypeErr(self.selector)
        
        reqSelectorKey = ["css","xpath"]
        self.userSelectorKey = [x for x in self.selector.keys()]
        if self.userSelectorKey[0] not in reqSelectorKey:
            raise selectorKeyerr(self.userSelectorKey[0])
        
        reqMode = ["s","m"]
        if self.mode not in reqMode:
            raise modeErr(self.mode)
        
        reqCaptureType = ["static","dynamic"]
        if self.captureType not in reqCaptureType:
            raise captureErr(self.captureType)
        
        if self.mode == "s":
            if type(self.url) != str:
                raise staticUrlErr(type(self.url))
            if self.captureType == "static":
                self.__captureStaticSingle()
            elif self.captureType == "dynamic":
                self.__captureDynamicSingle()
        elif self.mode == "m":
            if type(self.url) != list:
                raise dynamicUrlErr(type(self.url))
            if self.captureType == "static":
                self.__captureStaticMultiple()
            elif self.captureType == "dynamic":
                self.__captureDynamicMultiple()


    # To Capture Single And Static WebPage

    def __captureStaticSingle(self):
        try:
            response = requests.get(self.url)
                                    
            try :
                if response.status_code == 200:
                    rprint("[green bold]Successfuly Riched to the given website.[/green bold] \n [yellow] gathering data [/yellow]")
                
                    parser = BeautifulSoup(response.text,"html.parser")
                    time.sleep(3)
                    if self.userSelectorKey[0] == "css":
                        try:
                            for userReqEle in parser.select(self.selector[self.userSelectorKey[0]]):
                                try:
                                    File.Html.write(filename=f"{self.filename}.html", data=userReqEle.prettify(), encoding=self.encoding)
                                except:
                                    raise encodingErr()
                                rprint(f"[green bold] Data gathered Successfully and Saved To {self.filename}.html[/green bold]")
                        except:
                            raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                    elif self.userSelectorKey[0] == "xpath":
                        rprint("[red bold] Xpath Is Not Supported In Static captureType , Try It In Dynamic captureType  [/red bold]")
                
                else:
                    rprint(f"[red bold] Problem in riching to the given website exited with website status code:{response.status_code}[/red bold]")
            except Exception as e:
                raise rprint(f"[red bold]{e}[/red bold]")
        except Exception as e:
            rprint(f"[red bold] error occured provided url not found caused : {e}")
        

    # to Capture Static and Multiple Page

    def __captureStaticMultiple(self):
        try:
            count = 0
            for userLinks in self.url:
                filesavemsg = f"\n<!-- Website No. {count} starts from here url = '{userLinks}'-->\n"
                response = requests.get(userLinks)

                try:
                    if response.status_code == 200:
                        count+=1
                        rprint(f"[green bold]Successfuly Riched {count} website from the given list.[/green bold] \n [yellow] gathering data [/yellow]")
                    
                        parser = BeautifulSoup(response.text,"html.parser")
                        time.sleep(3)
                        if self.userSelectorKey[0] == "css":
                            if type(self.selector[self.userSelectorKey[0]]) == str:
                                try:
                                    File.Html.write(filename=f"{self.filename}.html", data=filesavemsg, encoding=self.encoding)
                                    for userReqEle in parser.select(self.selector[self.userSelectorKey[0]]):
                                        try:
                                            File.Html.write(filename=f"{self.filename}.html", data=userReqEle.prettify(), encoding=self.encoding)
                                        except:
                                            raise encodingErr()
                                        rprint(f"[green bold] Data gathered Successfully and Saved To {self.filename}.html[/green bold]")
                                except:
                                    raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                            elif type(self.selector[self.userSelectorKey[0]]) == list:
                                try:
                                    File.Html.write(filename=f"{self.filename}.html", data=filesavemsg, encoding=self.encoding)
                                    while True:
                                        for userReqEle in parser.select(self.selector[self.userSelectorKey[0]][count]):
                                            try:
                                                File.Html.write(filename=f"{self.filename}.html", data=userReqEle.prettify(), encoding=self.encoding)
                                            except:
                                                raise encodingErr()
                                            rprint(f"[green bold] Data gathered Successfully and Saved To {self.filename}.html[/green bold]")
                                        break
                                except:
                                    raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                                
                        elif self.userSelectorKey[0] == "xpath":
                            rprint("[red bold] Xpath Is Not Supported In Static captureType , Try It In Dynamic captureType  [/red bold]")
                            return
                    
                    else:
                        rprint(f"[red bold] Problem in riching to the given website exited with website status code:{response.status_code}[/red bold]")
                
                except Exception as e:
                    raise rprint(f"[red bold]{e}[/red bold]")
                count+=1
        except Exception as e:
            rprint(f"[red bold] error occured provided {userLinks} url not found caused : {e} ")


    # To Capture Dynamic Single Page 

    def __captureDynamicSingle(self):
        try:
            driver = webdriver.Chrome(options=Options())

            driver.get(self.url)

            try:
                rprint(f"[green bold]Successfuly Riched to website.[/green bold] \n [yellow] gathering data [/yellow]")
                parser = BeautifulSoup(driver.page_source,"html.parser")
                if self.userSelectorKey[0] == "css":
                    try:
                        for userReqEle in parser.select(self.selector[self.userSelectorKey[0]]):
                            try:
                                File.Html.write(filename=f"{self.filename}.html", data=f"{userReqEle.prettify()}",encoding=self.encoding)
                            except:
                                raise encodingErr()
                            rprint(f"[green bold] Data gathered Successfully and Saved To {self.filename}.html[/green bold]")
                    except:
                        raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                else:
                    if self.userSelectorKey[0] == "xpath":
                        try:
                            driver.page_source
                            userReqEleDriver = driver.find_element(By.XPATH,self.selector[self.userSelectorKey[0]])
                            userReqHtmlContent = userReqEleDriver.get_attribute("outerHTML")
                            try:
                                File.Html.write(filename=f"{self.filename}.html",data=userReqHtmlContent,encoding=self.encoding)
                            except:
                                raise encodingErr()
                        except:
                            raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                    else:
                        rprint(f"[red bold] {selectorKeyerr(self.selector)}[/red bold]")
                        return

            except Exception as e:
                raise rprint(f"[red bold]{e}[/red bold]")
        except Exception as e:
            rprint(f"[red bold] error occured provided {self.url} url not found caused : {e} ")


    # To Capture Dynamic Multiple Page

    def __captureDynamicMultiple(self):
        try:
            driver = webdriver.Chrome(options=Options())
            count = 0
            for links in self.url:
                filesavemsg = f"\n <!--Data for link No.{count+1} and link = {links} --> \n"
                driver.get(links)

                try:
                    rprint(f"[green] Reached To The Webpage No.{count}[/green] \n Gathering data")

                    if self.userSelectorKey[0] == 'css':
                        parser = BeautifulSoup(driver.page_source,"html.parser")
                        if type(self.selector[self.userSelectorKey[0]]) == str:
                            try:
                                File.Html.write(filename=f"{self.filename}.html",data=filesavemsg)
                                for userEle in parser.select(self.selector[self.userSelectorKey[0]]):
                                    try:
                                        File.Html.write(filename=f"{self.filename}.html",data=f"{userEle.prettify()}",encoding=self.encoding)
                                    except:
                                        raise encodingErr()
                                    rprint("[green] data saved successfuly[/green]")
                            except:
                                raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                        elif type(self.selector[self.userSelectorKey[0]]) == list:
                            try:
                                File.Html.write(filename=f"{self.filename}.html",data=filesavemsg)
                                while True:
                                    for userEle in parser.select(self.selector[self.userSelectorKey[0]][count]):
                                        try:
                                            File.Html.write(filename=f"{self.filename}.html",data=f"{userEle.prettify()}",encoding=self.encoding)
                                        except:
                                            raise encodingErr()
                                        rprint("[green] data saved successfuly[/green]")
                                    break
                            except:
                                raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                    else:
                        if self.userSelectorKey[0] == "xpath":
                            if type(self.selector[self.userSelectorKey[0]]) == str:
                                try:
                                    driver.page_source
                                    userReqEleDriver = driver.find_element(By.XPATH,self.selector[self.userSelectorKey[0]])
                                    userReqHtmlContent = userReqEleDriver.get_attribute("outerHTML")
                                    File.Html.write(filename=f"{self.filename}.html",data=filesavemsg)
                                    try:
                                        File.Html.write(filename=f"{self.filename}.html",data=userReqHtmlContent,encoding=self.encoding)
                                    except:
                                        raise encodingErr()
                                except:
                                    raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                            elif type(self.selector[self.userSelectorKey[0]]) == list:
                                try:
                                    driver.page_source
                                    while True:
                                        userReqEleDriver = driver.find_element(By.XPATH,self.selector[self.userSelectorKey[0]][count])
                                        userReqHtmlContent = userReqEleDriver.get_attribute("outerHTML")
                                        File.Html.write(filename=f"{self.filename}.html",data=filesavemsg)
                                        try:
                                            File.Html.write(filename=f"{self.filename}.html",data=userReqHtmlContent,encoding=self.encoding)
                                        except:
                                            raise encodingErr()
                                        break
                                except:
                                    raise EleNotFoundErr(self.selector[self.userSelectorKey[0]])
                            else:
                                rprint("[red bold] Cannot Identify The Xpath[/red bold]")
                                return
                        else:
                            rprint(f"[red bold] {selectorKeyerr(self.selector)}[/red bold]")
                            return
                except Exception as e:
                    rprint(f"[red bold] Exception occured {e} [/red bold]")
                    return
                count += 1
        except Exception as e:
            raise e
        

'''
 This Is an Filter Class Which Will Take Filename Which created from running above code and 
 take an css selector after that running parse() method it will filter the data according to 
 css selector provided and save them and after that running Get() Method with an argument as an         
 attribute of html and return the data get according to that attribute into a new variable,
 Text() method will return the text inside of the html element filtered before using parse() method.
'''
class Filter:

    def __init__(self,IF : str,css : str) -> None:
        self._IF = IF
        self._css = css
    
    def parse(self):
        data = File.Html.read(filename=self._IF,encoding="utf=8")

        parser = BeautifulSoup(data,"html.parser")
        self._data = []
        for ele in parser.select(self._css):
            self._data.append(ele)
        
    def Get(self,attr):
        try:
            if type(self._data) == list:
                self._reqData = []
                for e in self._data:
                    try:
                        if e.get(attr) != None:
                            self._reqData.append(e.get(attr))
                        else:
                            continue
                    except Exception as e:
                        raise e
            elif type(self._data) == str:
                if self._data != None:
                    self._reqData = self._data.get(attr)
                else:
                    self._reqData = None
            return self._reqData
        except:
            raise GetErr()
        
    
    def Text(self):
        try:
            if type(self._data) == list:
                self._text = []
                for e in self._data:
                    self._text.append(e.text)
            elif type(self._data) == str:
                self._text = self._data.text
            return self._text
        except:
            raise GetErr()


check = ScrapA()
# selector = {"css":["#faq-89","#faq-77"]}
# urllist = ["https://jainelibrary.org/","https://jainelibrary.org/"]
# check.CaptureData(url=urllist,mode="m",captureType="dynamic",filename="test",selector=selector)

# filt = Filter("test.html","a")
# filt.parse()
# a = filt.Get("target")
# # print(a)
# b = filt.Text()
# # print(b)

# data = {"link":a,"title":b}
# print(data)
