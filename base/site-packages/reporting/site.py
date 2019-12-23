

class ReportingSite(object):
    _registry = {}
    
    
    def register(self, slug, klass):
        self._registry[slug] = klass
        print self, self._registry
    
    def get_report(self, slug):
        try:
            return self._registry[slug]
        except KeyError:
            raise Exception("No such report '%s'" % slug)
    
    def all_reports(self):
        print self, self._registry
        return self._registry.items()


site = ReportingSite()