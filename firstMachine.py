# ----------------------- crawl session -----------------------

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ''

def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	index = {} # dictionary
	graph = {} 
	while tocrawl:
		page = tocrawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			#union(tocrawl, get_all_links(get_page(page)))
			outlinks = get_all_links(content)
			graph[page] = outlinks
			union(tocrawl, outlinks)
			crawled.append(page)
	return index, graph

def add_to_index(index, keyword, url):
    # for entry in index:
    #     if entry[keyword][0] == keyword:  # se bater a KEYWORD NO INDEX
    #         entry[1].append(url) # vamo dar um append na cauda do index
    #         return
    # index.append([keyword,[url]])	
    # newest ><
    if keyword in index:
    	index[keyword].append(url)
    else:
    	index[keyword] = [url]

# def make_big_index(size):
#     index = []
#     letters = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
#     while len(index) < size:
#         word = make_string(letters)
#         add_to_index(index, word, 'fake')
#         for i in range(len(letters) - 1, 0, -1): 
#             if letters[i] < 'z':
#                   letters[i] = chr(ord(letters[i]) + 1)
#                   break
#             else:
#                    letters[i] = 'a'
#     return index

def lookup(index, keyword):
    # for entry in index:
    #     if entry[0] == keyword:
    #         return entry[1]
    # newest
    if keyword in index:
    	return index[keyword]
    else:
    	return None

def add_page_to_index(index, url, content):
	print content
	words = content.split()
	for word in words:
		add_to_index(index,word,url)

def get_next_target(page):
   start_link = page.find('<a href=')
   if start_link == -1:
       return None,0   
   start_quote = page.find('"', start_link)
   end_quote = page.find('"', start_quote + 1)
   url = page[start_quote + 1:end_quote]
   return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links

def print_all_links(links):
	for item in links:
		print item

# ================== # crawl session

# ----------------------- hash session -----------------------

def hashtable_update(htable, key, value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return htable
    # if bucket == None:	
    #     hashtable_add(htable, key, value)
    bucket.append([key, value])
    return htable

def hashtable_lookup(htable, key):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None    

def hashtable_add(htable, key, value):
    bucket = hashtable_get_bucket(htable,key)
    bucket.append([key,value])

def hashtable_get_bucket(htable, keyword):
    return htable[hash_string(keyword,len(htable))]

def hash_string(keyword, buckets):
    out = 0
    for s in keyword:
        out = (out + ord(s)) % buckets
    return out

def make_hashtable(nbuckets):
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table

# ================== # hash session

# ----------------------- # popularity -----------------------

def compute_ranks(graph): #### LESSON 6
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
            	if page in graph[node]:
            		newrank = newrank + d * (ranks[node] / len(graph[node]))            
            newranks[page] = newrank
        ranks = newranks
    return ranks

# ================== # popularity session

# ----------------------- json session -----------------------

def toJson(index, name):
	import json
	import datetime
	now = datetime.datetime.now()
	with open(name + now.strftime("%d-%m-%Y_%H:%M") +'.json', 'w') as fp:
		json.dump(index, fp, indent=4, separators=(',', ':'))
# ================== # json session

# elements = {'a' : 3, 'b': [4, 5]}
# print elements['b'][0] + elements['b'][1] 
	
index, graph = crawl_web('https://www.udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

toJson(index, 'index')


print lookup(index, "Here")

print ranks
