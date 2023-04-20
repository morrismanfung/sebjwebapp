# Simple and Easy Blackjack Bankroll Magement Application

## Overview

Welcome, advantage players! This is the first free online Blackjack bankroll managment application. If you are hesitating whether to purchase CVCX or the BJA Pro Betting Software in the early stage of your counting journey, you may want to try out this web app.

If you are already a pro in Blackjack, I will advise you to use either CVCX or the BJA Pro Betting Software. They are designed with a simulation approach and with more advanced statistics. This web app is using a theoretical approach, which results should be treated as approximations (at least in the current stage) if you are going serious in card counting.

## Why do we need bankroll management

A successful card counting career consist of the followings: basic strategy, counting techniques, and a betting scheme. A betting scheme is important as advantage players should know how to adjust their bets based on their advantage and possible risk.

Bankroll managment involves managing both expected return and risk.

In professional blackjack, players gain an edge when the count is high. Still, the advantage may varies based on different rules. To calculate one's expected return, one needs to specify their betting scheme and the rules provided in the casinos. An estimation of expected return is crucial as one needs to know whether their effort really pays and consider their opportunity cost. Expected return evaluate how profitable a betting scheme is, giving advantage players a direct measurement of the value of their play. The expected return is often referred as the *expected value* in other literatures.

While players do have an advantage with card counting, variance in Blackjack is inherently large. The positive mean return is accompanied with a large variance that could end any new counters' career in the early stage. Counting card without knowing the risk in prior is dangerious. Before starting to count cards, one should know the probable range of return as one is NOT GUARANTEED to win in every session. If one encounters to negative variance, it is also with a chance for one to lose all of their bankrool. The corresponding probability is also known as the *risk of ruin* in gambling and statistics.

## How is Expected Value and Risk represented

The application takes rules, betting scheme, number of rounds per hour (as the speed) as input. It will return the expected value per round, expected value per hour, and the normalized advantage represented in expected value in percentage of the average bet.

The application does not only return the standard deviation and distribution chart as they are not easy to interpret. We present the risk of ruin given the user's specified bankroll. To present a more simple interpretation, we also present the worst case scenarios with probability 1%, 5%, 10%, and 50%.

Reference of the statsitics used can be found in our [proposal](proposal.md).

## Usage

1. Specify the rules of your blackjack game using the checkboxes. This will determine the the base advantage of the house.

2. Specify your own bet spread (i.e., betting strategy). Please note the players' advantage with each count is estimated roughly using the heuristic of +0.5% advantage for each unit increase in the count.

3. Specify your bankroll (i.e., the amount of money you prepare for card counting), hour (i.e., usually the amount of time for 1 trip), and the number of rounds per hour. These will be used for risk estimation.

4. Adjust your bet spread so that your expected return and risk become reasonable. Please also be reminded to use a bet spread that will not draw much attention from the casino!

## License

The software is licensed under the [MIT license](LICENSE).
