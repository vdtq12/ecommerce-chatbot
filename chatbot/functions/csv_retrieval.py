import pandas as pd

def csv_retrieval(keyword):
    print(keyword)
    path = "./static/app_sys_reqs.csv"
    df = pd.read_csv(path)

    url_data = df[df['name'].str.contains(keyword, case=False)]['url'].values[0]

    if url_data:
        return url_data
    else:
        return None