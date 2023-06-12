import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io



uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )
    elif column_type == "Categorical":
        categorical_column = st.sidebar.selectbox(
            'Select a Column', df.select_dtypes(include=['object']).columns
        )

        choose_color = st.color_picker('Pick a Color', "#69b3a2")
        choose_opacity = st.slider('Color Opacity', min_value=0.0, max_value=1.0, step=0.05, value=0.2)

        # Rest of the code for the "Categorical" case
        category_proportions = df[categorical_column].value_counts(normalize=True)

        # Display proportions in a table
        st.write("Proportions of Each Category Level:")
        st.write(category_proportions)

        fig, ax = plt.subplots()
        ax.bar(category_proportions.index, category_proportions.values, color=choose_color, alpha=choose_opacity)
        ax.set_title('Customized Bar Plot')
        ax.set_xlabel(categorical_column)
        ax.set_ylabel('Proportion')

        st.pyplot(fig)
        filename = "bar_plot.png"
        fig.savefig(filename, dpi=300)

        # Display the download button
        with open("bar_plot.png", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name="bar_plot.png",
                mime="image/png"
            )