from random import uniform as rand	## uniform distribution
import numpy as np
import matplotlib.pyplot as plt

def createMarket(N = 100, maxValue = 1000):
	""" 
	createMarket() returns a market of Sellers and Buyers.
	Sellers will be ready to sell and buyers will not have the product yet.

	Args:
		N (int): the number of seller - buyer pairs.
		maxValue (int): a maximum value for the valuations of the sellers and the buyers.

	Returns:
		a market

	market:
		- A tuple of Sellers and Buyers

	Sellers (A tuple of Sellers):
		- each seller has a value Wi as a valuation for the product.
		- each seller has a boolean value that indicates if he has the product in his possession.

	Buyers (A tuple of Buyers):
		- each buyer has a value Ui as a valuation for the product.
		- each buyer has a boolean value that indicates if he has got the product or not.
	"""
	buyers = []
	sellers = []
	for i in range(N):
		u = round(rand(0,maxValue),2)
		buyers.append((u,False))
	for i in range(N):
		w = round(rand(0,maxValue),2)
		sellers.append((w,True))
	return (tuple(sellers), tuple(buyers))

def pick(p = 0.5):
	"""
	A function that pics True with a possibility equal to (p*100)%.
	It also pics False with a possibility equal to ((1-p)*100)%.

	Args:
		p (float): the possibility to get True as a return.

	Returns:
		The needed boolean value.
	"""
	a = rand(0,1)	## uniform distribution
	if(a <= p):
		return True
	else:
		return False

def breakMarket(market, p = 0.5):
	"""
	A function that breaks a market, to a sample market and a market ready for run.

	Args:
		market: a market to be broken.
		p (float): the possibility of each pair of seller and buyer to become a sample.

	Returns:
		sampleMarket: the sample of the market.
		readyMarket: the given market without the sample.
	"""
	sellers = market[0]
	buyers = market[1]
	N = len(sellers)
	sampleBuyers = []
	sampleSellers = []
	readyBuyers = []
	readySellers = []
	for i in range(N):
		toSample = pick(p)
		if toSample == True:
			sampleBuyers.append(buyers[i])
			sampleSellers.append(sellers[i])
		else:
			readyBuyers.append(buyers[i])
			readySellers.append(sellers[i])
	sampleMarket = (tuple(sampleSellers),tuple(sampleBuyers))
	readyMarket = (tuple(readySellers),tuple(readyBuyers))
	return sampleMarket, readyMarket

def getAverValuationsOfMarket(market, maxValue = 1000):
	"""
	A function that returns the Average valuations of sellers and buyers in a market.

	If the market has not pairs of Sellers and Buyers then both of the Average 
	valuations will be the halve of the maxValue.

	Args:
		market: a market to get the average valuations.
		maxValue (int): a maximum value to avoid division by zero.

	Returns:
		Average valuation of Sellers.
		Average valuation of Buyers.
	"""
	sellers = market[0]
	buyers = market[1]
	N = len(sellers)
	pSSum = 0
	pBSum = 0
	pS = 0
	pB = 0
	for i in range(N):
		pBSum = pBSum + buyers[i][0]
		pSSum = pSSum + sellers[i][0]
	if(N!=0):
		pB = pBSum/N
		pS = pSSum/N
	else:
		pB = maxValue/2
		pS = maxValue/2
	return round(pS,2), round(pB,2)

def getMinProduct(stock):
	"""
	This function returns the needed minimum valued product by a seller who sold this 
	product to the Mediator.

	Args:
		stock (list): a list of tuples (each tuple - (seller_position, valuation_of_the_seller)).

	Returns:
		The product (tuple) with the minimum valuation.
	"""
	N = len(stock)
	minProduct = stock[0]
	minValuation = stock[0][1]
	for i in range(N):
		if(minValuation >= stock[i][1]):
			minProduct = stock[i]
			minValuation = stock[i][1]
	return minProduct

def updatePrice(averageValue, newValuation, amount):
	""" 
	This function is used to updated the average values of the Mediator with his new
	knowledge by every pair.

	Args:
		averageValue (float): old Average Value.
		newValuation (float): the value to add to consider in the new average value.
		amount (int): Amount of elements counted for the old average value.

	Returns:
		The new Average Value after considering the new valuation.
	""" 
	sumValue = averageValue*amount
	newSum = sumValue + newValuation
	newAmount = amount + 1
	newAverageValue = newSum/newAmount
	return round(newAverageValue, 2)

