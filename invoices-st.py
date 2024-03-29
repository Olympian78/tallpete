import fitz
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Cranberry Extract Invoices")

order_df = pd.DataFrame(columns=["order_no", "document_date", "store_name", "qty"], dtype=str)

# fname = "PO - 4801417909.pdf"
files = st.file_uploader(label="Select files to upload", type="pdf", accept_multiple_files=True)
for i, ff in enumerate(files, start=1):
    doc = fitz.open(stream=ff.getvalue())
    page = doc[0]
    text = page.get_text("blocks", sort=True)
    # # for i, block in enumerate(text):
    # #     print(i, block[-3])
    # #     # for j, row in enumerate(block[-4]):
    # #     #     print(i, j, row)

    order_no = list(filter(lambda x: x != "", text[0][4].split("\n")))[0].split()[-1]
    document_date = list(filter(lambda x: x != "", text[3][4].split("\n")))[-1].split()[-1]
    store_name = list(filter(lambda x: x != "", text[5][4].split("\n")))[-1].split(":")[-1].replace("-", "")
    # text
    qty = list(filter(lambda x: x != "", text[11][4].split("\n")))[4].strip()

    order_df.loc[i] = [order_no, document_date, store_name, qty]

    # st.write(f'{order_no = }')
    # st.write(f'{document_date = }')
    # st.write(f'{store_name = }')
    # st.write(f'{pk_unit = }')

st.write("Order preview:")
st.write(order_df)

st.download_button("Download .txt (CSV) file", order_df.to_csv(index=False))
