
from twisted.application import service, internet
from twisted.python import log, components
from twisted.internet import reactor, defer, threads
from twisted.internet.utils import getProcessOutput
from twisted.web import server, resource
from twisted.enterprise import adbapi
from subprocess import Popen, PIPE
from zope.interface import Interface, implements


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

    def render_GET(self, request):
        def got_error(err):
            log.err(err)
            request.write('request fail')
            request.finish()

        def send_responce(text):
            request.write(text)
            request.finish()
        
        addr = request.getClientIP()
        log.msg(addr)
        d = self.original.scanIP(addr)
        d.addCallbacks(send_responce, got_error)
        return server.NOT_DONE_YET
        
components.registerAdapter(webAPI, INetworkScanner, resource.IResource)


nmap = NMap()
site = server.Site(resource.IResource(nmap))
webServer = internet.TCPServer(80, site, interface='127.0.0.1')

application = service.Application("nmapme")
nmap.setServiceParent(application)
webServer.setServiceParent(application)
