import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_option_menu import option_menu
from babel.numbers import format_currency
sns.set(style='dark')

#setting daily_orders
def daily_orders(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg(
        count_order = ('order_id','nunique'), 
        sum_order_value = ('total_order_value','sum')
        ).reset_index()
    
    return daily_orders_df

#setting order_product_category
def order_product_category(df):
    order_by_product_category_df = df.groupby(by="product_category").agg(
        num_of_order = ('order_id','count'), 
        sum_order_value = ('total_order_value', 'sum')
        ).reset_index()
    
    return order_by_product_category_df

#setting count_customers
def count_customers(df):
    customers_in_cities = df.groupby(by="customer_city").agg(
        count_customer = ('customer_unique_id','nunique')
        ).reset_index()
    
    customers_in_states = df.groupby(by="customer_state").agg(
        count_customer = ('customer_unique_id','nunique')
        ).reset_index()
    
    return customers_in_cities, customers_in_states

#setting customers_order
def customers_order(df):
    cust_count_sum_order = df.groupby(by="customer_unique_id").agg(
        count_order = ('order_id','nunique'), 
        sum_order_value = ('total_order_value', 'sum')
        ).reset_index()
    
    return cust_count_sum_order

#setting count_sellers
def count_sellers(df):
    sellers_in_cities = df.groupby(by="seller_city").agg(
        count_seller = ('seller_id','nunique')
        ).reset_index()
    
    sellers_in_states = df.groupby(by="seller_state").agg(
        count_seller = ('seller_id','nunique')
        ).reset_index()
    
    return sellers_in_cities, sellers_in_states

#setting customers_order
def sellers_order(df):
    seller_count_sum_order = df.groupby(by="seller_id").agg(
        count_order = ('order_id','nunique'), 
        sum_order_value = ('total_order_value', 'sum')
        ).reset_index()
    
    return seller_count_sum_order

#setting color pallete
colors=["#3187d4",'#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4','#b3bcc4']

#load dataframe
main_df = pd.read_csv('https://raw.githubusercontent.com/danendrafau/ecommerce-dataset/refs/heads/main/dashboard/dashboard_main_data.csv')

#loop change kolom (untuk data type)
dt_columns = ['order_date', 'approved_date', 'shipped_date', 'delivery_date']
main_df.sort_values(by="order_date", inplace=True)
main_df.reset_index(inplace=True)

for column in dt_columns:
    main_df[column] = pd.to_datetime(main_df[column])

#setting min_date and max_date
min_date = main_df["order_date"].min()
max_date = main_df["order_date"].max()

#tambah sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/danendrafau/ecommerce-dataset/refs/heads/main/dashboard/logo-dan.png")
    
    #buat start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date,
        max_value=max_date,
        value= [min_date, max_date]
        )

#tambah satu hari ke end_date dan subs
start_date = start_date - pd.DateOffset(days=1)
end_date = end_date + pd.DateOffset(days=1)

#filter main_df by start_date dan end_date
main_df = main_df[(main_df["order_date"] >= start_date) & 
                (main_df["order_date"] <= end_date)]

#judul dashboard
st.markdown('<h1 style="text-align: center;">E-Commerce Public Dashboard</h1>', unsafe_allow_html=True)

