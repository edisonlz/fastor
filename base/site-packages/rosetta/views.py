from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from rosetta.polib import pofile
from rosetta.poutil import find_pos, pagination_range
from rosetta.conf import settings as rosetta_settings
import re, os, rosetta, datetime


def home(request):
    """
    Displays a list of messages to be translated
    """
        
    def fix_nls(in_,out_):
        """Fixes submitted translations by filtering carriage returns and pairing
        newlines at the begging and end of the translated string with the original
        """
        if 0 == len(in_) or 0 == len(out_):
            return out_

        if "\r" in out_ and "\r" not in in_:
            out_=out_.replace("\r",'')

        if "\n" == in_[0] and "\n" != out_[0]:
            out_ = "\n" + out_
        elif "\n" != in_[0] and "\n" == out_[0]:
            out_ = out_.lstrip()
        if "\n" == in_[-1] and "\n" != out_[-1]:
            out_ = out_ + "\n"
        elif "\n" != in_[-1] and "\n" == out_[-1]:
            out_ = out_.rstrip()
        return out_
    
    version = rosetta.get_version(True)
    if 'rosetta_i18n_fn' in request.session:
        rosetta_i18n_fn=request.session.get('rosetta_i18n_fn')
        rosetta_i18n_pofile = request.session.get('rosetta_i18n_pofile')
        rosetta_i18n_lang_code = request.session['rosetta_i18n_lang_code']
        rosetta_i18n_lang_bidi = (rosetta_i18n_lang_code in settings.LANGUAGES_BIDI)
        rosetta_i18n_write = request.session.get('rosetta_i18n_write', True)
        
        if 'filter' in request.GET:
            if request.GET.get('filter') == 'untranslated' or request.GET.get('filter') == 'translated' or request.GET.get('filter') == 'both':
                filter_ = request.GET.get('filter')
                request.session['rosetta_i18n_filter'] = filter_
                return HttpResponseRedirect(reverse('rosetta-home'))
        elif 'rosetta_i18n_filter' in request.session:
            rosetta_i18n_filter = request.session.get('rosetta_i18n_filter')
        else:
            rosetta_i18n_filter = 'both'
                
        if '_next' in request.POST:
            rx=re.compile(r'^m_([0-9]+)')
            rx_plural=re.compile(r'^m_([0-9]+)_([0-9]+)')
            file_change = False
            for k in request.POST.keys():
                if rx_plural.match(k):
                    id=int(rx_plural.match(k).groups()[0])
                    idx=int(rx_plural.match(k).groups()[1])
                    rosetta_i18n_pofile[id].msgstr_plural[str(idx)] = fix_nls(rosetta_i18n_pofile[id].msgid_plural[idx], request.POST.get(k))
                    file_change = True 
                elif rx.match(k):
                    id=int(rx.match(k).groups()[0])
                    rosetta_i18n_pofile[id].msgstr = fix_nls(rosetta_i18n_pofile[id].msgid, request.POST.get(k))
                    file_change = True
                if file_change and 'fuzzy' in rosetta_i18n_pofile[id].flags:
                    rosetta_i18n_pofile[id].flags.remove('fuzzy')
                    
                        
            if file_change and rosetta_i18n_write:
                try:
                    rosetta_i18n_pofile.metadata['Last-Translator'] = str(u"%s %s <%s>" %(request.user.first_name,request.user.last_name,request.user.email))
                    rosetta_i18n_pofile.metadata['X-Translated-Using'] = str(u"django-rosetta %s" % rosetta.get_version(False))
                    rosetta_i18n_pofile.metadata['PO-Revision-Date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M%z')
                except UnicodeDecodeError:
                    pass
                try:
                    rosetta_i18n_pofile.save()
                    rosetta_i18n_pofile.save_as_mofile(rosetta_i18n_fn.replace('.po','.mo'))
                    
                    # Try auto-reloading via the WSGI daemon mode reload mechanism
                    if  rosetta_settings.WSGI_AUTO_RELOAD and \
                        request.environ.has_key('mod_wsgi.process_group') and \
                        request.environ.get('mod_wsgi.process_group',None) and \
                        request.environ.has_key('SCRIPT_FILENAME') and \
                        int(request.environ.get('mod_wsgi.script_reloading', '0')):
                            try:
                                os.utime(request.environ.get('SCRIPT_FILENAME'), None)
                            except OSError:
                                pass
                        
                except:
                    request.session['rosetta_i18n_write'] = False
                
                request.session['rosetta_i18n_pofile']=rosetta_i18n_pofile
                
                # Retain query arguments
                query_arg = ''
                if 'query' in request.REQUEST:
                    query_arg = '?query=%s' %request.REQUEST.get('query')
                if 'page' in request.GET:
                    if query_arg:
                        query_arg = query_arg + '&'
                    else:
                        query_arg = '?'
                    query_arg = query_arg + 'page=%d' % int(request.GET.get('page'))
                    
                    
                return HttpResponseRedirect(reverse('rosetta-home') + query_arg)
                
                
        rosetta_i18n_lang_name = _(request.session.get('rosetta_i18n_lang_name'))
        rosetta_i18n_lang_code = request.session.get('rosetta_i18n_lang_code')
                
        if 'query' in request.REQUEST and request.REQUEST.get('query','').strip():
            query=request.REQUEST.get('query').strip()
            rx=re.compile(query, re.IGNORECASE)
            paginator = Paginator([e for e in rosetta_i18n_pofile if rx.search(smart_unicode(e.msgstr)+smart_unicode(e.msgid)+u''.join([o[0] for o in e.occurrences]))], rosetta_settings.MESSAGES_PER_PAGE)
        else:
            if rosetta_i18n_filter == 'both':
                paginator = Paginator(rosetta_i18n_pofile, rosetta_settings.MESSAGES_PER_PAGE)
            elif rosetta_i18n_filter == 'untranslated':
                paginator = Paginator(rosetta_i18n_pofile.untranslated_entries(), rosetta_settings.MESSAGES_PER_PAGE)
            elif rosetta_i18n_filter == 'translated':
                paginator = Paginator(rosetta_i18n_pofile.translated_entries(), rosetta_settings.MESSAGES_PER_PAGE)
        
        if 'page' in request.GET and int(request.GET.get('page')) <= paginator.num_pages and int(request.GET.get('page')) > 0:
            page = int(request.GET.get('page'))
        else:
            page = 1
        messages = paginator.page(page).object_list
        needs_pagination = paginator.num_pages > 1
        if needs_pagination:
            if paginator.num_pages >= 10:
                page_range = pagination_range(1, paginator.num_pages, page)
            else:
                page_range = range(1,1+paginator.num_pages)
        ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
        ENABLE_TRANSLATION_SUGGESTIONS = rosetta_settings.ENABLE_TRANSLATION_SUGGESTIONS
        
        return render_to_response('rosetta/pofile.html', locals())
        
        
    else:
        return list_languages(request)
