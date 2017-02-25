import pandas as pd
import numpy as np
import importlib
import utils.make_heatmap_detroit as make_heatmap

print('Loading data...')

# Load latitudes and longitudes
loc_df = pd.read_csv('./data/latlons.csv', index_col=0)
loc_df.rename(columns={'lat':'Latitude', 'lon':'Longitude'}, inplace=True)

# Load addresses
add_df = pd.read_csv('./data/addresses.csv', index_col=0)

# Load training data
train_df = pd.read_csv('./data/train.csv', usecols=['ticket_id', 'compliance'])
train_df = train_df.set_index('ticket_id')

train_df = train_df.join(add_df)
train_df = train_df.join(loc_df, on = 'address')

# Weight lat/lons by # of appearances
train_df['combined'] = train_df.apply(lambda x: (x.Latitude, x.Longitude), axis = 1)
counts = train_df['combined'].value_counts()
loc_df = pd.DataFrame({'Weight':counts})
loc_df['Latitude'] = loc_df.apply(lambda x: x.name[0], axis = 1)
loc_df['Longitude'] = loc_df.apply(lambda x: x.name[1], axis = 1)

# Filter out NaNs
loc_df = loc_df[np.logical_not(pd.isnull(loc_df.Latitude))]

print('Rendering...')
make_heatmap.render_heatmap(loc_df.copy(), 'data/blight_tickets.html')
print('Done. Output: at data/blight_tickets.html')
