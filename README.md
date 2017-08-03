# thetalesimplebot

A simple Python bot based on API of The Tale browser game. Api description is at: http://the-tale.org/guide/api

The bot itself consists of three parts, TheBrain class being the endpoint.

To run it as-is only email and password are required:

~~~python
import thebrain
bot = thebrain.TheBrain()

while True:
    bot.take_over_the_world()
~~~

It is pretty easy to edit the `take_over_the_world()` method to change the existing conditions or to add your own.