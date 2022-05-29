import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


PAGE_CONFIG = {"page_title": "Data Visualization",
               "page_icon": "chart_with_upwards_trend:", "layout": "centered"}
st.set_page_config(**PAGE_CONFIG)


def showGraphList():
    graph = ["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"]
    opt = st.radio("Select the graph", graph)
    return opt


def sidebar():
    global df, filename, option, opt, columnList
    df = None
    allowedExtension = ['csv', 'xlsx']
    with st.sidebar:
        uploaded_file = st.sidebar.file_uploader(
            label="Upload DataSet file", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            filename = uploaded_file.name
            extension = filename[filename.index(".")+1:]
            filename = filename[:filename.index(".")]

            if extension in allowedExtension:
                df = pd.read_csv(uploaded_file)
                columnList = df.columns.values.tolist()
                option = st.selectbox("Select Column", columnList)
                st.subheader("Filters")
                opt = showGraphList()
            else:
                st.write("File Format is not supported")


def getIndexes(columnName, value):

    count = -1
    for i in df[columnName]:
        count += 1

        if i == value:
            return count


def mainContent():
    st.header("Lets Visualize Your Data")
    if df is not None:
        st.write(df)
        label = "Choose the Column"
        st.header(label)
        columnList = df.columns.values.tolist()

        selectOption = []
        j = df[columnList[0]].unique()
        for i in j:
            selectOption.append(i)
        selectedData = st.multiselect(
            f"Choose {columnList[0]} to see", selectOption)

        dataToVisualize = []
        for i in selectedData:
            index = getIndexes(columnList[0], i)
            value = df[option][index]
            if type(value) is not str:
                dataToVisualize.append(df[option][index])
            else:
                st.warning(f"The data type of {value} is not supported")
        st.write(pd.DataFrame(dataToVisualize,selectedData))
        if opt == "Line Chart":
            label = "Line Chart for {} is".format(filename)
            st.header(label)
            st.line_chart(pd.DataFrame(dataToVisualize, selectedData))

        elif opt == "Bar Chart":
            label = "Bar Chart for {} is".format(filename)
            st.header(label)
            st.bar_chart(pd.DataFrame(dataToVisualize, selectedData))

        elif opt == "Area Chart":
            label = "Area Chart for {} is".format(filename)
            st.header(label)
            st.area_chart(pd.DataFrame(dataToVisualize, selectedData))

        elif opt == "Pie Chart":
            label = "Pie Chart for {} is".format(filename)
            st.header(label)
            x = np.array(dataToVisualize, 'f')

            fig = plt.figure(figsize=(10, 10))
            if len(dataToVisualize) != 0:
                plt.pie(x, labels=selectedData, autopct='%.5f%%')
                plt.legend(title=option)
                st.pyplot(fig)
            else:
                st.write("There is nothing to show!!")

    else:
        st.write("There is nothing to show!! please add file to see data")


if __name__ == "__main__":
    sidebar()
    mainContent()