def runMarket(market, k, pS = 500, pB = 500):
	""" 
	runMarket() runs a market with the values of the Mediator 
	for the Sellers and the Buyers.

	Everytime the Mediator leaves a pair of a seller and a buyer, he updates his
	two prices for the pairs.

	The Mediator sells only the products from the seller with the minimum valuation
	each time so he ends up with higher Social Value.

	If a buyer can buy the product but he values it less than the value of the seller od that
	product, then the Mediator will not sell it to end up with higher Social Value.

	Args:
		market (tuple): (sellers, buyers) - as described in createMarket().
		k (int): the amount of pairs used to get the Average values pS and pB.
		pS (float): the value of the Mediator for purchasing the product from Sellers.
		pB (float): the value of the Mediator for selling the product to Buyers.

	Returns:
		The market after the run.
		The products left on the Mediator with the positions of the Sellers who sold them.
	"""
	N = len(market[1])
	sellers = []
	buyers = []
	stock = []
	for i in range(N):
		if(market[0][i][0] <= pS):
			stock.append((i,market[0][i][0]))
			sellers.append((market[0][i][0],False))
		else:
			sellers.append((market[0][i][0],True))
		if((market[1][i][0] >= pB) and (len(stock) != 0)):
			minProduct = getMinProduct(stock)
			if(minProduct[1] <= market[1][i][0]):
				stock.remove(minProduct)
				buyers.append((market[1][i][0],True))
			else:
				buyers.append((market[1][i][0],False))
		else:
			buyers.append((market[1][i][0],False))
		pS = updatePrice(pS, market[0][i][0], k)
		pB = updatePrice(pB, market[1][i][0], k)
		k += 1
	return (tuple(sellers), tuple(buyers)), tuple(stock)

def showResults(market, stock = -1):
	"""
	This is a function for testing purposes.
	It is getting used by the demonstration() function ti make printings in the console.

	Args:
		market: a market.
		stock: a stock of the Mediator of the market.

	Returns:
		printings: outputs the sellers with the buyers.
		(also prints the stock with its values if given).
	"""
	sellers = market[0]
	buyers = market[1]
	N = len(sellers)
	for i in range(N):
		print('[ ',sellers[i][0],' | ',sellers[i][1],' ] - [ ',buyers[i][0],' | ',buyers[i][1],' ]')
	if(stock == -1):
		return
	for i in range(len(stock)):
		print('[ ',stock[i][0],' - ',stock[i][1],' ]')
	return

def maxSocialValue(market):
	"""
	This is used to find the best possible Social Value in a market.

	To find the maximum Social Value it sorts the valuations of all the people in the market
	and then it sums the highest N values.

	Args:
		market: a market.

	Returns:
		The maximum Social Value.
	"""
	people = []
	sellers = market[0]
	buyers = market[1]
	N = len(sellers)
	for i in range(N):
		people.append(sellers[i][0])
	for i in range(N):
		people.append(buyers[i][0])
	people.sort(reverse=True)
	socialValue = 0
	for i in range(N):
		socialValue += people[i]
	return round(socialValue, 2)

def trueSocialValue(market):
	"""
	This function is used to find the actual Social Value of the given market.

	To find this value, it sums the valuations of all people who have the product.

	Args:
		market: a market.

	Returns:
		The Social Value.
	"""
	sellers = market[0]
	buyers = market[1]
	N = len(sellers)
	socialValue = 0
	for i in range(N):
		if(sellers[i][1] == True):
			socialValue += sellers[i][0]
		if(buyers[i][1] == True):
			socialValue += buyers[i][0]
	return round(socialValue, 2)

def betterSocialValue(market, stock):
	"""
	betterSocialValue() finds the Social Value, after giving back the stock of the
	Mediator to the sellers whom their products stayed in the posetion of the Mediator.

	To find this value, it sums the trueSocialValue() of the market with the valuations
	of the sellers who got back their products.

	Args:
		market: a market.

	Returns:
		The better Social Value.
	"""
	socialValue = trueSocialValue(market)
	N = len(stock)
	for i in range(N):
		socialValue += stock[i][1]
	return round(socialValue, 2)

def testAMarket(N=100, maxValue=1000, possibilityOfSample = 0.27):
	"""
	This function is using any other non demonstrating function in this .py file to run the tests.

	Args:
		N (int): the number of seller - buyer pairs.
		maxValue (int): a maximum value for the valuations of the sellers and the buyers.

	Returns:
		The Max Social Value of a market, as described in maxSocialValue().
		The True Social Value of a market, as described in trueSocialValue().
		The Better Social Value of a market, as described in betterSocialValue().
	"""
	market = createMarket(N,maxValue)
	sampleMarket, readyMarket = breakMarket(market, possibilityOfSample)
	pS, pB = getAverValuationsOfMarket(sampleMarket, maxValue)
	marketAfterRun, stock = runMarket(readyMarket, len(sampleMarket[0]), pS, pB)
	return maxSocialValue(readyMarket), trueSocialValue(marketAfterRun), betterSocialValue(marketAfterRun, stock)