home=user_passes_test(lambda user:can_translate(user),'/admin/')(home)
home=never_cache(home)


def download_file(request):
    import zipfile, tempfile, os
    # original filename
    rosetta_i18n_fn=request.session.get('rosetta_i18n_fn', None)
    # in-session modified catalog
    rosetta_i18n_pofile = request.session.get('rosetta_i18n_pofile', None)
    # language code
    rosetta_i18n_lang_code = request.session.get('rosetta_i18n_lang_code', None)
    
    if not rosetta_i18n_lang_code or not rosetta_i18n_pofile or not rosetta_i18n_fn:
        return HttpResponseRedirect(reverse('rosetta-home'))
    try:
        if len(rosetta_i18n_fn.split('/')) >= 5:
            offered_fn = '_'.join(rosetta_i18n_fn.split('/')[-5:])
        else:
            offered_fn = rosetta_i18n_fn.split('/')[-1]
        # filenames
        tmpdir=tempfile.gettempdir()
        zip_fn = str(os.path.join(tmpdir,'%s.%s.zip' %(offered_fn,rosetta_i18n_lang_code)))
        po_fn = str(os.path.join(tmpdir, rosetta_i18n_fn.split('/')[-1]))
        mo_fn = str(po_fn.replace('.po','.mo')) # not so smart, huh
        rosetta_i18n_pofile.save(po_fn)
        rosetta_i18n_pofile.save_as_mofile(mo_fn)
        zf = zipfile.ZipFile(zip_fn,'w')
        zf.write(po_fn, str(po_fn.split('/')[-1]))
        zf.write(mo_fn, str(mo_fn.split('/')[-1]))
        zf.close()
        
        response = HttpResponse(file(zip_fn).read())
        response['Content-Disposition'] = 'attachment; filename=%s.%s.zip' %(offered_fn,rosetta_i18n_lang_code)
        response['Content-Type'] = 'application/x-zip'
    
        os.unlink(zip_fn)
        os.unlink(po_fn)
        os.unlink(mo_fn)

        return response
    except Exception, e:
        return HttpResponseRedirect(reverse('rosetta-home'))
        #return HttpResponse(e, mimetype="text/plain")
