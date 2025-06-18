# import necessary libraries
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# set option display view
pd.set_option('display.max_columns', None)  # prevent column truncation in output
pd.set_option('display.width', 500)         # set max display width for DataFrame output

### DATASET: AMAZON REVIEW

# Load dataset and create a copy
df_ = pd.read_csv("amazon_review.csv")
df = df_.copy()

print(df.shape)  # expected result:(4915, 12) rows and columns

print(df.head())  # show first 5 rows

print(df.info())  # check for NaN values

print(df[["reviewerID", "asin", "reviewerName"]].nunique())  # count unique values

# reviewerID is unique for each row: each review belongs to a different user.
# The dataset contains reviews for only one product: we will analyze reviews per product.
# reviewerName is not unique: multiple users can share the same display name.

###################################################################################################################
# TASK 1: Calculate average rating weighted by recent reviews and compare with original average rating.
# Users gave ratings and reviews for a product. We want to weight ratings by review date.
# Then compare original average rating with time-weighted average.

# Step 1: Calculate product's average rating

# Check unique rating values and their frequency to understand rating distribution.
print(df[["overall"]].nunique())
print(df[["overall"]].value_counts())

average_rating = df["overall"].mean()  # 4.5876
print("Original average rating:", average_rating)

# Step 2: Calculate time weighted average rating

# Check unique values and summary stats of 'day_diff' to understand its distribution.
print(df[["day_diff"]].nunique())
print(df["day_diff"].describe())

# Plot histogram of 'day_diff' to visualize the distribution and decide weighting intervals
plt.hist(df["day_diff"])
plt.show(block=True)

# Weights assigned to day_diff intervals based on histogram insights
# The weighting is intuitive to give more importance to recent reviews
# Recent reviews (0-100 days) get highest weight (50), older reviews get progressively less
# This helps highlight current user satisfaction trends
# 0-100 : 50
# 100-200 : 30
# 200-300 : 15
# 300-400 : 4
# 400-700 : 1

# We created a function to calculate a time-based weighted average rating.
# The weights represent our intuitive assumptions about the importance of reviews over time:
# more recent reviews get higher weights because they better reflect the current product quality.
# These weights are set as default parameters but can be adjusted if needed;
def time_based_average_rating(dataframe, w1=50, w2=30, w3=15, w4=4, w5=1):
    return dataframe.loc[dataframe["day_diff"] <= 100, "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > 100) & (dataframe["day_diff"] <= 200), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > 200) & (dataframe["day_diff"] <= 300), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > 300) & (dataframe["day_diff"] <= 400), "overall"].mean() * w4 / 100 + \
           dataframe.loc[(dataframe["day_diff"] > 400) & (dataframe["day_diff"] <= 700), "overall"].mean() * w5 / 100

weighted_avg = time_based_average_rating(df)
print("Time weighted average rating:", weighted_avg)  # 4.7068

# Step 3: Compare the averages
# average_rating = 4.5876
# weighted_average_rating = 4.7068

# Recent reviews have higher ratings.
# User satisfaction may have increased over time.
# Original average is dominated by older reviews, hiding the positive recent trend.
###################################################################################################################

# TASK 2: Select 20 reviews to show on the product detail page.

# Step 1: Create the helpful_no variable.
# total_vote is the total number of up and down votes for a review.
# up votes mean helpful.
# There is no helpful_no variable in the dataset, so we calculate it by subtracting helpful_yes from total_vote.
print(df.head())  # show initial rows to check columns
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

# Step 2:
# Define functions to calculate score_pos_neg_diff, score_average_rating, and wilson_lower_bound.
# Then add these scores to the dataframe.

# Difference between positive and negative votes
def score_pos_neg_diff(up_rating, down_rating):
    return up_rating - down_rating

# Ratio of positive votes to total votes
def score_average_rating(up_rating, all_rating):
    if all_rating == 0:
        return 0  # avoid division by zero
    return up_rating / all_rating

# Wilson Lower Bound score to estimate a conservative lower bound of the confidence interval for the positive vote ratio
def wilson_lower_bound(up_rating, down_rating, confidence=0.95):
    n = up_rating + down_rating
    if n == 0:
        return 0  # avoid division by zero
    z = st.norm.ppf(1 - (1 - confidence) / 2)  # z-score for confidence level
    phat = 1.0 * up_rating / n  # observed positive vote ratio
    return (phat + z*z/(2*n) - z * math.sqrt((phat*(1-phat) + z*z/(4*n))/n)) / (1 + z*z/n)
# Wilson score gives more reliable scores for items with fewer votes

# Calculate and add scores to dataframe
df["score_pos_neg_diff"] = df.apply(lambda row: score_pos_neg_diff(row["helpful_yes"], row["helpful_no"]), axis=1)
df["score_average_rating"] = df.apply(lambda row: score_average_rating(row["helpful_yes"], row["total_vote"]), axis=1)
df["wilson_lower_bound"] = df.apply(lambda row: wilson_lower_bound(row["helpful_yes"], row["helpful_no"]), axis=1)

print(df.head())  # check new columns added

# Step 3: Select the top 20 reviews based on wilson_lower_bound score and sort them
top_20_reviews = df.sort_values("wilson_lower_bound", ascending=False).head(20)
print(top_20_reviews)

# Results interpretation
# The ranking is based on the ratio of positive votes and the total number of votes.
# Recency (day_diff) is not considered in this ranking.
# A hybrid model considering recency can be created to improve the ranking.