# WikipediaPhilosophyWebCrawler
Generates graph of Wikipedia search results as first hyperlink is repetitively opened. Most searches lead to the Wikipedia page for Philosophy. This is an interesting way to see how knowledge is organized and related.

User will enter search and web crawler navigates to the article referenced in the first hyperlink. This is done successively until either a loop of searches emerges, or the article
for Philosophy is obtained. After desired number of searches are complete, user enters "TREE" and a flowchart/digraph is availible in PDF form.

Libraries/dependencies: graphviz, bs4, requests

Additional Information: This is one of my first projects and any contributions are both encouraged and appreciated.

*Wikipedia articles are frequently altered and as a result, a perpetual loop may be obtained instead of the article for Philosophy* 

Examples:

![WikipediaWebCrawlerFlowchart1 gv (5)-1](https://user-images.githubusercontent.com/113395566/192914688-d0b5bff0-7463-4e89-92db-7af85d3af538.png)
![WikipediaWebCrawlerFlowchart1 gv (4)-1](https://user-images.githubusercontent.com/113395566/192914182-1957b777-6b7f-424c-b0b7-8a2bb2ec5da0.png)
