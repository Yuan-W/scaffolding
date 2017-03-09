launch_public:
	python  flask_public_server/flask_public_server/flask_public_server.py &

launch_private:
	python  hints_provider/hints_provider/hints_provider.py &
	python  stats_analyser/stats_analyser/stats_analyser.py &
	python  stats_updater/stats_updater/stats_updater.py &
	python  test_management/test_management/test_management.py &
	npm start --prefix test_runner/ &

shutdown_public:
	ps -ef | grep "flask_public_server/flask_public_server/flask_public_server.py" | grep -v grep | awk '{print $$2}' | xargs kill -9

shutdown_private:
	ps -ef | grep "hints_provider/hints_provider/hints_provider.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_analyser/stats_analyser/stats_analyser.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_updater/stats_updater/stats_updater.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "test_management/test_management/test_management.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "app.js" | grep -v grep | awk '{print $$2}' | xargs kill

launch: launch_public launch_private;

shutdown: shutdown_public shutdown_private;