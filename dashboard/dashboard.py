import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtc
import seaborn as sns

st.set_page_config(layout="wide")
st.title("E-Commerce Dashboard")

@st.cache_data
def load_data():
    customers_df = pd.read_csv("../data/customers_dataset.csv")
    geolocation_df = pd.read_csv("../data/geolocation_dataset.csv")
    order_items_df = pd.read_csv("../data/order_items_dataset.csv")
    order_payments_df = pd.read_csv("../data/order_payments_dataset.csv")
    order_reviews_df = pd.read_csv("../data/order_reviews_dataset.csv")
    orders_df = pd.read_csv("../data/orders_dataset.csv")
    product_category_name_translation_df = pd.read_csv("../data/product_category_name_translation.csv")
    products_df = pd.read_csv("../data/products_dataset.csv")
    sellers_df = pd.read_csv("../data/sellers_dataset.csv")
    return customers_df, geolocation_df, order_items_df, order_payments_df, order_reviews_df, orders_df, product_category_name_translation_df, products_df, sellers_df

customers_df, geolocation_df, order_items_df, order_payments_df, order_reviews_df, orders_df, product_category_name_translation_df, products_df, sellers_df = load_data()

selected_tab = st.sidebar.radio("Pilih Analisis:", [
    "Home",
    "Pertanyaan 1", 
    "Pertanyaan 2", 
    "Pertanyaan 3",
    "Kesimpulan Akhir"
])

if selected_tab == "Home":
    st.header("🏠 Proyek Analisis Data: E-Commerce Public Dataset")
    st.markdown("""
        ### **Pertanyaan Bisnis:** \n
        1. Bagaimana performa penjualan dan revenue perusahaan dalam beberapa bulan terakhir?
        2. Bagaimana tingkat kepuasan pelanggan terhadap produk dan layanan dalam beberapa bulan terakhir?
        3. Bagaimana demografi pelanggan perusahaan, seperti lokasi state dan lokasi kota?
    """)

elif selected_tab == "Pertanyaan 1":
    st.header("📈 Bagaimana Performa Penjualan dan Revenue Perusahaan Dalam Beberapa Bulan Terakhir?")
    
    orders_delivered = orders_df[orders_df["order_status"] == "delivered"].copy()
    
    # Konversi tanggal pembelian
    orders_delivered["order_purchase_timestamp"] = pd.to_datetime(orders_delivered["order_purchase_timestamp"])
    orders_delivered["order_month"] = orders_delivered["order_purchase_timestamp"].dt.to_period("M")

    # Jumlah pesanan per bulan
    sales_per_month = orders_delivered.groupby("order_month").size().reset_index(name="total_orders")

    # Revenue per bulan
    revenue_df = orders_delivered.merge(order_payments_df, on="order_id", how="left")
    revenue_per_month = revenue_df.groupby("order_month")["payment_value"].sum().reset_index()

    # Visualisasi: Tren jumlah penjualan per bulan
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=sales_per_month["order_month"].astype(str), y=sales_per_month["total_orders"], marker='o', linestyle='-', ax=ax)
    ax.set_title("Tren Jumlah Penjualan Per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Orders")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(fig)

    # Visualisasi: Tren revenue per bulan
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(x=revenue_per_month["order_month"].astype(str), y=revenue_per_month["payment_value"], marker='o', linestyle='-', color='red', ax=ax)
    ax.set_title("Tren Revenue Per Bulan dalam Brazilian Real (BRL)")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Revenue")
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(fig)

    # Analisis produk terlaris
    product_sales = order_items_df.groupby("product_id")["order_id"].count().reset_index()
    product_sales = product_sales.rename(columns={"order_id": "total_sold"}).sort_values(by="total_sold", ascending=False)

    # Ambil kategori produk
    product_sales = product_sales.merge(products_df[["product_id", "product_category_name"]], on="product_id", how="left")
    product_sales = product_sales.merge(product_category_name_translation_df, on="product_category_name", how="left")

    # Visualisasi: 10 produk terlaris
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(x="total_sold", y="product_category_name_english", data=product_sales.head(10), palette="Blues_r", ax=ax)
    ax.set_xlabel("Jumlah Terjual")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("10 Kategori Produk Terlaris")
    st.pyplot(fig)
    
    st.markdown("""
        ### **Conclusion** \n
        - Bulan November 2017 mencatat jumlah penjualan tertinggi, yaitu 7288 penjualan. Ini menunjukkan adanya lonjakan permintaan, kemungkinan akibat promosi atau event tertentu
        - Sebaliknya, bulan September dan Desember 2016 memiliki penjualan terendah, hanya 1 transaksi, yang bisa mengindikasikan bahwa platform ini baru mulai beroperasi saat itu
        - Pendapatan tertinggi juga terjadi pada bulan November 2017, dengan total pendapatan sebesar 1.153.393,22 BRL, yang sejalan dengan tingginya jumlah transaksi pada bulan tersebut
        - Produk dalam kategori "furniture decor" adalah yang paling banyak terjual, yang bisa menunjukkan bahwa pelanggan e-commerce ini lebih cenderung membeli produk dekorasi rumah dibanding kategori lainnya
    """)

