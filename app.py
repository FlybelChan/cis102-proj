import streamlit as st
import math
from datetime import datetime

st.title("CIS102: My 2nd App")
st.markdown("Welcome to my App #2.")
st.header("Slider widget")

x = st.slider('Your number', help="Please choose a number by sliding through the bar")
st.write('$x^2$ = ', x * x)

st.write("---") # line separater

# note `r` before quotation mark below
# it means `\` in the string should be treated as is
# instead of an escape symbol
theta = st.slider(r'θ: Angle in degrees', min_value=-180, max_value=180, step=5)
st.write(r'$Cos( \theta )$ = ', math.cos(theta/180.*math.pi))

st.write("---")

beta = st.slider(r'β: Angle in degrees', value = 30, min_value=-180, max_value=180, step=5)
st.write(r'$Sin( \beta )$ = ', math.sin(beta/180.*math.pi))

st.write("---")
start_time = st.slider(
      "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YYYY - hh:mm")
st.write("Start time:", start_time)

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

######################
# Page Title
######################

# PIL.Image
imageX = Image.open('ft-logo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(imageX, use_column_width=False)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")


######################
# Input Text Box
######################

#st.sidebar.header('Enter DNA sequence')
st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skips the sequence name (first line)
sequence = ''.join(sequence) # Concatenates list to string

st.write("""
***
""")

## Prints  the partial input DNA sequence
st.header('INPUT (DNA Query)')
sequence[:20]+ "<END>"

## DNA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

### 1. Print dictionary
st.subheader('1. Print dictionary')
def DNA_nucleotide_count(seq):
  d = dict([
            ('A',seq.count('A')),
            ('T',seq.count('T')),
            ('G',seq.count('G')),
            ('C',seq.count('C'))
            ])
  return d

X = DNA_nucleotide_count(sequence)

#X_label = list(X)
#X_values = list(X.values())

X

### 2. Print text
st.subheader('2. Print text')
st.write('There are  ' + str(X['A']) + ' adenine (A)')
st.write('There are  ' + str(X['T']) + ' thymine (T)')
st.write('There are  ' + str(X['G']) + ' guanine (G)')
st.write('There are  ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader('3. Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

### 4. Display Bar Chart using Altair
st.subheader('4. Display Bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)  # controls width of bar.
)
st.write(p)

######################
# Import libraries
######################

import pandas as pd
import streamlit as st
from PIL import Image

import math
from datetime import datetime

import pandas as pd

import plotly.express as px
import folium
from streamlit_folium import folium_static


######################
# Page Title
######################

# PIL.Image
image = Image.open('ft-logo.png')

#https://docs.streamlit.io/library/api-reference/media/st.image
st.image(image, use_column_width=False)




@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.header('AireBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))

st.subheader('Selecting a subset of columns')

st.markdown("Streamlit has a [multiselect widget](https://streamlit.io/docs/api.html#streamlit.multiselect) that allows selecting or removing from a list of items. This lets us build a column selector widget for a dataframe.")

cols = ["name", "host_name", "neighbourhood", "room_type", "price"]
st_ms = st.multiselect("Columns", df.columns.tolist(), default=cols)

st.dataframe(df[st_ms].head(10))

st.write("---")

st.markdown("""### Sidebar and price range slider

We use `st.slider` to provide a slider that allows selecting a custom range for the histogram. We tuck it away into a [sidebar](https://streamlit.io/docs/api.html#add-widgets-to-sidebar).""")

values = st.sidebar.slider("Price range", float(df.price.min()), 1000., (50., 300.))
f = px.histogram(df.query(f"price.between{values}", engine="python"),
                 x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)

st.write("---")

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")

# Get "latitude", "longitude", "price" for top listings
toplistings = df.query("price>=800")[["name", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

Top = toplistings.values[0,:]
m = folium.Map(location=Top[1:-1], zoom_start=16)

tooltip = "Top listings"
for j in range(50):
    name, lat, lon, price = toplistings.values[j,:]
    folium.Marker(
            (lat,lon), popup=f"{name}" , tooltip=f"Price:{price}"
        ).add_to(m)

# call to render Folium map in Streamlit
folium_static(m)


st.write("---")

st.markdown("""### Images and dropdowns

Use [st.image](https://streamlit.io/docs/api.html#streamlit.image) to show images of cats, puppies, feature importance plots, tagged video frames, and so on.

Now for a bit of fun.""")

pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg",
    "Cheetah": "img/running-cheetah.jpeg",
    "FT-Logo": "ft-logo.png"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])

st.write("---")

select_col = st.selectbox("Select Columns", list(df.columns), 0)
st.write(f"Your selection is {select_col}")
