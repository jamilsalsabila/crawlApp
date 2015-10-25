import urllib
import requests
from lxml import html
from bs4 import BeautifulSoup
import urlparse
import time
import os  #os.system("wget -O ttt.html <url>")

class crawl:
	# method constructor
	def __init__(self, urlSeed):
		self.urlSeed = urlSeed
		self.urlList = [self.urlSeed]
		self.urlHistoric = {self.urlSeed : 1}
		self.title = None
		self.count = 0
		self.logfile = open('LOG.txt', 'w')
		self.logfileHist = open('histLog.txt', 'w')
		self.readLinkOkezone = "http://news.okezone.com/read/2014/"

	def start(self) :

		htmlcontent = requests.get(self.urlList[0])
		
		self.title = str(self.count+1)
		self.count+=1
		
		soup = BeautifulSoup(htmlcontent.text)
		try:
			tree = html.fromstring(htmlcontent.text)
		except:
			print "web page error"
			print self.urlList[0]
			self.urlList.pop(0)
			return
		accesstime = time.ctime()
		try:
			title = tree.xpath('//div[@class="titles"]/h1/text()')[0].strip()
			date = tree.xpath('//div[@class="meta-post"]//p/time[@class="tgl"]/text()')[0].strip()
			author = tree.xpath('//div[@class="nmreporter"]/div/text()')[0].strip()
			
		except:
			title = "?"
			date = "?"
			author = "?"

		self.logFile(self.urlList[0], title, date, author, accesstime)
		#if self.urlList[0] not in self.urlHistoric:
		#self.download(self.urlList[0], self.title)
			#self.urlHistoric.append(self.urlList[0])
		self.urlList.pop(0)
		extractLink = soup.findAll('a', href=True)

		for link in extractLink:
			# news.okezone.com/read/ (articel)
			# news.okezone.com/view/ (photos)
			# news.okezone.com/play/ (videos)
			# news.okezone.com/more_topic/ (list of links)
			# news.okezone.com/topic/ (list of links of particular topic)
			link['href'] = urlparse.urljoin("http://news.okezone.com/", link['href'])
			if self.readLinkOkezone in link['href'] and not self.urlHistoric.get(link['href'], 0):

				self.appendURL(link['href'])
				print link['href']
			
		print "items in urlList = "+str(len(self.urlList))+"\n"
		print "items in urlHistoric = "+str(len(self.urlHistoric))+"\n"
		

	def download(self):
		title = 7100
		postpound = [i*1000 for i in range(1,11)]
		for item in self.urlHistoric:
			if title in postpound:
				time.sleep(60)

			os.system("wget -O "+str(title)+".html"+" "+item)
			title += 1

	def logFile(self, url, title, date, author, accesstime):
		try :
			self.logfile.write("%s::%s::%s::%s::%s\n" %(url, title.encode('UTF-8'), date.encode('UTF-8'), author.encode('UTF-8'), accesstime))
	 		self.logfileHist.write("%s\n" %(url))
	 	except:
	 		print "web page error"
			print self.urlList[0]
			self.urlList.pop(0)
			return

	'''
	def checkURL(self, url):
		
		regex = '(#fragment-|index\.|#content-)' #ad.beritasatumedia.com
		pattern = re.compile(regex)
		output = re.findall(pattern, url)

		if len(output) >= 1:
			x = url.find(output[0])
			url = url[0:x]
		elif 'ad.beritasatumedia.com' in url:
			return
		else :
			if url=='http://suarapembaruan.com/' or url=='http://suarapembaruan.com/home':
				url = 'http://suarapembaruan.com/home/'

		#print url
		self.appendURL(url)
	'''	
	def appendURL(self, url):


		self.urlList.append(url)
		self.urlHistoric[url] = self.urlHistoric.get(url, 1)
		
	
	def run(self, numberOfPages):
		i = 0
		postpound = [i*1000 for i in range(1,11)]
	
		while len(self.urlHistoric) <= 2950:
			if len(self.urlList) == 0:
				break
			if i in postpound:
				time.sleep(60) # biar ip tidak di-blokir akibat banyak request, dikiranya DDOS
			self.start()
			i += 1

		self.download()
		
		savedLink = open("savedLink.txt", 'w')
		for link in self.urlList:
			savedLink.write(link+"\n")

		savedLink.close()
		self.logfile.close()	
		self.logfileHist.close()
		print "size of self.urlHistoric = " + str(self.urlHistoric.__sizeof__())
		self.urlHistoric.clear()

if __name__ == '__main__':

	# start place 
	crawler = crawl("http://news.okezone.com/read/2014/09/08/373/1036039/bloobis-bawa-leo-ke-mit/largehttp:")
	crawler.run(10000)
