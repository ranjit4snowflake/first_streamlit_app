import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


#import streamlit

streamlit.title('My Parents New Healthy Diner');

streamlit.header('Breakfast Menu');

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal');

streamlit.text('🥗 Kale Spinach & Rocket Smoothie');

streamlit.text('🐔 Hard-Boiled Free-Range Egg');

streamlit.text('🥑🍞 Avocado Toast');

#import pandas
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');

my_fruit_list=pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt');

my_fruit_list = my_fruit_list.set_index('Fruit');

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries']);
fruits_to_show = my_fruit_list.loc[fruits_selected];

#display the table on the page
streamlit.dataframe(fruits_to_show);

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 #fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
 if not fruit_choice:
  streamlit.error('Please select a fruit to get information.')
 else:
  #streamlit.write('The user entered ', fruit_choice)
  #import requests
  #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  #streamlit.text(fruityvice_response.json())
  # write your own comment -what does the next line do? 
  #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # write your own comment - what does this do?
  streamlit.dataframe(get_fruitvice_data(fruit_choice))

except URLLError as e:
 streamlit.error()
  
streamlit.stop()

#no comments
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")
streamlit.header("The Fruit load list contains: ")
streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to aad?')
streamlit.write('Thanks for adding ', fruit_choice)
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

