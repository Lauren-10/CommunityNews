from scn_src.functions import scan_with_regex
import pandas as pd
test_url_df = pd.read_csv("urls.csv")
test_regex_df = pd.read_csv("regex.csv")

scan_with_regex(test_url_df,test_regex_df)