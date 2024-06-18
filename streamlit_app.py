# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

#get DataFrame
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


# Titre
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

# Command name
name_on_order = st.text_input('Name of Smoothie :')
st.write(name_on_order)
    #drop-down
ingredients_list = st.multiselect('Choose up to 5 ingredients',my_dataframe,max_selections=5)



if ingredients_list:    
  ingredients_string = ''
    
  for fruit_choosen in ingredients_list:
    ingredients_string += fruit_choosen + ' '

  my_insert_stmt = """insert into smoothies.public.orders (order_id,ingredients,name_on_order,order_filled)
    values(order_id_seq.NEXTVAL,'""" + ingredients_string + "','" + name_on_order + "', False);"

  st.text(my_insert_stmt)

    #Button
  time_to_insert = st.button('Submit Order')
  if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Well done ' + name_on_order + ' ! Your Smoothie is ordered!', icon="✅")


