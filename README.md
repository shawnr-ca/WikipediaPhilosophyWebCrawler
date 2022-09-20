# WikipediaPhilosophyWebCrawler
Generates graph of Wikipedia search results as first hyperlink is repetitively opened. Most searches lead to the Wikipedia page for Philosophy. This is an interesting way to see how knowledge is organized and related.

User will enter search and web crawler navigates to the article referenced in the first hyperlink. This is done successively until either a loop of searches emerges, or the article
for Philosophy is obtained. After desired number of searches are complete, user enters "TREE" and a flowchart/digraph is availible in PDF form.

Libraries/dependencies: graphviz, bs4, requests

Additional Information: This is one of my first projects and any contributions are both encouraged and appreciated.

*Wikipedia articles are frequently altered and as a result, a perpetual loop may be obtained instead of the article for Philosophy, as is the case in the example flowchart* 
