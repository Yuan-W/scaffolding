# Scaffolding

[![Build Status](https://travis-ci.com/Yuan-W/scaffolding.svg?token=wCDdC3iNXfe4K35sqGoj&branch=master)](https://travis-ci.com/Yuan-W/scaffolding)

# Services and Ports
| Service | Port | Url
--- | --- | ---
HintsProvider | 5001 | N/A
StatsAnalysis | 5005 | N/A
StatsUpdater | 5002 | N/A
TestManagement | 5003 | N/A
TestRunner | 5004 | N/A


## Current Structure

<center> ![sturcuture](https://www.dropbox.com/s/uagmfuy3o1vjf64/structure.pdf?raw=1) </center>

[Link to the diagram](https://www.lucidchart.com/invitations/accept/56fab060-db54-4f7a-aeba-22e1647b0796)

### Legend

| Edge Id | Method | Fields
--- | --- | ---
1 | GET | Nil
2 | GET | Nil
3 | Response | {time\_spent, average\_time\_spent}
4 | POST | {user\_code, time\_spent}
5 | POST | {user\_code, time\_spent}
6 | POST | {user\_code}
7 | POST | {time\_spent}
8 | Database Update | {time\_spent}
9 | Response | {test\_result}
10 | Response | {hints}
11 | Database Query | {time\_spent}
12 | Response | {time\_spent, average\_time\_spent}
13 | Response | {hints}
