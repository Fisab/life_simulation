# life_simulation
---
### Anchors
 - [What is it?](#what_is_it)
 - [Progress](#progress)
 - [Specifications](#specifications)
 - [Example world](#example)
---

## <a name="what_is_it">What is it?</a>
This is a simulation of the evolution of 2d cells. Until the end is not decided how this will be implemented.


## <a name="progress">Progress</a>
- ~~Generating map~~
- Client-server connection
- Client recieved world and draw real-time
- ...
- Start the implementation of organisms
- ...

## <a name="example">Example world</a>
Below u can check example of result runned generator map(will update after any commits which will affect map generator)
![](https://github.com/Fisab/life_simulation/blob/master/imgs/map_example_1000x1000_000.jpg?raw=true)


## <a name="specifications">Specifications</a>
 - Server will process game and run in 3 threads
    1. First thread will process game loop
    2. Second thread will process flask API for local client
        - via API local client will get data, and control world
    3. Third thread will process flask SocketIO for local client
        - via SocketIO local client will recieve update on map
 - Client just for spectating for this pretty simulation of world


*I only started work on this project and will update README when developing*