### ORDERS ###
def orders_analysis():
    daily_orders_df = daily_orders(main_df)
    order_by_product_category_df = order_product_category(main_df)

    #Count Orders dan Total Order Value per hari
    st.subheader("Pesanan Harian")

    col1, col2 = st.columns(2)
    with col1:
        total_orders = daily_orders_df.count_order.sum()
        st.metric("Jumlah Pesanan", value=total_orders)
 
    with col2:
        total_order_value = format_currency(daily_orders_df.sum_order_value.sum(), "R$", locale='pt_BR') 
        st.metric("Jumlah Nilai Pesanan", value=total_order_value)
    
    #setting nilai max
    xmax = daily_orders_df.order_date[np.argmax(daily_orders_df.count_order)]
    ymax = daily_orders_df.count_order.max()

    fig, ax = plt.subplots(figsize=(25, 10))
    ax.plot(daily_orders_df["order_date"],
            daily_orders_df["count_order"],
            marker='o', 
            linewidth=3,
            color= "#3187d4"
            )
    ax.set_title("Number of Order per Day", loc="center", fontsize=30, pad=20)
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=20)
    ax.annotate(f"At {xmax.strftime('%Y-%m-%d')}\n have {ymax} orders", 
                xy=(xmax, ymax), xycoords='data',
                xytext=(xmax + (end_date - start_date)/6, ymax), 
                textcoords='data', size=20, va="center", ha="center",
                bbox=dict(boxstyle="round4", fc="w"),
                arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", fc="w")
                )
    st.pyplot(fig)

    #setting max 
    x_max = daily_orders_df.order_date[np.argmax(daily_orders_df.sum_order_value)]
    y_max = round(daily_orders_df.sum_order_value.max(), 2)
    
    fig, ax = plt.subplots(figsize=(25, 10))
    ax.plot(daily_orders_df["order_date"],
            daily_orders_df["sum_order_value"],
            marker='o', 
            linewidth=3,
            color= "#3187d4"
            )
    ax.set_title("Jumlah Nilai Pesanan per Hari", loc="center", fontsize=30, pad=20)
    ax.set_ylabel("R$", fontsize=20, labelpad=10)
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=20)
    ax.annotate(f"At {x_max.strftime('%Y-%m-%d')}\n have value\n R$ {y_max}", 
            xy=(x_max, y_max), xycoords='data',
            xytext=(x_max + (end_date - start_date)/6, y_max), 
            textcoords='data', size=20, va="center", ha="center",
            bbox=dict(boxstyle="round4", fc="w"),
            arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.2", fc="w")
            )
    st.pyplot(fig)

    #ranking produknya
    st.subheader("Kategori Produk Terbaik dan Terburuk")
 
    tab1, tab2 = st.tabs(['Frekuensi Pesanan', 'Jumlah Nilai Pesanan'])
    
    with tab1:
        col1, col2 = st.columns(2)
 
        with col2:
            min_order = order_by_product_category_df.num_of_order.min()
            st.metric("Kategori Produk dengan Frekuensi Pesanan Terendah", value=min_order)
 
        with col1:
            max_order = order_by_product_category_df.num_of_order.max()
            st.metric("Kategori Produk dengan Frekuensi Pesanan Tertinggi", value=max_order)

        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25,10))

        sns.barplot(
            x="num_of_order",
            y="product_category",
            data= order_by_product_category_df.sort_values('num_of_order', ascending=False).head(10),
            palette= colors,
            ax=ax[0]
            )
        ax[0].set_ylabel(None)
        ax[0].set_xlabel('Frekuensi', fontsize=15, labelpad=10)
        ax[0].set_title("Frekuensi Tertinggi", loc="center", fontsize=20, pad=10)
        ax[0].tick_params(axis ='y', labelsize=18)
        ax[0].tick_params(axis ='x', labelsize=18)

        sns.barplot(
            x="num_of_order",
            y="product_category",
            data= order_by_product_category_df.sort_values(by=['num_of_order','sum_order_value'], ascending=True).head(10),
            palette=colors,
            ax=ax[1]
            )
        ax[1].set_ylabel(None)
        ax[1].set_xlabel('Frekuensi', fontsize=15, labelpad=10)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Frekuensi Terendah", loc="center", fontsize=20, pad=10)
        ax[1].tick_params(axis='y', labelsize=18)
        ax[1].tick_params(axis='x', labelsize=18)
        plt.suptitle("Kategori Produk Terbaik dan Terburuk berdasarkan Frekuensi", fontsize=25)

        st.pyplot(fig)

    with tab2:
        col1, col2 = st.columns(2)
 
        with col1:
            max_order_value = format_currency(order_by_product_category_df.sum_order_value.max(), "R$", locale='pt_BR')
            st.metric("Kategori Produk dengan Nilai Pesanan Tertinggi", value=max_order_value)

        with col2:
            min_order_value = format_currency(order_by_product_category_df.sum_order_value.min(), "R$", locale='pt_BR')
            st.metric("Kategori Produk dengan Nilai Pesanan Tertinggi", value=min_order_value)
 
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25,10))

        sns.barplot(
            x="sum_order_value",
            y="product_category",
            data= order_by_product_category_df.sort_values('sum_order_value', ascending=False).head(10),
            palette= colors,
            ax=ax[0]
            )
        ax[0].set_ylabel(None)
        ax[0].set_xlabel('Jumlah Nilai Pesanan (Million R$)', fontsize=15, labelpad=10)
        ax[0].set_title("Total Nilai Pesanan Tertinggi", loc="center", fontsize=20, pad=10)
        ax[0].tick_params(axis ='y', labelsize=18)
        ax[0].tick_params(axis ='x', labelsize=18)

        sns.barplot(
            x="sum_order_value",
            y="product_category",
            data= order_by_product_category_df.sort_values('sum_order_value', ascending=True).head(10),
            palette= colors,
            ax=ax[1]
            )
        ax[1].set_ylabel(None)
        ax[1].set_xlabel('Jumlah Nilai Pesanan (R$)', fontsize=15, labelpad=10)
        ax[1].invert_xaxis()
        ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_title("Jumlah Nilai Pesanan Terendah", loc="center", fontsize=20, pad=10)
        ax[1].tick_params(axis='y', labelsize=18)
        ax[1].tick_params(axis='x', labelsize=18)
        plt.suptitle("Kategori Produk Terbaik dan Terburuk berdasarkan Jumlah Nilai Pesanan", fontsize=25)

        st.pyplot(fig)

