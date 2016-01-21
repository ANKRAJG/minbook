from django.shortcuts import render
from bookmarks.models import Bookmark, Tag_list
from django.http import HttpResponseBadRequest
#from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.core import serializers
import sqlite3
import re




def bookmarks(request):

    if request.method == 'POST':
        if request.POST.get('deleteUrl'):
            urls = request.POST.get('delete_url')
            
            conn = sqlite3.connect('db.sqlite3')
            o = conn.cursor()
            o.execute("DELETE FROM bookmarks_bookmark WHERE task = ?", (urls,))
            conn.commit()
            o.close()
              
    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM bookmarks_bookmark")
    result = c.fetchall()
    
    ids = [r[0] for r in result]
    tags = [r[1] for r in result]
    urls = [r[2] for r in result]
    
    j = ",".join(tags)                                  #Converting list into string i.e. from ['abc, xyz'] to 'abc, xyz'
    k = j.split(',')                                    # 'abc, xyz' to ['abc', 'xyz']   
    s_tags = unique(k)
    
    s = conn.cursor()                                   #Filling Tag_list Table if for some additional tags
    s.execute("SELECT * FROM bookmarks_tag_list")
    res = s.fetchall()
    
    tg_ids = [f[0] for f in res]
    tg_list = [f[1] for f in res]
    
    inter = intersect(s_tags, tg_list)
    new_tags = [x for x in s_tags if x not in inter]
    
    i = [idx for idx,t in enumerate(new_tags)] 
    for y in i:
        tagInstance = Tag_list(tags = new_tags[y])
        tagInstance.save()
    
    
    list = zip(ids, urls)
    
    context = {'list': list, 'all_tags': s_tags}

    return render(request, 'bookmark.html', context)






def save_data(request):
    
    data = request.GET.getlist('data[]')
    if data is None:
        return HttpResponseBadRequest()

    taskss = data[0]  
    del data[0]
    
    if not is_valid_url(taskss):
        return HttpResponse('<h1>Invalid URL!</h1>')
    
    
    if "http" not in taskss and "www" not in taskss:
        if "//" in taskss:
            return HttpResponse('<h2>// is present without http(or https) and www!</h2>')
        tasks = "http://www." + taskss
        
        
    elif "http" in taskss and "//" not in taskss and "www" in taskss:
        return HttpResponse('<h2>http(or https) and www are there but no "//"!</h2>')
    
    
    elif "http" not in taskss and "www" in taskss:
        if taskss[:3] == "www":
            tasks = "http://" + taskss
        else:
            return HttpResponse('<h2>Second elif ("www" not the First Characters)!</h2>')
        
        
    elif "http" in taskss and "www" not in taskss:
        try:
            taskss.index("/")
        except:
             return HttpResponse('<h2>http(or https) is there but www and // are not there!</h2>')
        k = taskss.index("/")
        tasks = taskss[:(k+2)] + "www." + taskss[(k+2):]
        
    else:
        tasks = taskss

    
    #loop for removing spaces from list data
    data = [x.strip(' ') for x in data]
    u_data = unique(data)

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM bookmarks_bookmark WHERE task LIKE '%" + tasks + "%'")
    result = c.fetchall()


    if not result:
        searchInstance = Bookmark(task = tasks, tag_name = ",".join(u_data))
        searchInstance.save()
        return HttpResponse('<h1>Data Saved!</h1>')
    
    '''      
    c.execute("SELECT * FROM bookmarks_bookmark")
    url_result = c.fetchall()
       
    urls = [idx for idx,r in enumerate(url_result)]
    url = [r[2] for r in url_result]      
        
    for i in urls:
        if not is_valid_url(url[i]):
            Bookmark.objects.filter(task = url[i]).delete()
    '''
    
    tup = [r[1] for r in result]
    tags1 = ",".join(tup)                               #Converting list into string i.e. from ['abc, xyz'] to 'abc, xyz'
    tags2 = tags1.split(',')                            # 'abc, xyz' to ['abc', 'xyz']
        
    #u_d = tup + u_data
    u_d = union(tags2, u_data)

    Bookmark.objects.filter(task__contains = tasks).update(tag_name = ",".join(u_d))

    return HttpResponse('<h1>Data Saved!</h1>')
    
  




def search_data(request):
    
    data1 = request.GET.getlist('data[]')
    data = data1[0]
    
    urls = Bookmark.objects.all().filter(tag_name__contains = data)
    
    json_artists = serializers.serialize("json", urls)
    return HttpResponse(json_artists, content_type="application/json")
    
    
    
    

def edit_tags(request):
    
    if request.method == 'POST':
        if request.POST.get('tagName'):
            tg = request.POST.get('tagName')

            conn = sqlite3.connect('db.sqlite3')
            c = conn.cursor()
            c.execute("SELECT * FROM bookmarks_tag_list")
            result = c.fetchall()

            tgs = [r[1] for r in result]

            if tg not in tgs:
                newTag = Tag_list(tags = tg)
                newTag.save()
                
        elif request.POST.get('deleteTag'):  
            tggs = request.POST.get('delete_tag')
            
            conn = sqlite3.connect('db.sqlite3')
            o = conn.cursor()
            mydata = o.execute("DELETE FROM bookmarks_tag_list WHERE tags = ?", (tggs,))
            conn.commit()
    
    conn = sqlite3.connect('db.sqlite3')
    b = conn.cursor()
    b.execute("SELECT * FROM bookmarks_tag_list")
    resultt = b.fetchall()
    
    context = {'list': resultt}

    return render(request, 'edit_tags.html', context)
    
    
 


