import graphviz as gv
import requests
from bs4 import BeautifulSoup
from bs4 import element


def ExtractName(Current):     #Function to take name of Wiki Article from URL
	Next = str(Current)[6:]
	return Next

def ExtractHERF(string):   #Create HERF link from string
    NewString = ""
    for char in string:
        if char == " ":
            char = "_"
        if char == ",":
            break
        else:
            NewString += char
    return NewString

def Remove_(text):     #Function to return text without underscore ("_")
	TEXT = ""
	for char in text:
		if char == "_":
			TEXT += " "
		else:
			TEXT += char
	return TEXT

def FixEntry(Entry):     #Function to change user input to searchable URL format for request
	Fixed = ""
	for char in range(len(Entry)):
		newchar = Entry[char]
		if char == 0:
			newchar = Entry[char].upper()
		elif Entry[char-1] != " " and Entry[char].isupper():
			newchar = Entry[char].lower()
		if Entry[char-1] == " ":
			newchar = Entry[char].upper()
		if Entry[char] == " ":
			newchar = "_"
		Fixed += newchar
	return Fixed

def AddBlankLine(string, num):
    StringLen = len(string)
    NewString = str(num) + " "
    StringList = []
    count = 0
    for char in string:
        count += 1
        if char == "\n" or count == StringLen:
            num += 1
            StringList.append(NewString)
            NewString = str(num) + " "
        else:
            NewString += char
    StringList[-1] += string[-1]
    return StringList

def CheckREDIRECT(Wiki):  #Function to account for wikipedia articles that are incomplete and intended to redirect you to correct article
	FirstWikiPageRequest0 = requests.get(url="https://en.wikipedia.org/wiki/" + Wiki)
	FirstWikiPage0 = BeautifulSoup(FirstWikiPageRequest0.content, "html.parser")
	FirstHyperLink0 = FirstWikiPage0.find(id="bodyContent").find_all("p")
	NewWiki = ""
	for item in FirstHyperLink0:
		if "#REDIRECT" in str(item):
			item1 = str(item)
			for char in range(len(item1)):
				if item1[char-12:char] == '''href="/wiki/''':
					item2 = item1[char:]
					for CHAR in range(len(item2)):
						if item2[CHAR] == '''"''':
							print(NewWiki)
							return NewWiki
						NewWiki += item2[CHAR]
	if len(NewWiki) == 0:
		return False

def CheckBrackets(string, index):
    BrackLeftScore = 0
    BrackRightScore = 0
    for char in string[:index]:
        if char == "(":
            BrackLeftScore += 1
        if char == ")":
            BrackLeftScore += -1
    for char in string[index:]:
        if char == "(":
            BrackRightScore += 1
        if char == ")":
            BrackRightScore += -1
    if BrackRightScore + BrackLeftScore == 0 and BrackRightScore != 0 and BrackLeftScore != 0:
        return True
    else:
        return False

def NewSearch(WIKI, CAT):  #Function to redirect search when user search input yields multiple results
	CatNum = 0
	FirstWikiPageRequest1 = requests.get(url="https://en.wikipedia.org/wiki/" + WIKI + "#" + CAT)
	WikiParsed = BeautifulSoup(FirstWikiPageRequest1.content, "html.parser")
	WikiParsedFilt1 = WikiParsed.find("div", class_ = "toc").find_all("li")

	for i in WikiParsedFilt1:
		CatNum += 1
		if CAT in i.text:
			break
	if CatNum > 1:
		CatNum += 1
	WikiParsedFilt = WikiParsed.find(class_="mw-parser-output").find_all("ul")[CatNum]
	print("\n" + CAT + ":\n")
	ResultNum = 1
	ResultList = []
	for i in WikiParsedFilt:
		if type(i) is not element.NavigableString:
				if str(i).count("href") > 1:
					ResultList += AddBlankLine(str(i.text),ResultNum)
					ResultNum += str(i).count("href")
					print("\n")
					for j in i:
						#print(j.text + str(len(j)) + str(type(j)))
						if type(j) is not element.NavigableString:
							RedirectLink = j.get("href")
							if RedirectLink == None:
								RedirectLink = j.find(href = True).get("href")
				elif str(i).count("href") == 1:
					RedirectLink = i.get("href")
					if RedirectLink == None:
						RedirectLink = i.find(href=True).get("href")
					ResultList += AddBlankLine(str(i.text), ResultNum)
					ResultNum += 1
	for result in ResultList:
		print(result)
		print("\n")
	UserIn = input("Above are the available Wikipedia articles from the selected category. Please select an option by entering its corresponding number.")
	for result in ResultList:
		if UserIn == result[0] or UserIn in result:
			HERF = ExtractHERF(result[2:])
	return HERF



