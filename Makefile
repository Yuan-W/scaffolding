launch_public:
	python  flask_public_server/flask_public_server/flask_public_server.py &

launch_private:
	python  hints_provider/hints_provider/hints_provider.py &
	python  stats_analyser/stats_analyser/stats_analyser.py &
	python  stats_updater/stats_updater/stats_updater.py &
	python  exercise_manager/exercise_manager/exercise_manager.py &
	npm start --prefix test_runner/ &

gunicorn_private:
	gunicorn hints_provider:app --access-logfile hints_provider-access.log  --error-logfile hints_provider-error.log -b :5001 --chdir hints_provider/hints_provider/ &
	gunicorn stats_updater:app --access-logfile stats_updater-access.log  --error-logfile stats_updater-error.log -b :5002 --chdir stats_updater/stats_updater/ &
	gunicorn exercise_manager:app --access-logfile exercise_manager-access.log  --error-logfile exercise_manager-error.log -b :5003 --chdir exercise_manager/exercise_manager/ &
	gunicorn stats_analyser:app --access-logfile stats_analyser-access.log  --error-logfile stats_analyser-error.log -b :5005 --chdir stats_analyser/stats_analyser/ &
	npm start --prefix test_runner/ &

shutdown_gunicorn:
	ps -ef | grep "hints_provider:app" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_analyser:app" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_updater:app" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "exercise_manager:app" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "app.js" | grep -v grep | awk '{print $$2}' | xargs kill

gunicorn_public:
	gunicorn flask_public_server:app --access-logfile gunicorn-access.log  --error-logfile gunicorn-error.log -b :5000 --chdir flask_public_server/flask_public_server/ &

shutdown_gunicorn_public:
	ps -ef | grep "flask_public_server:app" | grep -v grep | awk '{print $$2}' | xargs kill

shutdown_public:
	ps -ef | grep "flask_public_server/flask_public_server/flask_public_server.py" | grep -v grep | awk '{print $$2}' | xargs kill -9

shutdown_private:
	ps -ef | grep "hints_provider/hints_provider/hints_provider.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_analyser/stats_analyser/stats_analyser.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "stats_updater/stats_updater/stats_updater.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "exercise_manager/exercise_manager/exercise_manager.py" | grep -v grep | awk '{print $$2}' | xargs kill
	ps -ef | grep "app.js" | grep -v grep | awk '{print $$2}' | xargs kill

launch: launch_public launch_private;

shutdown: shutdown_public shutdown_private;


