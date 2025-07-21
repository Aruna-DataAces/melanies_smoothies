# Import python packages
import streamlit as st
import requests

# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie ! :cup_with_straw: ")

name = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be", name)

st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

option = st.selectbox(
    "What is your favourite fruit?",
    ("Banana", "Strawberries", "Mango"),
)
context = st.connection("snowflake")
session = context.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe,
    # default=["Yellow", "Red"],
    max_selections=5
)

# if ingredients_list:
    # st.write("You selected:", ingredients_list)
    # st.text(ingredients_list)

ingredients_string =''
for each_fruit in ingredients_list:
    ingredients_string+=each_fruit+' '
    st.subheader(each_fruit + ' Nutrition Information')
    smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
    # st.text(smoothiefroot_response.json())
    smoothie_fruit_data_frame = st.dataframe(smoothiefroot_response.json(), use_container_width=True)

# st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+name+"""')"""

st.write(my_insert_stmt)
# st.stop()
submit = st.button("Submit Order")

if submit:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
