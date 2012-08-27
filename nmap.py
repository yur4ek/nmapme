
from twisted.application import service, internet
from twisted.internet.utils import getProcessOutput
from twisted.python import log, components
from twisted.web import server, resource
from zope.interface import Interface, implements

import re


class INetworkScanner(Interface):
    def scanIP(addr):
        "Scan IP addr return string contains nmap utility output"


class NMap(service.Service):
    implements(INetworkScanner)

    def scanIP(self, addr):
        log.msg('nmap ', addr)
        return getProcessOutput('nmap', ['-sT', addr])


class webAPI(resource.Resource):
    isLeaf = True

    def __init__(self, original):
        self.original = original

    def formatPage(self, text):
        html = '<html><body>{0}</body></html>'
        res = re.sub(r'(Interesting ports on )(.*):', r'\1<b>\2</b>', text)
        return html.format(re.sub('\n', '<br>', res))

    def render_GET(self, request):
        def got_error(err):
            log.err(err)
            request.write('request fail')
            request.finish()

        def send_responce(text):
            agent = request.getHeader('user-agent')
            if 'curl' in agent:
                request.write(text)
            else:
                request.write(self.formatPage(text))
            request.finish()
        addr = request.getClientIP()
        log.msg(addr)
        d = self.original.scanIP(addr)
        d.addCallbacks(send_responce, got_error)
        return server.NOT_DONE_YET
        
components.registerAdapter(webAPI, INetworkScanner, resource.IResource)


nmap = NMap()
site = server.Site(resource.IResource(nmap))
webServer = internet.TCPServer(80, site, interface='0.0.0.0')

application = service.Application("nmapme")
nmap.setServiceParent(application)
webServer.setServiceParent(application)