def show_url(request, pk):
    
    if request.method == 'POST':
        taggs = request.POST.getlist('bookmark_tags')
        urlls = request.POST.get('bookmark_url')
        
        taggs1 = ",".join(taggs)                               #Converting list into string i.e. from ['abc, xyz'] to 'abc, xyz'
        taggs2 = taggs1.split(',')
        
        tas = Bookmark.objects.get(id = pk)
        tasks = tas.task
        
        Bookmark.objects.filter(task__contains = tasks).update(task = urlls, tag_name = ",".join(taggs2))
           
    
    conn = sqlite3.connect('db.sqlite3')
    d = conn.cursor()
    d.execute("SELECT * FROM bookmarks_bookmark WHERE id LIKE '%" + pk + "%'")
    result = d.fetchall()

    id_list = [r[0] for r in result]                        #id_list, tags_list, url_list will contain only one element
    tags_list = [r[1] for r in result]
    url_list = [r[2] for r in result]
    
    ids = id_list[0]
    urls = url_list[0]
    
    j = ",".join(tags_list)                                  #Converting list into string i.e. from ['abc, xyz'] to 'abc, xyz'
    s_tags = j.split(',')                                         # 'abc, xyz' to ['abc', 'xyz']   
    
    #Extracting Title from URL
    m = urls.index(".")
    q = urls[(m+1)].upper()                             #Converting first letter to uppercase
    n = urls[(m+1):].index(".")
    title = q + urls[(m+2):(m+n+1)]
    
    context = {'ids': ids, 'urls': urls, 'tags': s_tags, 'title': title}

    return render(request, 'show_url.html', context)
    
    
    

    
def edit_url_tags(request, pk):

    conn = sqlite3.connect('db.sqlite3')
    g = conn.cursor()
    g.execute("SELECT * FROM bookmarks_bookmark WHERE id LIKE '%" + pk + "%'")
    res = g.fetchall()
    
    id_list = [r[0] for r in res]                        #id_list, tags_list, url_list will contain only one element
    tags_list = [r[1] for r in res]
    url_list = [r[2] for r in res]
    
    j = ",".join(tags_list)                                  #Converting list into string i.e. from ['abc, xyz'] to 'abc, xyz'
    s_tags = j.split(',')                                         # 'abc, xyz' to ['abc', 'xyz']   
    
    conn = sqlite3.connect('db.sqlite3')
    h = conn.cursor()
    h.execute("SELECT * FROM bookmarks_tag_list")
    result = h.fetchall()

    all_tags = [t[1] for t in result]

    tags_left = [x for x in all_tags if x not in s_tags]
    
    p = len(s_tags)
    ids = [idx for idx,k in enumerate(s_tags)]
    
    ids_left = [idr+p for idr,k in enumerate(tags_left)]
    
    list1 = zip(ids, s_tags)
    list2 = zip(ids_left, tags_left)
    
    context = {'list1': list1, 'list2': list2, 'urls': url_list[0], 'ids': id_list[0]}

    return render(request, 'edit_url_tags.html', context)
    
    

    
    
def show_tags(request, pk):
    
    if request.method == 'POST':
        tgs = request.POST.get('tag')
        tag_d = Tag_list.objects.get(id = pk)
        tg = tag_d.tags
        Tag_list.objects.filter(tags = tg).update(tags = tgs)
    
    tag_details = Tag_list.objects.get(id = pk)
    tag = tag_details.tags
    
    context = {'tag': tag, 'ids': pk}
    return render(request, 'show_tags.html', context)
    

    
    
    
def edit_tags_edit(request, pk):
    tag_details = Tag_list.objects.get(id = pk)
    tag = tag_details.tags
    
    context = {'tag': tag, 'ids': pk}
    return render(request, 'edit_tags_edit.html', context)

    
    
    
def new_tag(request):
    return render(request, 'new_tag.html', None)
        
    

    
    
    
def delete_url(request, pk):
    
    book = Bookmark.objects.get(id = pk)
    urls = book.task
    tags1 = book.tag_name
    ids = book.id
    tags = tags1.split(',') 
    
    context = {'urls': urls, 'tags': tags, 'ids': ids}
    return render(request, 'delete_url.html', context)
    

    
    

def delete_tag(request, pk):
    
    tags = Tag_list.objects.get(id = pk)
    tag = tags.tags
    ids = tags.id
    
    context = {'tag': tag, 'ids': ids}
    return render(request, 'delete_tag.html', context)

    
  

    
def is_valid_url(url):
    import re
    regex = re.compile(
        #r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)




def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))



    
def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))



def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))