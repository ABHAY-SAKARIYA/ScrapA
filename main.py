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
        self.message = f"You Have Entered The Wrong Mode {self.mode} \n Expecting 's' - for Single Page or 'm' for Multiple Page."
        super().__init__(self.message)

class captureErr(Exception):

    def __init__(self,captureType) -> None:
        self.captureType = captureType
        self.message = f"You Have Entered Wrong Capture type {self.captureType} \n Expecting 'static' for static websites or 'dynamic' for dynamic websites."
        super().__init__(self.message)

class selectorTypeErr(Exception):

    def __init__(self,selector) -> None:
        self.selector = selector
        self.message = f"Wrong Selector type {self.selector} \n Expecting dict Not {type(self.selector)}."
        super().__init__(self.message)

class selectorKeyerr(Exception):

    def __init__(self, selector) -> None:
        self.selector = selector
        self.message = f"Wrong Selector type {self.selector} \n Expecting 'css' or 'xpath'."
        super().__init__(self.message)

class staticUrlErr(Exception):

    def __init__(self, url) -> None:
        self.url = url
        self.message = f"Wrong Url Provided {self.url} \n Expecting str got {type(self.url)}."
        super().__init__(self.message)

class dynamicUrlErr(Exception):

    def __init__(self, url) -> None:
        self.url = url
        self.message = f"Wrong Url Provided {self.url} \n Expecting list got {type(self.url)}."
        super().__init__(self.message)

class encodingErr(Exception):

    def __init__(self) -> None:
        self.message = "Error In The Encoding of The Webpage While Saving Data To Html File Try Adding 'encoding='utf-16'' To Resolve This Error And Re Run The Program."
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
                        
                        for userReqEle in parser.select(self.selector[self.userSelectorKey[0]]):
                            File.Html.write(filename=f"{self.filename}.html", data=userReqEle.prettify(), encoding=self.encoding)
                            rprint(f"[green bold] Data gathered Successfully and Saved To {self.filename}.html[/green bold]")
                
                else:
                    rprint(f"[red bold] Problem in riching to the given website exited with website status code:{response.status_code}[/red bold]")
            except:
                raise rprint(f"[red bold]{encodingErr()}[/red bold]")
        except Exception as e:
            rprint(f"[red bold] error occured provided url not found caused : {e}")
        

check = ScrapA()
selector = {"css":"body"}
check.CaptureData(url="https://www.google.com",mode="s",captureType="static",filename="test",selector=selector)
