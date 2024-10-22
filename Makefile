#ASK WILL
#what should the default tags to extract be? different in call and langchainutils

feeds_file_pathway = \\wsl.localhost\Ubuntu\home\cret2\anaconda3\envs\communitynews\CommunityNews\scn_src\feeds_click
urls_file_pathway = scn_src/urls_click
chatgpt_file_pathway = scn_src/chatgpt_click
metrics_file_pathway = scn_src/diagnostics_click
dbconnector_file_pathway = scn_src/dbconnector_click

create-dbconnector:
	python -m $(dbconnector_file_pathway)

add-rss-feeds:
	python -m $(feeds_file_pathway)

scrape-feeds:
	python -m $(urls_file_pathway)

scrape-urls:
	python -m $(chatgpt_file_pathway)
	
calculate-metrics:
	python -m $(metrics_file_pathway)

full-pipeline:
	python -m $(feeds_file_pathway)
	python -m $(urls_file_pathway)
	python -m $(chatgpt_file_pathway)
	python -m $(metrics_file_pathway)