### CUSTOMERS ###
def customers_analysis():
    customers_in_cities, customers_in_states = count_customers(main_df)
    cust_count_sum_order = customers_order(main_df)
    
    #sebaran Customers dengan kota dan negara bagian
    st.subheader("Sebaran Pelanggan berdasarkan Kota dan Negara Bagian")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_count_cust = main_df.customer_unique_id.nunique()
        st.metric("Jumlah Pelanggan", value=total_count_cust)

    with col2:
        highest_count_cust_city = customers_in_cities.count_customer.max()
        st.metric("Terbanyak berdasarkan Kota", value=highest_count_cust_city)

    with col3:
        highest_count_cust_state = customers_in_states.count_customer.max()
        st.metric("Terbanyak berdasarkan Negara Bagian", value=highest_count_cust_state)
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25, 10))

    sns.barplot(x="customer_city", 
                y="count_customer", 
                data= customers_in_cities.sort_values('count_customer', ascending=False).head(10), 
                palette= colors, 
                ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].tick_params(axis='x', labelrotation=45)
    ax[0].set_title("Berdasarkan Kota", loc="center", fontsize=18, pad=10)
    ax[0].tick_params(axis ='y', labelsize=15)
    ax[0].tick_params(axis ='x', labelsize=15)

    sns.barplot(x="customer_state", 
                y="count_customer", 
                data= customers_in_states.sort_values('count_customer', ascending=False).head(10),
                palette= colors, 
                ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].tick_params(axis='x', labelrotation=45)
    ax[1].set_title("Berdasarkan Negara Bagian", loc="center", fontsize=18, pad=10)
    ax[1].tick_params(axis='y', labelsize=15)
    ax[1].tick_params(axis ='x', labelsize=15)

    plt.suptitle("Sebaran Jumlah Pelanggan berdasarkan Kota dan Negara Bagian", fontsize=20)
    st.pyplot(fig)

    #pelanggan dengan orderan paling gede
    st.subheader("Pelanggan dengan Frekuensi dan Nilai Pesanan Tertinggi")
    tab1, tab2 = st.tabs(['Frekuensi','Jumlah Nilai'])
 
    with tab1:
        col1, col2, col3 = st.columns(3)
 
        with col1:
            max_cust_count_order = cust_count_sum_order.count_order.max()
            st.metric("Frekuensi Tertinggi", value=max_cust_count_order)

        with col2:
            min_cust_count_order = cust_count_sum_order.count_order.min()
            st.metric("Frekuensi Terendah", value=min_cust_count_order)

        with col3:
            avg_cust_count_order = cust_count_sum_order.count_order.mean().astype(int)
            st.metric("Frekuensi Rata-rata", value=avg_cust_count_order)
        
        fig, ax = plt.subplots(figsize=(25, 10))
        sns.barplot(x="count_order", 
                y="customer_unique_id", 
                data= cust_count_sum_order.sort_values('count_order',ascending=False).head(10), 
                palette= colors,
                ax=ax)
        ax.set_ylabel('Customer Unique ID', fontsize=18, labelpad=10)
        ax.set_xlabel('Frekuensi', fontsize=18, labelpad=10)
        ax.set_title("Pelanggan dengan Frekuensi Terbesar", loc="center", fontsize=20, pad=10)
        ax.bar_label(ax.containers[0], label_type='center')
        ax.tick_params(axis ='y', labelsize=15)
        ax.tick_params(axis ='x', labelsize=15)
        st.pyplot(fig)
 
    with tab2:
        col1, col2, col3 = st.columns(3)
 
        with col1:
            max_cust_order_value = format_currency(cust_count_sum_order.sum_order_value.max(), "R$", locale='pt_BR')
            st.metric("Jumlah Nilai Tertinggi", value=max_cust_order_value)

        with col2:
            min_cust_order_value = format_currency(cust_count_sum_order.sum_order_value.min(), "R$", locale='pt_BR')
            st.metric("Jumlah Nilai Tertinggi", value=min_cust_order_value)
        
        with col3:
            avg_cust_order_value = format_currency(cust_count_sum_order.sum_order_value.mean(), "R$", locale='pt_BR')
            st.metric("Jumlah Nilai Rata-rata", value=avg_cust_order_value)
        
        fig, ax = plt.subplots(figsize=(25, 10))

        sns.barplot(x="sum_order_value", 
                    y="customer_unique_id", 
                    data= cust_count_sum_order.sort_values('sum_order_value',ascending=False).head(10), 
                    palette= colors,
                    ax=ax)
        ax.set_ylabel('Customer Unique ID', fontsize=18, labelpad=10)
        ax.set_xlabel('Jumlah Nilai Pesanan (R$)', fontsize=18, labelpad=10)
        ax.set_title("Pelanggan dengan Nilai Pesanan Tertinggi", loc="center", fontsize=20, pad=10)
        ax.bar_label(ax.containers[0], label_type='center')
        ax.tick_params(axis ='y', labelsize=15)
        ax.tick_params(axis ='x', labelsize=15)
        st.pyplot(fig)
            
