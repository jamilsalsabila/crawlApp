import urllib
import time

class crawl:
	# method constructor
	def __init__(self, urlSeed, numberOfPages):
		
		self.readLinkOkezone = urlSeed
		self.numberOfPages = numberOfPages
		self.urlHistoric = {}
		self.postpound = [i*1000 for i in range(1,11)]
	def start(self) :

		for count in range(36, self.numberOfPages):
		
			if not self.urlHistoric.get(self.readLinkOkezone+str(count), 0):

				self.appendURL(self.readLinkOkezone+str(count), count)
				
			#print str(self.urlHistoric)+"\n"
			#print str(len(self.urlHistoric)) + "\n"
			if count in self.postpound:
				time.sleep(60)

	def download(self, url, title):
		print "downloading : " + url
		try :
			urllib.urlretrieve(url, str(title)+'.html')
		except:
			print "ERROR"
		
		print "finish"

	def appendURL(self, url, count):
		self.urlHistoric[url] = self.urlHistoric.get(url, 1)
		self.download(url, count)
	
	def run(self):	
		self.start()

		print "size of self.urlHistoric = " + str(self.urlHistoric.__sizeof__())
		self.urlHistoric.clear()

if __name__ == '__main__':

	# start place 
	crawler = crawl("http://pelita.or.id/baca.php?id=", 10040)
	crawler.run()
