from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from news.models import NewsItem

class NewsFeed(Feed):

	def title(self):
		return u"%s" % Site.objects.get_current().name

	def description(self):
		return u'Latest news from %s' % Site.objects.get_current().name

	def link(self):
		# return reverse('news-index')
		return '/news/'

	def items(self):
		return NewsItem.on_site.published(5)
		
	def item_pubdate(self, item):
		from datetime import datetime
		return datetime(item.date.year, item.date.month, item.date.day)