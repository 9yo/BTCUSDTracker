# BTCUSDTracker
Как запустить?
```
cd BTCUSDTracker/
python -m venv venv/
source venv/bin/activate
pip install -r req.txt
python server.py
python client.py

```
В отправке серверу timestamp взят с хоста, а не с апи провайдера, как было предложено в задании, надеюсь это не проблема.