def demonstration():
	"""
	This function is made for demonstrating perposes.
	To use it, run this function alone in the main() and read this .py file.

	Args:
		None.

	Returns:
		Printings of an example of the above code (in the console).
	"""
	## My settings
	N = 10
	maxValue = 100
	possibilityOfSample = 0.3

	## Making of the market
	market = createMarket(N,maxValue)
	print("The market:")
	showResults(market)

	## Breaking the market
	sampleMarket, readyMarket = breakMarket(market, possibilityOfSample)
	print()

	## Results from the sample of the market
	print("The sample market:")
	showResults(sampleMarket)
	pS, pB = getAverValuationsOfMarket(sampleMarket, maxValue)
	print('Seller Average price = ',pS)
	print('Buyer Average price = ',pB)
	print()

	## Show the results for the market after the run
	marketAfterRun, stock = runMarket(readyMarket, len(sampleMarket[0]), pS, pB)
	print("The ready market after the run:")
	showResults(marketAfterRun, stock)
	print()

	## Show the results for the market after the run
	print('Best Social Value: ', maxSocialValue(readyMarket))
	print('Social Value Got: ', trueSocialValue(marketAfterRun))
	print('Better Social Value Got: ', betterSocialValue(marketAfterRun, stock))
	
	## Ending
	return

def testTheAlgorithm(N = 100, maxValue = 1000, amountOfTests = 10, possibilityStep = 0.01):
	"""
	This function is testing the success of the Algorithm.
	To use it, run this function alone in the main() and read this .py file.

	It will run for each number of sample market possibility (e.g. 0, 0.01, 0.02, ... , 0.99, 1.00)
	----It will find Ep[SW(N\So)]
	----It will find Ep[SW*(N\So)]
	----It will find Ep[W+SW(N\So)]

	after that,

	It will run again for all the statistical tests that happend, and
	----It will find the success rate based on Ep[SW(N\So)]/Ep[SW*(N\So)]
	----It will find the success rate based on Ep[W+SW(N\So)]/Ep[SW*(N\So)]

	then,

	It will make a figure and save it in this directory.

	Args:
		N (int): Number of pairs in each Market.
		maxValue (int): Max valuation for each participant.
		amountOfTests (int): Amount of Markets for each possibility step (positive value).
		possibilityStep (float): The step for the possibility of each sample Market for each statistical test.

	Returns:
		A figure with the Success Rate Results.
	"""
	amountOfStatisticalTests = 1/possibilityStep + 1
	possibilityOfSample = 0
	possibilityList = []
	bestSV = []
	trueSV = []
	betterSV = []
	for i in range(int(amountOfStatisticalTests)):
		possibilityList.append(round(possibilityOfSample,3))
		bestSum = 0
		trueSum = 0
		betterSum = 0
		for j in range(amountOfTests):
			a, b, c = testAMarket(N, maxValue, possibilityOfSample)
			bestSum += a
			trueSum += b
			betterSum += c
		averageBestSocialValue = bestSum/amountOfTests
		averageTrueSocialValue = trueSum/amountOfTests
		averageBetterSocialValue = betterSum/amountOfTests
		bestSV.append(averageBestSocialValue)
		trueSV.append(averageTrueSocialValue)
		betterSV.append(averageBetterSocialValue)
		possibilityOfSample += possibilityStep

	successTrueRate = []
	successBetterRate = []
	for i in range(int(amountOfStatisticalTests)):
		trueRate = 0
		betterRate = 0
		if(bestSV[i]!=0):
			trueRate = trueSV[i]/bestSV[i]
			betterRate = betterSV[i]/bestSV[i]
		successTrueRate.append(round(trueRate,4))
		successBetterRate.append(round(betterRate,4))
	## print(successTrueRate)		## this will show the result for the true success rate in the console (for each statistical test of every possibility)
	## print(successBetterRate)		## this will show the result for the better success rate in the console (for each statistical test of every possibility)

	fig = plt.figure(1)	## identifies the figure 
	plt.title("Success of the Algorithm", fontsize='12')
	plt.xlabel("Possibility of Sample (p)",fontsize='11')
	plt.ylabel("Success Rate",fontsize='11')
	plt.plot(possibilityList, successTrueRate, "-b", label="Ep[SW(N\So)]/Ep[SW*(N\So)]")		## plot the success rate with the true Social Value
	plt.plot(possibilityList, successBetterRate, "-g", label="Ep[W+SW(N\So)]/Ep[SW*(N\So)]")	## plot the success rate with the better Social Value
	plt.legend(loc="lower left")
	plt.grid()	#shows a grid under the plot
	plt.savefig('e17065.png')	#saves the figure in the present directory
	plt.show()
	return

def main():
	N = 200							## Number of pairs in each Market.
	maxValue = 10000				## Max valuation for each participant.
	amountOfTests = 100				## Amount of Markets for each possibility step (positive value).
	possibilityStep = 0.01			## The step for the possibility of each sample Market for each statistical test.

	testTheAlgorithm(N, maxValue, amountOfTests, possibilityStep)

	return

if __name__ == "__main__":
    main()