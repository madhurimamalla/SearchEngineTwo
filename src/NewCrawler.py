#Finishing the page ranking algorithm.

def compute_ranks(graph):
    d = 0.8 # damping factor     # Find out why we have this damping factor? How do we arrive at it? 
    numloops = 10                                   # Number of iterations.
    
    ranks = {}                                      # 'ranks' is a dictionary {}
    npages = len(graph)                             # npages is the length of the graph (basically how many URLs/pages)
    for page in graph:                              # For every page in the graph, initiate a ranks array with 1/npages
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            
            #Insert Code Here
            for node in graph:
                if page in graph[node]:
                    newrank = newrank+d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


# What does crawl_web(seed) do: Take 'seed' page as the only input. It uses get_page() to get the content of the inputed page. 
# Then, it starts with a list called 'tocrawl' and keeps adding pages to it. It recursively goes through all the pages till where this first seed links and puts them in a graph. 
# There are 2 lists to know about 1. tocrawl; 2. crawled; 

def crawl_web(seed): # returns index, graph of inlinks 
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl:                                      # while the tocrawl list is not empty
        page = tocrawl.pop()                            # Pops the last entered URL in the tocrawl list  
        if page not in crawled:                         # Checks if the page is not already traversed. If it is, skips this if loop and goes back to 'while tocrawl'
            content = get_page(page)                    # Explained below. 
            add_page_to_index(index, page, content)     # Explained below. 
            outlinks = get_all_links(content)           # Explained below.
                       
            graph[page] = outlinks                      # 'page' is the keyword and for that it attaches it to a list outlinks.
            
            union(tocrawl, outlinks)                    # Check if the links that are present in 'outlinks' are also there is 'tocrawl' , if not , it'll add/append them to 'tocrawl' list.
            crawled.append(page)                        # Appends the whole page (content) to the string 'crawled'
    return index, graph


# This function get a 'url' as input and then returns the content of that URL. 
def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

    
def get_next_target(page):                          # The input to this function is the content/page sent from get_all_links()
    start_link = page.find('<a href=')              # Initialize counter start_link with the position of the first <a ref=  
    if start_link == -1:                            # If no <a ref= is found, then it gets a value -1 , so if it comes here, it returns None,0     
        return None, 0
    start_quote = page.find('"', start_link)        # Once it finds the <a ref=... , it looks for the quoted url it it. Here it looks for the start_link from the start_quote. 
    end_quote = page.find('"', start_quote + 1)     # Then, it looks for the next quote which would mark the end of the URL. And that is end_quote.     
    url = page[start_quote + 1:end_quote]           # Then the string between the (start_quote + 1) location and end quote location is the URL   
    return url, end_quote                           # Returns the URL and the end_quote so next time it will search from that location.

# This function just gives all the links found in page. 

def get_all_links(page):                            # Input is the 'content' of the page.    
    links = []                                      # Links is a empty list initialized.   
    while True:                                         
        url, endpos = get_next_target(page)         # Explained above.
        if url:                                     # If there's a URL that gets returns from the function get_next_target()
            links.append(url)                       # 'url' gets appended to the list of the links founds in that page. 
            page = page[endpos:]                    # Delete the part which is already checked. So, page = page[endpos:]  where endpos is the end_quote's position sent from get_next_target()
        else:
            break
    return links                                    # Returns a list of links present in that content of the 'page'.

            
def union(a, b):                                    # a: tocrawl; b: outlinks 
    for e in b:                                     # for every URL ('e') in tocrawl,   
        if e not in a:                              # that 'e' is not in outlinks
            a.append(e)                             # Then, append 'e' to a (tocrawl) 

# Here add_page_to_index() gets previous index, the url & the content as the input.

def add_page_to_index(index, url, content):         
    words = content.split()                         # Here the content is split into words and added to a list called words. 
    for word in words:                              # Then, we traverse the words list and add each words into the index. 
        add_to_index(index, word, url)
 
# Here add_to_index() gets the previous index, the url where the word was found and keyword (read word from previous function) as inputs and output is just the updated index. 
        
def add_to_index(index, keyword, url):               
    if keyword in index:                            # If the 'word' is already in the index, then enters this
        index[keyword].append(url)                  # Look for the index[keyword] and append the URL to this list of URLs.  
    else:                                           # If the 'word' is not present, then create a new [url] list w.r.t to that 'keyword'    
        index[keyword] = [url]

# Lookup function is used to look up all the URLs for a particular 'keyword'

def lookup(index, keyword): 
    if keyword in index:
        return index[keyword]
    else:
        return None

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)
print ranks

#>>> {'http://udacity.com/cs101x/urank/kathleen.html': 0.11661866666666663,
#'http://udacity.com/cs101x/urank/zinc.html': 0.038666666666666655,
#'http://udacity.com/cs101x/urank/hummus.html': 0.038666666666666655,
#'http://udacity.com/cs101x/urank/arsenic.html': 0.054133333333333325,
#'http://udacity.com/cs101x/urank/index.html': 0.033333333333333326,
#'http://udacity.com/cs101x/urank/nickel.html': 0.09743999999999997}




