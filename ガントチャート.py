import streamlit as st
import pandas as pd
import gspread_pandas as gspd
from datetime import datetime, timedelta
import plotly.express as px

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1BsKymbniKnSCFJAkYbflLoAjd4GzjSRC17NU-hhkFlo/edit#gid=0"
JSON_KEYFILE_CONTENT = {
  "type": "service_account",
  "project_id": "lms-dx",
  "private_key_id": "1febf55abbf8698aab97af1a3d7160ab7b6aaf90",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD0bDuh5ibfaI8M\n5JNJoLFJUHmhbofyY3hGzvBdnr7/PWZ9g3QBh6NlElwI+cnbWHuqZFEyqMJjudUs\nffwqhOUxgA5rWwG+eeN24LWZPVehaGGmmWfAGllfdCU6j1HMwoIZmJahAs1SnarV\nPp3tl5uL91rGkk0ckYF2u37TCxukr4PZJ71DtMgYj7ckn5wim5gPQzrwkmJRUsmr\n/pCgupxepxV9NqlaYD1iiqsm79fDELMCjVu3kcTyb0eevNRmhvNJaOfS2f3f+ItR\nPgL3OdzCc+5+iYjeD8ulJZrNl3hs0R2crHZZdE42NcO0pKj5UyjrnqnEpxjBOwSV\nm5ehEm+rAgMBAAECggEAZnp4mB0sgC/RBllRjaWznycAEBiNJCnjVGDQM5hqwQ4n\nygkS2s9ZSPelIdhE81PKabrstl4+Ply8TY626sbUZ2gm44kBFrD5Fy8IxKqM8q4W\nfyjDcK47eYNzVnWfmMeWj4/D29cWagSUCxtZULPncgwwAaB2dztkefkLqAV4vhdM\n2tjhJ4mIGk8ZhqrABEdHzq6NlaSVDP6P5JajFyHgEHly734KukBm29ZwDvA33ty+\nyK58TlKhrCEV6nymBlX7KsV6OPqxJrvUSbD5HEMduvKAGD70CXsZqKc2VzRyhoK5\nQlSqpJAq87vJnaa09aIS3FgB6tZUSSWynXvZYlWh9QKBgQD99glYRTqLGOKFXrUl\nivIUSDk3J3vBeHdw+YemXI6wQSnZ1BxfnTkuT9Lr3bmfpMaUPLzd+g+d04Xp0XAP\n2+sOaqaldNxDDMtT2zZGcIllK+C0o5MSTT19AbtbC8Homf3Rn3iiOtOINsFKsUR+\nARJ28wkIjyvemvehUGkfzjj2BQKBgQD2YpeswI1ebIbHS2hnpe2NzXk+mtC8t6MU\nSHj+56vAHlBH3uNmtz1q/7fdWPa6Q0MHYQ5qMhIFhIDXfwZgDS/zV2BWAwhpAZe5\noRu3zOSv+OuREkojead7Sn4sQ0EyFqYTXcHE21I5XO1lTxSMNuSxVWdKZbA6kaXY\nJ/YtGhSN7wKBgEzD7Ds0Yefd08sAv7zjbR1YX4MeejgXE/OgWbKd07vPVrkzdogo\nXDp1gootcYiiJCx215g5mDLa12XAGyGQFlM7RbhJxLK30VY9swBD0CQ2ySuRLkmf\n83Av79Qrj6ehtKmCjNJs+bf45SCQyOVVqaEvAZIGxPn62dN3HO+yRGGJAoGBAIap\nLjLZ7qob8LH+MersUmC9W7Xu0YVDbNtKHO9c2Y8gQkp1tJ3QKr5PU0OkOv1kg78F\nueYqxZTEbdLZ9zcKHhoGuH1qHO+fUji/qDGVx6uyBbX9ZA3tkK8e8MTqYTiqDkzp\nYl1gbZkyhAFp7lYQLoAJqHGOEHqCXj084hyWc4N7AoGAXwAGPsW5R4v/asBi7tL3\nZofKRx4ikZAZ1IipART1QOkv+mFjdwkVQOMqo2dtrc/lmj9n9W/VKomUMtzLMhuU\nes3iHdSF2vcV/lohPpNm0mcl5wBKEYfQurul0FTD+MWLe0bShk7qauVw3Qd21qSE\nlO2gBynmZawljbUKRgUVyPQ=\n-----END PRIVATE KEY-----\n",
   "client_email": "jld-lmstest@lms-dx.iam.gserviceaccount.com",
   "client_id": "116188404457669453091",
   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
   "token_uri": "https://oauth2.googleapis.com/token",
   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/jld-lmstest%40lms-dx.iam.gserviceaccount.com",
   "universe_domain": "googleapis.com"
}

def get_data_from_gsheet():
    spread = gspd.Spread(SPREADSHEET_URL, config=JSON_KEYFILE_CONTENT)
    df = spread.sheet_to_df(sheet='sheet2')
    df = df.rename(columns={'readerNo.': 'readerNo', 'CardID': 'CardID', 'Process': 'Process', 'start': 'start', 'end': 'end', 'diff(second)': 'diff'})
    return df

def process_data(df):
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    df['Process_padded'] = '\n' + df['Process'] + '\n'
    df['diff'] = pd.to_timedelta(df['diff']).dt.total_seconds().astype(int)
    return df

def plot_gantt_chart(data, selected_date):
    fig = px.timeline(data, x_start='start', x_end='end', y='Process_padded', color='Process')
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(xaxis_range=[datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=9),
                                datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=18)])
    fig.update_traces(marker=dict(line=dict(width=0))) 
    st.plotly_chart(fig)

def get_date_range(df):
    min_date = df['start'].dt.date.min()
    max_date = df['end'].dt.date.max()
    return min_date, max_date

def get_selected_card_ids(df, selected_date):
    selected_card_ids = df.loc[df['start'].dt.date == selected_date, 'CardID'].unique()
    return selected_card_ids

def get_selected_data(df, selected_date, selected_card_id):
    selected_data = df[(df['start'].dt.date == selected_date) & (df['CardID'] == selected_card_id)]
    return selected_data

def calc_process_times(selected_data):
    process_times = selected_data.groupby('Process')['diff'].sum().reset_index()
    process_times['diff'] = process_times['diff'].apply(lambda x: str(timedelta(seconds=x)))
    return process_times

def calc_process_workid_times(selected_data):
    process_workid_times = selected_data.groupby(['Process', 'WorkID'])['diff'].sum().reset_index()
    process_workid_times['diff'] = process_workid_times['diff'].apply(lambda x: str(timedelta(seconds=x)))
    return process_workid_times

def display_tables(process_times, process_workid_times):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Total time per Process:")
        st.dataframe(process_times)
    with col2:
        st.write("Total time per WorkID, grouped by Process:")
        st.dataframe(process_workid_times)

def main():
    st.title("Time on Task")
    df = get_data_from_gsheet()
    df = process_data(df)
    min_date, max_date = get_date_range(df)
    selected_date = st.date_input("Select Date", min_value=min_date, max_value=max_date, value=min_date)
    selected_card_ids = get_selected_card_ids(df, selected_date)
    selected_card_id = st.selectbox("Select Card ID", options=selected_card_ids)
    selected_data = get_selected_data(df, selected_date, selected_card_id)

    if selected_data.empty:
        st.write("No data available for the selected date and Card ID.")
    else:
        plot_gantt_chart(selected_data, selected_date)
        process_times = calc_process_times(selected_data)
        process_workid_times = calc_process_workid_times(selected_data)
        display_tables(process_times, process_workid_times)

if __name__ == "__main__":
    main()