print('''This program takes in the name of a wikipedia article and then the name of the article corresponding to its first hyperlink. It does this iteratively, until the wikipedia article for "Philosophy" is reached. This is based on the observation that applying this algorithm for any Wikipedia entry will yield "Philosophy". In the end a tree connecting each entry is constructed.''' + "\n")
FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
FirstArticle = FixEntry(FirstArticle)


def SearchWiki(Start):    #Function that searches Wikipedia and requests HTML data (first hyperlink*)
	FirstWikiPageRequest = requests.get(url="https://en.wikipedia.org/wiki/" + str(Start))
	FirstWikiPage = BeautifulSoup(FirstWikiPageRequest.content, "html.parser")
	FirstHyperLink = FirstWikiPage.find(id="bodyContent").find_all("p")

	if len(FirstHyperLink) == 1:
		if "may refer to:" in str(FirstHyperLink):
			try:
				Categories = FirstWikiPage.find("div", class_ = "tocright").find_all("li")
				CatList = []
			except:
				return None
			for cat in Categories:
				print(cat.text)
				CatList.append(cat.text)
			User_Cat = input("\n" + "This search yields multiple results. In which of the above categories was your search intended? ")
			for cat in CatList:
				if cat[0] == User_Cat or cat[2:].lower() in User_Cat.lower():
					UserIn = NewSearch(Start, cat[2:])
					FirstWikiPageRequest = requests.get(url="https://en.wikipedia.org/wiki/" + UserIn)
					FirstWikiPage = BeautifulSoup(FirstWikiPageRequest.content, "html.parser")
					FirstHyperLink = FirstWikiPage.find(id="bodyContent").find_all("p")
	ExitBool = False
	for i in FirstHyperLink:
		if i.find(href = True) != None:
			for j in i:
				if ExitBool == True:
					break
				if type(j) == element.Tag:
					HERF = j.get("href")
					if HERF != None:
						FirstPText = i.text
						TITLE = j.text
						FirstInst = str(FirstPText).find(TITLE)
						InBrack = CheckBrackets(FirstPText,FirstInst)
						if "wiktionary" not in HERF and "Help:Pronunciation" not in HERF and InBrack == False:
							HREF_Pres = True
							NextArt = ExtractName(HERF)
							if HREF_Pres == True:
								return NextArt
	CheckEmpty = FirstWikiPage.find(id="content").find_all("li")
	for i in CheckEmpty[0]:
		if type(i) is not element.NavigableString and i.get("href") != None:
			NewLink = i.get("href")
			if str(NewLink).count("/wiki/") == 1:
				NextArt = NewLink[6:]
			else:
				NextArt = NewLink[1:]
			return NextArt


