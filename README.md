# Casino Slot Engine
[![Coverage Status](https://coveralls.io/repos/github/meznick/casic-slot-engine/badge.svg?branch=main)](https://coveralls.io/github/meznick/casic-slot-engine?branch=main)

Just a simple engine + simple API microservice for it.

Distributed under [GPLv3](LICENSE.md).

### What's implemented
- [x] Reading config. While in service, config location is set in config.py
- [x] Basic config verification
- [x] Slot rolling new matrix and win lines according to config
- [x] Synchronous service accessible via HTTP

### And what's not
- Bonus games
- Async in service
- Multithread rolling
- RPC service

### Contributing
Suggest new features using issues on this repo. For now first priority on
features above chapter.

### Special thanks
- to Oleg Olegych for creating engine
