add-rss-feeds:
	python -m scn_src.feeds_click \
	--rss_feed_csv $(RSS_FEED_CSV) \
	--table_name $(FEEDS_TABLE)
# example call: make add-rss-feeds RSS_FEED_CSV=scn_src/lauren/rss_test.csv TABLE_NAME=craigtest_feeds2 

scrape-feeds:
	python -m scn_src.articles_click \
	--feeds_table $(FEEDS_TABLE) \
	--final_table $(FINAL_TABLE)

# example call: make scrape-urls FEEDS_TABLE=craigtest_feeds2 FINAL_TABLE=craigtest_articles2

scrape-articles:
	python -m scn_src.chatgpt_click \
	--chunk_size $(CHUNK_SIZE) \
	--llm_model $(LLM_MODEL) \
	--llm_temperature $(LLM_TEMPERATURE) \
	--table_name $(FINAL_TABLE) \
	--multiprocessor_on $(MULTIPROCESSOR_ON)
# example call: make scrape-articles CHUNK_SIZE=50 LLM_MODEL=gpt-4o-mini LLM_TEMPERATURE=0 TABLE_NAME=craigtest_articles2 MULTIPROCESSOR_ON=True

calculate-metrics:
	python -m scn_src.diagnostics_click \
	--bootstrap_iterations $(BOOTSTRAP_ITERATIONS) \
	--llm_model $(LLM_MODEL) \
	--llm_temperature $(LLM_TEMPERATURE) \
	--ground_truth_csv $(GROUND_TRUTH_CSV)
# example call: make calculate-metrics BOOTSTRAP_ITERATIONS=10000 LLM_MODEL=gpt-4o-mini LLM_TEMPERATURE=0 GROUND_TRUTH_CSV=data_files/ground_truth_df.csv


full-pipeline: add-rss-feeds scrape-feeds scrape-articles calculate-metrics
# runs all steps in sequence
# example call: make full-pipeline RSS_FEED_CSV=scn_src/lauren/rss_test.csv FEEDS_TABLE=craigtest_feeds2 FINAL_TABLE=craigtest_articles2
#	 CHUNK_SIZE=50 LLM_MODEL=gpt-4o-mini LLM_TEMPERATURE=0 MULTIPROCESSOR_ON=True BOOTSTRAP_ITERATIONS=10000 GROUND_TRUTH_CSV=data_files/ground_truth_df.csv

