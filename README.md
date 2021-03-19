# OSA-Social-Value-Optimization
An algorithm for Optimizing the Social Value of a Market with N sellers and N buyers and a lot of copies of a product.

The algorithm uses a middleman who is deticated to maximise the Social Value of the market above without caring about his own profit.

This middleman is allowed to take an amount of K pairs of sellers and buyers as a sample of the market. But he is using this sample only for knowledge, thus he is not allowed to make transactions with them.

The middleman, after gaining knowledge by the sample market, he is allowed to start interacting with the rest of the market, serially, with seller and buyer pairs. 
He is also allowed to gain knowledge by the pairs that he has left behind him while he is moving through the market.

# To run the code
To run the .py you will need to have python installed, with matplotlib and numpy.
Open a CLI and type the commands below to open python:
```
python
```
Then, import the e17065:
```
import e17065
```
Then, test the algorithm buy giving values to the parameters like the example below:
```
e17065.testTheAlgorithm(100, 1000, 50, 0.02)
```
Where:

- 100: Number of pairs in each Market.
- 1000: Max valuation for each participant.
- 50: Amount of Markets for each possibility step (positive value).
- 0.02: The step for the possibility of each sample Market for each statistical test.
