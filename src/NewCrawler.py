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

def crawl_web(seed, max_pages): # returns index, graph of inlinks || Added a max_pages variable that breaks out of the loop when the number of max pages is exceeded. 
    number_of_pages = 0
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl:                                      # while the tocrawl list is not empty
        page = tocrawl.pop()
        print page                                        # Uncomment this to see what all pages are getting crawled
        number_of_pages = number_of_pages + 1                            # Pops the last entered URL in the tocrawl list  
        if page not in crawled:                         # Checks if the page is not already traversed. If it is, skips this if loop and goes back to 'while tocrawl'
            content = get_page(page)                    # Explained below. 
            add_page_to_index(index, page, content)     # Explained below. 
            outlinks = get_all_links(content)           # Explained below.
                       
            graph[page] = outlinks                      # 'page' is the keyword and for that it attaches it to a list outlinks.
            
            union(tocrawl, outlinks)                    # Check if the links that are present in 'outlinks' are also there is 'tocrawl' , if not , it'll add/append them to 'tocrawl' list.
            crawled.append(page)                        # Appends the whole page (content) to the string 'crawled'
           
        if (number_of_pages == max_pages):
                break
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

# For 1, normal crawl_web. 
# index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')

# For 2, with Max_pages  
index, graph = crawl_web ('http://xkcd.com/', 30)

# Let's try with wikipedia 
# index, graph = crawl_web ('http://en.wikipedia.org/wiki/Language', 2)
ranks = compute_ranks(graph)
print ranks

#--------------------------------Looking up of words like from a search engine---------------------------------------#

word_url = lookup(index, 'fund')
# word_url = lookup(index,'money')                     # word_url is a list of URLs
print word_url



# Output for 1. 

#>>> {'http://udacity.com/cs101x/urank/kathleen.html': 0.11661866666666663,
#'http://udacity.com/cs101x/urank/zinc.html': 0.038666666666666655,
#'http://udacity.com/cs101x/urank/hummus.html': 0.038666666666666655,
#'http://udacity.com/cs101x/urank/arsenic.html': 0.054133333333333325,
#'http://udacity.com/cs101x/urank/index.html': 0.033333333333333326,
#'http://udacity.com/cs101x/urank/nickel.html': 0.09743999999999997}

# Output for 2. With Max_pages = 4
# {'legalcode': 0.07066666666666666, '#': 0.07066666666666666, 'http://xkcd.com/': 0.04999999999999999, 'http://creativecommons.org/licenses/by-nc/2.5/': 0.05166666666666665}

# Output when max_pages = 10
# {'http://www.topatoco.com/merchant.mvc?Screen=PROD&Store_Code=TO&Product_Code=BF-COMIC-PRINTS&Category_Code=BF&Product_Attributes[1]:value=132 - can opener': 0.0314074074074074, 'http://www.topatoco.com/merchant.mvc?Screen=PRIVACY&Store_Code=TO': 0.0237864310043809, 'rss-id': 0.0314074074074074, 'http://www.buttercupfestival.com/': 0.022962962962962956, '#': 0.0314074074074074, 'http://xkcd.com/': 0.022222222222222216, 'http://creativecommons.org/licenses/by-nc/2.5/': 0.022962962962962956, 'legalcode': 0.0314074074074074, 'https://www.topatoco.com/merchant.mvc?Session_ID=47e1bc593d827441fedeaf19ec3c25b3&Screen=ORHL&Store_Code=TO': 0.024727191448566523}

# Output for max_pages = 20
# {'http://www.topatoco.com/merchant.mvc?Screen=PROD&Store_Code=TO&Product_Code=BF-COMIC-PRINTS&Category_Code=BF&Product_Attributes[1]:value=132 - can opener': 0.020190476190476186, '#': 0.020190476190476186, 'rss-id': 0.020190476190476186, 'http://www.topatoco.com/merchant.mvc?Session_ID=c070fd7af643dc6de9dd71bad58f3f99&Screen=PRIVACY&Store_Code=TO': 0.016003865383724617, 'https://www.topatoco.com/merchant.mvc?Session_ID=c070fd7af643dc6de9dd71bad58f3f99&Screen=JOIN&Store_Code=TO': 0.014925868920894462, 'http://www.buttercupfestival.com/': 0.014761904761904757, 'http://www.topatoco.com/merchant.mvc?Screen=PRIVACY&Store_Code=TO': 0.01771001707776763, 'http://xkcd.com/': 0.014285714285714282, 'http://creativecommons.org/licenses/by-nc/2.5/': 0.014761904761904757, 'legalcode': 0.020190476190476186, 'http://www.topatoco.com/merchant.mvc?Screen=WHOLESALE': 0.014925868920894462, 'https://www.topatoco.com/merchant.mvc?Session_ID=4b50a3f647afc721bec9045e399f788b&Screen=ORHL&Store_Code=TO': 0.015875537517107022, 'http://www.topatoco.com/merchant.mvc?Session_ID=c070fd7af643dc6de9dd71bad58f3f99&Screen=ABOUT&Store_Code=TO': 0.016003865383724617, 'https://www.topatoco.com/merchant.mvc?Session_ID=c070fd7af643dc6de9dd71bad58f3f99&Screen=ORHL&Store_Code=TO': 0.01844209381404054}
# Has only 14 urls here. 