# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

st.stop()
This code assumes that your orders table has two columns: ingredients and name_on_order. If the table schema is different, you'll need to adjust the column names and the insert statement accordingly.

Let me know if this helps or if you need further assistance!


Edit in Pages



AI-generated content may be incorrect
You said:

edit the below code accordingly:

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

#from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

#convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )
import requests

if ingredients_list:
    ingredients_string =''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
   
        st.success('Your Smoothie is ordered!', icon="✅")
st.stop()
Copilot said:
Copilot
Here's the updated code to ensure the insert statement matches the table schema and to fix the issue with the multiselect widget:

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """
    
    st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

st.stop()

