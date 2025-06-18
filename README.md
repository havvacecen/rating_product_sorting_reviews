# 🛒 Rating Product & Sorting Reviews in Amazon

This project was completed as part of the **Miuul Data Science Bootcamp**.

---

## 📌 Project Overview

In online shopping, it's important to show fair product ratings and useful reviews.  
A good rating system helps customers trust the product and helps sellers increase sales.

This project focuses on two main goals:
- To calculate a better average rating by giving more weight to recent reviews.
- To find and show the most helpful reviews using a scoring method.

We used review data from a popular electronic product on Amazon.

---

## 📊 Dataset Description

ℹ️ **Note:** The dataset is not included in this repository due to data confidentiality.  
All data operations are done directly in the notebook.

The dataset includes user reviews and ratings for one product.  
Below is a table that explains each variable:

| Variable Name       | Description                                                       |
|---------------------|-------------------------------------------------------------------|
| `reviewerID`        | ID of the reviewer                                                |
| `asin`              | ID of the product                                                 |
| `reviewerName`      | Name of the reviewer (not always unique)                          |
| `helpful`           | Helpfulness score (e.g. [2, 3] means 2 helpful out of 3)          |
| `reviewText`        | Full text of the review                                           |
| `overall`           | Product rating (1 to 5 stars)                                     |
| `summary`           | Short version of the review                                       |
| `unixReviewTime`    | Review time as Unix timestamp                                     |
| `reviewTime`        | Review time in date format                                        |
| `day_diff`          | Days since the review was written                                 |
| `helpful_yes`       | Number of users who found the review helpful                      |
| `total_vote`        | Total number of votes received by the review                      |

---

## ⚙️ Project Workflow

### 🧮 Time-Based Weighted Average Rating

- Checked the distribution of `day_diff` to define time periods
- Gave higher weights to recent reviews
- Calculated a new average score using these weights

### 🗂️ Sorting Reviews by Helpfulness

- Created a new variable: `helpful_no` (not helpful votes)
- Defined and used three scoring methods:
  - `score_pos_neg_diff`: Helpful votes minus not helpful votes
  - `score_average_rating`: Helpful votes divided by total votes
  - `wilson_lower_bound`: A safe score that considers helpful and total votes
- Sorted the reviews by Wilson Lower Bound score to find the top 20

---

## 🛠️ Tools and Libraries Used

- `pandas`: Data handling  
- `matplotlib`: Creating plots  
- `scipy.stats`: Statistical functions  
- `math`: Basic math operations  
- `sklearn.preprocessing`: Scaling data (optional)

---

## 🖥️ Code Structure

The project has two main parts:

### 🔹 Task 1: Rating Calculation  
- Find the average rating  
- Create a time-based average rating  
- Compare both results

### 🔹 Task 2: Review Ranking  
- Create new variables  
- Calculate scores  
- Sort and select the top reviews

---

## 📎 Notes

- This project was done as part of the **Miuul Data Science Bootcamp**.  
- The dataset is not shared in this repository.  
- No CSV file is created. Data is used directly inside the notebook.

---

## 📫 Contact

If you have any questions, suggestions, or just want to say hi — feel free to reach out!

You can find my contact details on my GitHub profile.  
I'm always open to meaningful connections and curious collaborations.