### BAKULAN ###
def sellers_analysis():
    sellers_in_cities, sellers_in_states = count_sellers(main_df)
    seller_count_sum_order = sellers_order(main_df)

    #sebaran penjual berdasarkan kota dan negara bagian
    st.subheader("Persebaran Penjual berdasarkan kota dan negara bagian")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_count_seller = main_df.seller_id.nunique()
        st.metric("Jumlah Penjual", value=total_count_seller)

    with col2:
        highest_count_seller_city = sellers_in_cities.count_seller.max()
        st.metric("Terbanyak berdasarkan Kota", value=highest_count_seller_city)

    with col3:
        highest_count_seller_state = sellers_in_states.count_seller.max()
        st.metric("Terbanyak berdasarkan Negara Bagian", value=highest_count_seller_state)
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))

    sns.barplot(x="seller_city", 
                y="count_seller", 
                data= sellers_in_cities.sort_values('count_seller', ascending=False).head(10), 
                palette= colors, 
                ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].tick_params(axis='x', labelrotation=45)
    ax[0].set_title("Berdasarkan Kota", loc="center", fontsize=18, pad=10)
    ax[0].tick_params(axis ='y', labelsize=15)
    ax[0].tick_params(axis='x', labelsize=15)

    sns.barplot(x="seller_state", 
                y="count_seller", 
                data= sellers_in_states.sort_values('count_seller', ascending=False).head(10),
                palette= colors, 
                ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].tick_params(axis='x', labelrotation=50)
    ax[1].set_title("Berdasarkan Negara Bagian", loc="center", fontsize=18, pad=10)
    ax[1].tick_params(axis='y', labelsize=15)
    ax[1].tick_params(axis='x', labelsize=15)

    plt.suptitle("Persebaran Jumlah Penjual Berdasarkan Kota dan Negara Bagian", fontsize=20)
    st.pyplot(fig)

    #penjual frekuensi terbesar
    st.subheader("Penjual dengan Frekuensi dan Jumlah Nilai Pesanan Terbesar")
    tab1, tab2 = st.tabs(['Frekuensi','Jumlah Nilai Pesanan'])
 
    with tab1:
        col1, col2, col3 = st.columns(3)
 
        with col1:
            max_seller_count_order = seller_count_sum_order.count_order.max()
            st.metric("Frekuensi Tertinggi", value=max_seller_count_order)

        with col2:
            min_seller_count_order = seller_count_sum_order.count_order.min()
            st.metric("Frekuensi Terendah", value=min_seller_count_order)

        with col3:
            avg_seller_count_order = seller_count_sum_order.count_order.mean().astype(int)
            st.metric("Rata-rata Frekuensi", value=avg_seller_count_order)
        
        fig, ax = plt.subplots(figsize=(25, 10))
        sns.barplot(x="count_order", 
                    y="seller_id", 
                    data= seller_count_sum_order.sort_values('count_order',ascending=False).head(10), 
                    palette= colors,
                    ax=ax)
        ax.set_ylabel('Seller ID', fontsize=18, labelpad=10)
        ax.set_xlabel('Jumlah Pesanan', fontsize=18, labelpad=10)
        ax.set_title("Penjual dengan Jumlah Pesanan Tertinggi", loc="center", fontsize=20, pad=10)
        ax.bar_label(ax.containers[0], label_type='center')
        ax.tick_params(axis ='y', labelsize=15)
        ax.tick_params(axis ='x', labelsize=15)
        st.pyplot(fig)
 
    with tab2:
        col1, col2, col3 = st.columns(3)
 
        with col1:
            max_seller_order_value = format_currency(seller_count_sum_order.sum_order_value.max(), "R$", locale='pt_BR')
            st.metric("Nilai Pesanan Tertinggi", value=max_seller_order_value)

        with col2:
            min_seller_order_value = format_currency(seller_count_sum_order.sum_order_value.min(), "R$", locale='pt_BR')
            st.metric("Nilai Pesanan Terendah", value=min_seller_order_value)
        
        with col3:
            avg_seller_order_value = format_currency(seller_count_sum_order.sum_order_value.mean(), "R$", locale='pt_BR')
            st.metric("Rata-rata Nilai Pesanan", value=avg_seller_order_value)

        
        fig, ax = plt.subplots(figsize=(25, 10))

        sns.barplot(x="sum_order_value", 
                    y="seller_id", 
                    data= seller_count_sum_order.sort_values('sum_order_value',ascending=False).head(10), 
                    palette= colors,
                    ax=ax)
        ax.set_ylabel('Seller ID', fontsize=18, labelpad=10)
        ax.set_xlabel('Jumlah Nilai Pesanan (R$)', fontsize=18, labelpad=10)
        ax.set_title("Penjual dengan Jumlah Nilai Pesanan Terbesar", loc="center", fontsize=20, pad=10)
        ax.bar_label(ax.containers[0], label_type='center')
        ax.tick_params(axis ='y', labelsize=15)
        ax.tick_params(axis ='x', labelsize=15)
        st.pyplot(fig)

#nambahin radio sidebar
def sidebar_function():
    with st.sidebar:
        selected= option_menu(
            menu_title= "Mau ngecek apa sih?",
            options=["Pesanan","Pelanggan","Penjual"],
            icons=["cart-fill","people-fill","shop-window"],
            menu_icon="clipboard-data-fill",
            default_index=0
            )

    if selected =="Pesanan":
        orders_analysis()
    if selected=="Pelanggan":
        customers_analysis()
    if selected=="Penjual":
        sellers_analysis()
sidebar_function()

st.sidebar.caption('Copyright © Danendra Fahar Utama - 2024')