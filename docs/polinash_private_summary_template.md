# Private Technical Background Summary Template

Use this in the application or CV, not necessarily inside the public repo if you want to keep the repo fully generic.

## Short version

I built Polinash, a private real-time ML systems project for high-volume streaming market data. The system reconstructs live L2 orderbooks, manages non-stationary time-series features, and supports low-latency predictive modeling. This gave me practical experience with distribution shift, noisy data, evaluation leakage, latency constraints, and robustness problems in sequential decision systems.

## Longer version

My main private engineering project is Polinash, a high-frequency crypto intelligence platform. It processes live websocket streams, reconstructs L2 orderbooks, and produces low-latency analytics and predictive signals. The modeling stack includes a 77M-parameter Temporal Fusion Transformer-style ensemble with specialized experts for different time horizons.

I do not expose proprietary code, private datasets, production features, model weights, or trading logic. The public benchmark in this repository abstracts the general safety/evaluation problems I encountered: distribution shift, overconfident errors, abstention, constraint violations, latency-sensitive decisions, and robustness evaluation under non-stationary conditions.
