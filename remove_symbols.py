import pandas as pd
df=pd.read_csv(r"""D:\code\datahack\open_trivia_questions_all_difficulties.csv""")
pattern1='&quot;'
pattern2='&#039;'
pattern3='&aacute;'
count_pattern1 = df['Question'].str.contains(pattern1, regex=True).sum()
count_pattern2 = df['Question'].str.contains(pattern2, regex=True).sum()
count_pattern3 = df['Question'].str.contains(pattern3, regex=True).sum()
print(f"Count of '{pattern1}' in Question column: {count_pattern1}")
print(f"Count of '{pattern3}' in Question column: {count_pattern3}")
print(f"Count of '{pattern2}' in Question column: {count_pattern2}")
count_pattern1 = df['Probable Answers'].str.contains(pattern1, regex=True).sum()
count_pattern2 = df['Probable Answers'].str.contains(pattern2, regex=True).sum()
count_pattern3 = df['Probable Answers'].str.contains(pattern3, regex=True).sum()
print(f"Count of '{pattern1}' in Probable Answers column: {count_pattern1}")
print(f"Count of '{pattern3}' in Probable Answers column: {count_pattern3}")
print(f"Count of '{pattern2}' in Probable Answers column: {count_pattern2}")