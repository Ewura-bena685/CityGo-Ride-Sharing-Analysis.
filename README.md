# CityGo Ride-Sharing Data Analysis

## Introduction

CityGo is a ride-sharing platform, and this project was built to help business owners understand what's working and what needs attention. I looked at 1000+ trips to identify revenue patterns, find our most valuable drivers for retention programs, and spot where we're missing customer feedback. The result is a live dashboard that answers key business questions without the fluff.

## The Tools

- **Python** for data processing
- **Pandas** for data manipulation
- **Plotly** for interactive charts
- **Streamlit** for the dashboard interface

## Business Logic

### Commission Model

Most ride-sharing platforms take a cut. Here's ours:

- Trips under or equal to $25: 15% commission
- Trips over $25: 25% commission

This tiering rewards longer or premium rides with better margins.

### Driver Bonus Eligibility

We want to keep our best drivers. A driver qualifies for a bonus when they hit both of these:

- At least 15 completed trips
- Average rating above 4.2 stars

The dashboard flags these drivers so the operations team can reach out with incentives.

### Rating Gap Issue

About 18% of trips come back with no rating (marked as "Not given"). This is a problem because we can't measure driver quality or act on customer issues. The dashboard highlights this as a priority for follow-up.

## Key Findings

- Between 25% and 75% of trips fall into the higher commission tier (fare > $25), meaning revenue is healthy if we focus on trip quality and duration.
- The top 3 riders account for a disproportionate share of trips. Targeting them with loyalty rewards (20% discount vouchers) is a smart retention move.
- Wait times cluster around 6 minutes on average, which is manageable but suggests room for improvement during peak hours.
- The weekend fleet mix shifts toward SUVs and premium vehicles, which aligns with higher fares on weekends.

