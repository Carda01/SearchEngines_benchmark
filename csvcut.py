import pandas as pd

csvs=['./data_1/Comments.csv','./data_1/Posts.csv', './data_1/Users.csv']
sf=[2,3]

for i in csvs:
    for j in sf:
        df = pd.read_csv(i)
        output_file='./data_'+str(j)+'/'+i.split("/")[2]
        cut=len(df)//j
        final= df.iloc[:cut]
        final.to_csv(output_file, index=False)
        