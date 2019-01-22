# life_simulation

Now working at generating map. Below u can check example of result runned generator map(will update after any commits which will affect map generator)

![](https://github.com/Fisab/life_simulation/blob/master/imgs/map_example.jpg?raw=true)

# Specifications
 - Server will process game and run in 3 threads
    1. First thread will process game loop
    2. Second thread will process flask API for local client
        - via API local client will get data, and control world
    3. Third thread will process flask SocketIO for local client
        - via SocketIO local client will recieve update on map

 - Client just for spectating for this pretty simulation of world


I only started work on this project and will update README when developing