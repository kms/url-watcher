#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# url-watcher
# Monitor webpages for changes.
#
# (c) Karl-Martin Skontorp <kms@skontorp.net> ~ http://picofarad.org/
# Licensed under the GNU GPL 2.0 or later.

from simpletal import simpleTAL, simpleTALES
import urllib2
import sys
import re
import md5
import os
from datetime import datetime, tzinfo, timedelta
from time import gmtime, strptime, mktime
from difflib import SequenceMatcher

def main():

    config = {'basedir': '/home/kms/web/la9pma.org/la-hams' \
	    ,'cachedir': '/home/kms/url-watcher/pages-la-hams' \
	    ,'proxy': 'home.tmvs.vgs.no:3128'}
    
    pagesToWatch = [('Personal', 'LAØBY', 'http://www.qsl.net/la0by/', None, 1.0)\
    	    ,('Group', 'LA2T Trondheimsgruppen', 'http://www.la2t.org/', None, 1.0)\
	    ,('Group', 'LA7G Gudbrandsdalgsgruppen', 'http://www.hamradio.no/la7g/', 'http://www.hamradio.no/la7g/start00.htm', 1.0)\
	    ,('Group', 'LA2D Drammensgruppen', 'http://www.la2d.com/', None, 1.0)\
	    ,('Misc', 'JX7SIX', 'http://www.qsl.net/la7dfa/jx7six.htm', None, 1.0)\
	    ,('Group', 'LA2K Kirkenesgruppen', 'http://www.arcticnet.no/la5xx/la2k.htm', None, 1.0)\
	    ,('Misc', 'Norwegain Repeaters, 2m', 'http://www.nrrl.no/4_fakta/rep_la144.htm', None, 1.0)\
	    ,('Misc', 'Norwegian Repeaters, 6m', 'http://www.nrrl.no/4_fakta/rep_la50.htm', None, 1.0)\
	    ,('Misc', 'Norwegian Repeaters, 70cm', 'http://www.nrrl.no/4_fakta/rep_la432.htm', None, 1.0)\
	    ,('Misc', 'Norwegian Repeaters, links', 'http://www.nrrl.no/4_fakta/rep_lafmlinks.htm', None, 1.0)\
	    ,('Misc', 'Samband Mjøsa', 'http://www.qsl.net/la3r/sm/sm.html', None, 1.0)\
	    ,('Misc', 'List of Norwegian hams', 'http://www.npt.no/pt_internet/ressursforvaltning/frekvenser/radioamatoer/radioamatoerer.html', None, 1.0)\
	    ,('Group', 'LA1G Grenlandgruppen', 'http://www.qsl.net/la1g/main.htm', None, 1.0)\
	    ,('News', 'NRRL Nyheter', 'http://www.nrrl.no/start/start00.htm', 'http://www.nrrl.no/', 1.0)\
	    ,('Personal', 'LA3LNA', 'http://www.la3lna.net/', None, 1.0)\
	    ,('Group', 'LA6LI Listagruppen', 'http://www.qsl.net/la6li/main.htm', 'http://www.qsl.net/la6li/', 1.0)\
	    ,('Personal', 'LA8OKA', 'http://www.arcticpeak.com/index.htm', None, 1.0)\
	    ,('Personal', 'LA8OKA (Radio)', 'http://www.arcticpeak.com/radio.htm', None, 1.0)\
	    ,('Misc', 'APRS Norge', 'http://aprs.dahltech.no/', None, 0.999)\
	    ,('Commercial', 'Permo', 'http://www.permo.no/main.htm', None, 1.0)\
	    ,('Commercial', 'Permo (Auksjon)', 'http://www.permo.no/Auksjon.htm', None, 1.0)\
	    ,('Commercial', 'Permo (Nyheter)', 'http://www.permo.no/A/Nyheter.htm', None, 1.0)\
	    ,('News', 'AMSAT', 'http://www.amsat.org/', None, 1.0)\
	    ,('News', 'AMSAT What\'s New', 'http://www.amsat.org/amsat/whatsnew.html', None, 1.0)\
	    ,('News', 'AMSAT WSR', 'http://www.amsat.org/amsat/news/wsr.html', None, 1.0)\
	    ,('Personal', 'LA8IMA', 'http://www.rolvs.org/index2.php', None, 1.0)\
	    ,('DX/Contest', '3B9C Rodrigues Island', 'http://www.fsdxa.com/3b9c/', None, 1.0)\
	    ,('DX/Contest', 'T33C Banaba', 'http://www.dx-pedition.de/banaba2004/home.htm', 'http://www.dx-pedition.de/banaba2004/', 1.0)\
	    ,('News', 'AMSAT OSCAR E', 'http://www.amsat.org/amsat/sats/echo/index.html', None, 1.0)\
	    ,('News', 'findU News', 'http://www.findu.com/new.html', None, 1.0)\
	    ,('Misc', 'Solar Terrestrial Activity Report', 'http://www.dxlc.com/solar/', None, 1.0)\
	    ,('Misc', 'W1AW Propagation Bulletins', 'http://www.arrl.org/w1aw/prop/', None, 0.99)\
	    ,('DX/Contest', 'Contests this week', 'http://www.hornucopia.com/contestcal/weeklycont.php', None, 1.0)\
	    ,('Personal', 'LA1BNA', 'http://www.la1bna.net/main.html', 'http://www.la1bna.net/', 1.0)\
	    ,('Personal', 'LA9PMA', 'http://la9pma.org/', None, 1.0)\
	    ,('Group', 'LA1T Tønsberggruppen', 'http://la1t.tsoft.no/files/nyheter.asp', 'http://la1t.tsoft.no/', 1.0)\
	    ,('Personal', 'LA5UNA', 'http://www.qsl.net/la5una/hei_og_velkommen_til_min_hjemmes.htm', 'http://www.qsl.net/la5una/', 1.0)\
	    ,('Personal', 'LA3YNA', 'http://home.online.no/~arvjakob/index2.htm', 'http://www.la3yna.tk/', 1.0)\
	    ,('Misc', 'Norwegian Beacon List', 'http://www.qsl.net/la0by/LA-beac.htm', None, 1.0)\
	    ,('Group', 'LA3T Tromsøgruppen', 'http://www.hamradio.no/la3t/hovedside.htm', 'http://www.hamradio.no/la3t/', 1.0)\
	    ,('Group', 'LA4O Oslogruppen', 'http://www.qsl.net/la4o/', None, 1.0)\
	    ,('Group', 'LA3F Follogruppen', 'http://www.la3f.no/main.htm', 'http://www.la3f.no/', 1.0)\
	    ,('Personal', 'LA5NCA', 'http://www.laud.no/la6nca/', None, 1.0)\
	    ,('Personal', 'LA9UX', 'http://www.qsl.net/la9ux/', None, 1.0)\
	    ,('Personal', 'LAØFX', 'http://www.qsl.net/la0fx/', None, 1.0)\
	    ,('Personal', 'LAØFA', 'http://www.qsl.net/la0fa/index.html', None, 1.0)\
	    ,('Personal', 'LAØFD', 'http://www.qsl.net/la0fd/index.html', None, 1.0)\
	    ,('Personal', 'LAØHV', 'http://www.qsl.net/la0hv/index.html', None, 1.0)\
	    ,('Personal', 'LA1AEA', 'http://www.qsl.net/la1aea/index.html', None, 1.0)\
	    ,('Group', 'LA ARDF', 'http://www.ardf.no/', None, 1.0)\
	    ,('Personal', 'LA1CNA', 'http://www.qsl.net/la1cna/index.html', None, 1.0)\
	    ,('Personal', 'LA1DGA', 'http://www.qsl.net/la1aea/main.html', 'http://www.qsl.net/la1aea/index.html', 1.0)\
	    ,('Misc', 'PACKET-radio nettet i Nord-Norge', 'http://www.qsl.net/la1h/nodenett/hoyre.htm', 'http://www.qsl.net/la1h/nodenett/index.htm', 1.0)\
	    ,('Group', 'LA1JAM', 'http://www.qsl.net/la1jam/index.htm', None, 1.0)\
	    ,('Personal', 'LA1KHA', 'http://www.qsl.net/la1kha/index.html', None, 1.0)\
	    ,('Personal', 'LA1KKA', 'http://www.qsl.net/la1kka/index.html', None, 1.0)\
	    ,('DX/Contest', 'VHF aktivitets-tester (NRAU NAC)', 'http://www.qsl.net/la1kka/vhf/index.html', None, 1.0)\
	    ,('Personal', 'LA1KP', 'http://www.qsl.net/la1kp/index.html', None, 1.0)\
	    ,('Group', 'LA8D Sandnes og Jærengruppen', 'http://www.lug.no/la8d/main.php?LA8D=1', 'http://www.lug.no/la8d/', 1.0)\
	    ,('Personal', 'LA3ZA', 'http://www.qsl.net/la3za/hoved.html', 'http://www.qsl.net/la3za/', 1.0)\
	    ,('Group', 'LA1NRK', 'http://home.eunet.no/~aosteren/index0.htm', None, 1.0)\
	    ,('Group', 'LA1NSF', 'http://www.qsl.net/la1nsf/index.htm', None, 1.0)\
	    ,('Personal', 'LA1PHA', 'http://www.qsl.net/la1pha/index.htm', None, 1.0)\
	    ,('Personal', 'LA1PNA', 'http://www.qsl.net/la1pna/index.htm', None, 1.0)\
	    ,('Personal', 'LA1SNA', 'http://www.qsl.net/la1sna/right.html', 'http://www.qsl.net/la1sna/index.html', 1.0)\
	    ,('Group', 'LA1SS Nettverk for radiospeidere', 'http://www.qsl.net/la1ss/index.html', None, 1.0)\
	    ,('Group', 'LA1TUR Radioklubben ut på tur', 'http://www.qsl.net/la1tur/index.html', 'http://www.qsl.net/la1tur/hoved.html', 1.0)\
	    ,('Personal', 'LA1UW', 'http://www.qsl.net/la1uw/index.html', None, 1.0)\
	    ,('Personal', 'LA1VNA', 'http://www.qsl.net/la1vna/index.htm', None, 1.0)\
	    ,('Personal', 'LA1ONA', 'http://www.qsl.net/la1ona/index.htm', None, 1.0)\
	    ,('Personal', 'LA3FY', 'http://k-j.skontorp.net/', None, 1.0)\
	    ,('Group', 'LA1B Bergensgruppen', 'http://www.qsl.net/la1b/frame1.htm', 'http://www.qsl.net/la1b/index.htm', 1.0)\
	    ]

    exportData = []

    startTime = int(mktime(gmtime()))

    for (category, title, watchURL, linkURL, tresholdRatio) in pagesToWatch:
	page = {}

	page['title'] = unicode(title, 'iso-8859-1')
	page['category'] = category
	page['watchURL'] = watchURL
	page['cacheFilename'] = md5.new(watchURL).hexdigest()
	if linkURL:
	    page['linkURL'] = linkURL
	else:
	    page['linkURL'] = watchURL
	page['tresholdRatio'] = tresholdRatio

	try:
	    request = urllib2.Request(watchURL)
	    if config.has_key('proxy'):
		request.set_proxy(config['proxy'], None)
		
	    if (len(sys.argv) == 2) and (sys.argv[1] == '--no-cache'):
		request.add_header('Pragma', 'no-cache')
		
	    response = urllib2.urlopen(request)
	    
	    lastModifiedHeader = response.info().getheader('Last-Modified')
	    page['proxyStatus'] = response.info().getheader('X-Cache')
	    
	    if lastModifiedHeader:
		page['lastModified'] \
			= int(mktime(strptime( \
			lastModifiedHeader, \
			'%a, %d %b %Y %H:%M:%S %Z')));
		page['lastModifiedFromHeader'] = 'true'
	    else:
		page['lastModified'] = int(mktime(gmtime()))
		page['lastModifiedFromHeader'] = 'false'

	    webpageNow = response.read()
	except urllib2.HTTPError:
	    continue

	try:
	    file = open(config['cachedir'] + '/' \
		    + page['cacheFilename'], 'r')
	    webpageOld = file.read()
	    file.close()
	except IOError:
	    webpageOld = ""

	s = SequenceMatcher(None, webpageNow, webpageOld)

	webpageRatio = s.ratio()

	s = None

	if webpageRatio < page['tresholdRatio']:
	    try:
		file = open(config['cachedir'] + '/' \
			+ page['cacheFilename'], 'w')
		file.write(webpageNow)
		file.close()
	    	os.utime(config['cachedir'] + '/' \
			+ page['cacheFilename'], \
			(page['lastModified'], page['lastModified']))
	    except IOError:
		print 'Unable to save cache...'

	secs = os.stat(config['cachedir'] + '/' \
		+ page['cacheFilename']).st_mtime

	class utc(tzinfo):
	    def utcoffset(self, dt): 
		return timedelta()
	    def dst(selft, dt):
		return timedelta()

	page['lastModified'] = datetime.fromtimestamp(secs, \
		tz=utc()).isoformat(sep='T')
	
	page['lastModifiedDate'] = datetime.fromtimestamp(secs, \
		tz=utc()).strftime('%A %d. %B, %Y')
	
	page['lastModifiedTime'] = datetime.fromtimestamp(secs, \
		tz=utc()).strftime('%H:%M')
		
	page['lastModifiedUnix'] = secs

	exportData.append(page)


    endTime = int(mktime(gmtime()))

    context = simpleTALES.Context()

    if (len(sys.argv) == 2) and (sys.argv[1] == '--no-cache'):
	context.addGlobal('noCache', 'true')
    else:
	context.addGlobal('noCache', 'false')

    context.addGlobal('runtime', str(endTime - startTime))
    context.addGlobal('pages', exportData)
    context.addGlobal('generated', datetime.utcnow().isoformat(sep='T'))
    templateFile = open(config['basedir'] + '/' + 'uw-template.xml', 'r')
    template = simpleTAL.compileXMLTemplate(templateFile)
    templateFile.close()
    template.expand(context, sys.stdout, 'iso-8859-1')

if __name__ == "__main__":
    main()