elif selected_tab == "Pertanyaan 2":
    st.header("⭐ Bagaimana Tingkat Kepuasan Pelanggan Terhadap Produk dan Layanan Dalam Beberapa Bulan Terakhir?")
    
    order_reviews_df["review_creation_date"] = pd.to_datetime(order_reviews_df["review_creation_date"])
    order_reviews_df["review_month"] = order_reviews_df["review_creation_date"].dt.to_period("M")

    # Distribusi rating pelanggan
    review_distribution = order_reviews_df["review_score"].value_counts().sort_index()

    # Rata-rata rating per bulan
    avg_rating_per_month = order_reviews_df.groupby("review_month")["review_score"].mean().reset_index()

    # Visualisasi: Distribusi rating pelanggan
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=review_distribution.index, y=review_distribution.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Jumlah Ulasan")
    ax.set_title("Distribusi Rating Pelanggan")
    ax.grid()
    st.pyplot(fig)

    # Visualisasi: Tren rata-rata rating per bulan
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(avg_rating_per_month["review_month"].astype(str), avg_rating_per_month["review_score"], color="blue", alpha=0.7)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Rating")
    ax.set_title("Tren Rata-rata Rating Per Bulan")
    plt.xticks(rotation=45)
    ax.grid(axis="y")
    st.pyplot(fig)
    
    st.markdown("""
        ### **Conclusion** \n
        - Sebanyak 57.328 pengguna memberikan rating 5, yang berarti mayoritas pelanggan merasa puas dengan pengalaman belanja mereka
        - Rata-rata rating selama satu tahun cukup stabil di angka sekitar 4.5, menunjukkan bahwa kualitas layanan dan produk secara umum cukup baik
    """)
    
    st.markdown("""  
        Namun, perlu diperhatikan bahwa ada beberapa pelanggan yang memberikan rating kurang memuaskan, yaitu sekitar 15.000 orang, 
        sehingga sangat perlu diperhatikan untuk meningkatkan kualitas produk atau layanan.
    """)

    # Contoh ulasan dengan rating 1 (ketidakpuasan pelanggan)
    st.markdown("""
        ##### Contoh Ulasan dengan Rating 1
    """)
    negative_reviews = order_reviews_df[order_reviews_df["review_score"] == 1]["review_comment_message"].dropna().sample(7, random_state=50)
    for review in negative_reviews:
        st.write(f"📝 *{review}*")

elif selected_tab == "Pertanyaan 3":
    st.header("🌍 Bagaimana demografi pelanggan perusahaan, seperti lokasi state dan lokasi kota?")
    # Sebaran pelanggan berdasarkan state
    customer_per_state = customers_df["customer_state"].value_counts()

    # Sebaran pelanggan berdasarkan kota (Top 10)
    customer_per_city = customers_df["customer_city"].value_counts().head(10)

    # Performa penjualan berdasarkan state
    revenue_per_state = (
        orders_df.merge(order_payments_df, on="order_id")
        .merge(customers_df, on="customer_id")
        .groupby("customer_state")["payment_value"]
        .sum()
        .sort_values(ascending=False)
    )

    # 📊 Visualisasi: Sebaran pelanggan berdasarkan state
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=customer_per_state.index, y=customer_per_state.values, palette="viridis", ax=ax)
    ax.set_xlabel("State")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title("Sebaran Pelanggan Berdasarkan State")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Visualisasi: Performa penjualan berdasarkan state
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=revenue_per_state.index, y=revenue_per_state.values, ax=ax)
    ax.set_xlabel("State")
    ax.set_ylabel("Total Revenue (BRL)")
    ax.set_title("Performa Penjualan Berdasarkan State Dalam Brazilian Real (BRL)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    ax.yaxis.set_major_formatter(mtc.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    st.pyplot(fig)

    # Visualisasi: Top 10 kota dengan pelanggan terbanyak
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=customer_per_city.index, y=customer_per_city.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kota")
    ax.set_ylabel("Jumlah Pelanggan")
    ax.set_title("Top 10 Kota dengan Pelanggan Terbanyak")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    st.markdown("""
        ### **Conclusion** \n
        - Pendapatan terbanyak berasal dari State of São Paulo, dengan total pendapatan sebesar 5.997.042,04 BRL, menjadikannya wilayah dengan kontribusi terbesar terhadap revenue perusahaan
        - State of São Paulo juga memiliki jumlah pelanggan terbanyak, dengan 41.746 pengguna
        - Kota dengan pelanggan terbanyak adalah São Paulo, dengan 15.540 pengguna, yang menegaskan bahwa pusat aktivitas e-commerce ini berada di kota besar tersebut
    """)
    
elif selected_tab == "Kesimpulan Akhir":
    st.header("💡 Kesimpulan Akhir & Rekomendasi Bisnis")
    st.markdown("""
    - **Optimalisasi Penjualan di Bulan November**
        - Mengingat bulan November memiliki penjualan dan pendapatan tertinggi, perusahaan bisa mengulang strategi promosi atau campaign yang sukses di bulan tersebut untuk meningkatkan penjualan pada bulan lainnya
        
    - **Fokus pada Produk yang Laris**
        - Karena kategori "furniture decor" paling laris, strategi pemasaran bisa difokuskan lebih banyak pada kategori ini untuk meningkatkan pendapatan lebih lanjut

    - **Menjaga Kepuasan Pelanggan**
        - Dengan rating rata-rata stabil di 4.5, perusahaan perlu tetap mempertahankan layanan yang baik, kualitas produk yang tinggi, serta pengiriman yang tepat waktu untuk menjaga kepuasan pelanggan

    - **Memanfaatkan Wilayah dengan Permintaan Tinggi**
        - State dan Kota São Paulo merupakan state dengan jumlah palanggan terbanyak, sehingga perusahaan bisa mempertimbangkan strategi pengiriman lebih cepat, gudang lokal, atau penawaran eksklusif bagi pelanggan di wilayah tersebut untuk meningkatkan loyalitas pelanggan
    """)
