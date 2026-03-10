import numpy as np
import pandas as pd

#Box-Muller transformation 

#ressources

#https://mathworld.wolfram.com/Box-MullerTransformation.html

#https://www.youtube.com/watch?v=YhLokU9qDj4

#https://numpy.org/doc/2.1/reference/random/generated/numpy.random.normal.html

#https://numpy.org/devdocs/reference/random/generated/numpy.random.seed.html

#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html


#setup

# unprompted
# mean was ~2.45, variance ~0.21
mean_unprompted = 2.453125
standev_unprompted = np.sqrt(0.21015625) # stand dev is just sqrt(variance)

# prompted
# mean ~2.73, variance ~0.84 
mean_prompted = 2.734375
standev_prompted = np.sqrt(0.8372395833)

# target num of experts
target_n = 100

#seed to make it reproducible (to get the same random numbers every time)
np.random.seed(42)

# generate raw scores using a normal distribution
raw_unprompted = np.random.normal(mean_unprompted, standev_unprompted, target_n)
raw_prompted = np.random.normal(mean_prompted, standev_prompted, target_n)

# cleanup

# round to nearest 0.25
round_val= 0.25

clean_unprompted = np.round(raw_unprompted / round_val) * round_val
clean_prompted = np.round(raw_prompted / round_val) * round_val

# clip to 1-5 after rounding
clean_unprompted = np.clip(clean_unprompted, 1, 5)
clean_prompted = np.clip(clean_prompted, 1, 5)

# generate expert ids (1 to 200)
ids_group1 = [f"Fake_Expert{i}" for i in range(1, target_n + 1)]
ids_group2 = [f"Fake_Expert{i}" for i in range(target_n + 1, (target_n * 2) + 1)]

# organize into two staggered dataframes

# first group (unprompted)
df_1 = pd.DataFrame({
    'Expert_ID': ids_group1,
    'Unprompted_Scores': clean_unprompted,
    'Prompted_Scores': [np.nan] * target_n
})

# second group (prompted)
df_2 = pd.DataFrame({
    'Expert_ID': ids_group2,
    'Unprompted_Scores': [np.nan] * target_n,
    'Prompted_Scores': clean_prompted
})

# combine
df = pd.concat([df_1, df_2], ignore_index=True)

# save
output_filename = 'hypothetical_expert_data.csv'
df.to_csv(output_filename, index=False)


