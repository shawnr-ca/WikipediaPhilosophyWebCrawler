# WikipediaPhilosophyWebCrawler
Generates graph of Wikipedia search results as first hyperlink is repetitively opened. Most searches lead to the Wikipedia page for Philosophy. This is an interesting way to see how knowledge is organized and related.

User will enter search and web crawler navigates to the article referenced in the first hyperlink. This is done successively until either a loop of searches emerges, or the article
for Philosophy is obtained. After desired number of searches are complete, user enters "TREE" and a flowchart/digraph is availible in PDF form.

Libraries: graphviz, bs4, requests