download_file=user_passes_test(lambda user:can_translate(user),'/admin/')(download_file)
download_file=never_cache(download_file)
        


def list_languages(request):
    """
    Lists the languages for the current project, the gettext catalog files
    that can be translated and their translation progress
    """
    languages = []
    do_django = 'django' in request.GET
    do_rosetta = 'rosetta' in request.GET
    has_pos = False
    for language in settings.LANGUAGES:
        pos = find_pos(language[0],include_djangos=do_django,include_rosetta=do_rosetta)
        has_pos = has_pos or len(pos)
        languages.append(
            (language[0], 
            _(language[1]),
            [(os.path.realpath(l), pofile(l)) for l in  pos],
            )
        )
    ADMIN_MEDIA_PREFIX = settings.ADMIN_MEDIA_PREFIX
    version = rosetta.get_version(True)
    return render_to_response('rosetta/languages.html', locals())    
list_languages=user_passes_test(lambda user:can_translate(user),'/admin/')(list_languages)
list_languages=never_cache(list_languages)

def lang_sel(request,langid,idx):
    """
    Selects a file to be translated
    """
    if langid not in [l[0] for l in settings.LANGUAGES]:
        raise Http404
    else:
        
        do_django = 'django' in request.GET
        do_rosetta = 'rosetta' in request.GET
        
        file_ = find_pos(langid,include_djangos=do_django,include_rosetta=do_rosetta)[int(idx)]
        
        request.session['rosetta_i18n_lang_code'] = langid
        request.session['rosetta_i18n_lang_name'] = unicode([l[1] for l in settings.LANGUAGES if l[0] == langid][0])
        request.session['rosetta_i18n_fn'] = file_
        po = pofile(file_)
        for i in range(len(po)):
            po[i].id = i
            
        request.session['rosetta_i18n_pofile'] = po
        try:
            os.utime(file_,None)
            request.session['rosetta_i18n_write'] = True
        except OSError:
            request.session['rosetta_i18n_write'] = False
            
        return HttpResponseRedirect(reverse('rosetta-home'))
lang_sel=user_passes_test(lambda user:can_translate(user),'/admin/')(lang_sel)
lang_sel=never_cache(lang_sel)

def can_translate(user):
    if not user.is_authenticated():
        return False
    elif user.is_superuser:
        return True
    else:
        try:
            from django.contrib.auth.models import Group
            translators = Group.objects.get(name='translators')
            return translators in user.groups.all()
        except Group.DoesNotExist:
            return False

