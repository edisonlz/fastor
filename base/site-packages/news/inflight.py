INFLIGHT_APP_LABEL = 'news'
TAB_TEXT = "News"
TAB_URL = '/inflight/news/'
ADMIN_REQUIRED = False

from django.template.defaultfilters import truncatewords_html, striptags
from news.models import NewsItem

class SearchableNews(object):	
	def get_results(self, keywords):
		results = []
		for item in NewsItem.on_site.published():
			title_score = item.title.lower().count(keywords) * 5 # `title` has five times the relevance of body
			body_score = item.body.lower().count(keywords)
			total_score = title_score + body_score
			snippet = item.snippet or item.body
			if total_score > 0:
				import textile
				snippet = truncatewords_html(textile.textile(snippet.encode('ascii','xmlcharrefreplace')), 25)
				results.append((item, item.title, snippet, total_score))
		return results