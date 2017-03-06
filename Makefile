launch: shutdown
	python  flask_public_server/flask_public_server/flask_public_server.py &
	python  hints_provider/hints_provider/hints_provider.py &
	python  stats_analyser/stats_analyser/stats_analyser.py &
	python  stats_updater/stats_updater/stats_updater.py &

shutdown:
	ps -ef | grep "flask_public_server/flask_public_server/flask_public_server.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "hints_provider/hints_provider/hints_provider.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_analyser/stats_analyser/stats_analyser.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_updater/stats_updater/stats_updater.py" | grep -v grep | awk '{print $$2}' | xargs kill