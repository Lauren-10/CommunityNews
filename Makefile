#Add a way to instantiate DB_connector???
feeds_file_pathway = scn_src/feeds_click.py
urls_file_pathway = scn_src/urls_click.py
chatgpt_file_pathway = scn_src/chatgpt_click.py
metrics_file_pathway = scn_src/diagnostics_click.py

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