def CreateFlow(CombList):
	G_Wiki = gv.Digraph(name="WikipediaWebCrawlerFlowchart", format="pdf")
	G_Wiki.attr(concentrate = "true", overlap = "false", splines = "true")
	for list in CombList:
		for index, i in enumerate(list):
			if index != 0:
				G_Wiki.node(Remove_(str(list[index])))
				G_Wiki.node(Remove_(str(list[index - 1])))
				G_Wiki.edge(Remove_(str(list[index])), Remove_(str(list[index - 1])))
			if index == len(list) - 1:
				G_Wiki.node(Remove_(str(list[index])),color = "blue", style = "filled")
			if i == "Philosophy":
				G_Wiki.node(Remove_(str(list[index])), color="red", style="filled", shape = "star")
	G_Wiki.view()

	G1_Wiki = gv.Digraph(name="WikipediaWebCrawlerFlowchart1", format="pdf")
	G1_Wiki.attr(concentrate="true", overlap="false", splines = "ortho", center = "true")
	for list in CombList:
		for index, i in enumerate(list):
			if index != 0:
				G1_Wiki.node(Remove_(str(list[index])))
				G1_Wiki.node(Remove_(str(list[index - 1])))
				G1_Wiki.edge(Remove_(str(list[index])), Remove_(str(list[index - 1])))
			if index == len(list) - 1:
				G1_Wiki.node(Remove_(str(list[index])), color="green", style = "filled")
			if i == "Philosophy":
				G1_Wiki.node(Remove_(str(list[index])), color="red", style="filled", shape="star")
	G1_Wiki.view()




CombList = []

def SequentialSearchFlowChart(FirstArticle):
	PhilBool = False
	Initial = FirstArticle
	Initial0 = Initial
	count = 0
	ArtList = []
	while PhilBool == False:
		if str(Initial) == "None":
			try:
				ResultCR = CheckREDIRECT(ArtList[-3])
				if ResultCR != False:
					Initial = ResultCR
				elif ResultCR == False:
					print("ERROR")
			except:
				print("This search is invalid and yields an error. Refine your search or try another... ")
				FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
				SequentialSearchFlowChart(FirstArticle)
		Initial = SearchWiki(Initial)
		if str(Initial) != "None" and str(Initial)[:2] != "a:":
			print(Remove_(str(Initial)))
			count += 1
		if Initial == "Philosophy":
			TREElist = []
			for wiki in ArtList:
				TREElist.insert(0, wiki)
			if Initial0 not in TREElist:
				TREElist.append(Initial0)
			TREElist.insert(0,"Philosophy")
			if TREElist not in CombList:
				CombList.append(TREElist)
			print("\n" + "The search is complete.")
			print("It took " + str(count) + " searches to get to the Wikipedia page for Philosophy when starting with the " + Initial0 + "  Wikipedia article.")
			UserExit = input('''Press enter to Exit or the space bar and then enter to restart. If you would like to view the tree representing the results of all your searches, type "TREE" and then enter. ''')
			if UserExit == " ":
				FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
				SequentialSearchFlowChart(FirstArticle)
			if UserExit == "TREE":
				CreateFlow(CombList)
				FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
				SequentialSearchFlowChart(FirstArticle)
			PhilBool = True
		if Initial in ArtList:
			TREElist1 = []
			for wiki in ArtList:
				TREElist1.insert(0,wiki)
			if Initial0 not in TREElist1:
				TREElist1.append(Initial0)
			if TREElist1 not in CombList and TREElist1[0] != None:
				CombList.append(TREElist1)
			print("\n" + "This search leads to a loop of searches and will never yield the Wikipedia page for Philosophy.")
			print("It took " + str(count) + " searches to obtain this result.")
			UserExit = input('''Press enter to Exit or the space bar and then enter to complete another search.  If you would like to view the tree representing the results of all your searches, type "TREE" and then enter.''')
			if UserExit == " ":
				FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
				SequentialSearchFlowChart(FirstArticle)
			if UserExit == "TREE":
				CreateFlow(CombList)
				FirstArticle = str(input("What is the Wikipedia article you would like to start with? "))
				SequentialSearchFlowChart(FirstArticle)
			PhilBool = True
		ArtList.append(Initial)

SequentialSearchFlowChart(FirstArticle)