# Proposal

## Motivation and Purpose

Betting strategy and bankroll managment are of paramount importance for advantage player in Blackjack. Card counting invovles estimating the player's edge before a specific round starts. When an advantage player has the edge, they should put a bigger bet on the table. To become a successful card counter, one essential step is to determine one's betting scheme, i.e., how much bigger should one bet given a specific count and the advantage. The optimal bet spread is not only for maximizing expected gain, but is also for the optimization of the balance between winnings, risks, and feasibility.

The current web app aims to provide a free and simple calculator to examine the expected gain and variance of return based on one's customized betting strategy. Currently, there are 2 paid software by [Blackjack Apprenticeship](https://www.blackjackapprenticeship.com/cvcx-blackjack-betting-software/) and [QFIT](https://www.qfit.com/blackjack-simulation.htm). The current web app aims to provide an approximation to players' return and variance using a theoretical approach. The current project is not a full replacement to existing paid softwares (because they are AWESOME) but a free substitute for players who just start card counting. Both of the paid softwares use a simulation-based calculation which give more accurate results.

## Statistics Used

Currently the web app is only for Hi-Lo users.

Count frequencies are extracted from [QFIT CVCX Online Viewer](https://www.qfit.com/cvcxonlineviewer.htm).

Base house edge is estimated with the chart in [Blackbet in Blackjack: Playing 21 as a Martial Art](https://www.amazon.com/Blackbelt-Blackjack-Playing-Martial-Art/dp/1580421431) Chapter 6.

Variance is extracted from [Variance in Blackjack on The Wizard of Odds](https://wizardofodds.com/games/blackjack/variance/).

## Use Case Scenario

The webapp is designed for advantage players who are using the Hi-Lo system. Users are supposed to know the basic rules of Blackjack, the basic strategy of Blackjack, Hi-Lo counting, and true count conversion. The webapp is not designed for players to learn how to play Blackjack but for players to determine how to optimize their betting strategy.

Below are some of the goals that our potential users will want to achieve.

- What is the expected gain per hour with my current betting strategy?
- What are the risk and worst case scenarios with my current betting strategy?
- What is my risk of ruin?
- How will my bankroll evolve across time given the current betting strategy?
