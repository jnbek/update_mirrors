# update_mirrors.py
My personal open source project mirrors script

My shell based script works fine, however I sync a lot of mirrors for hosting on my personal server. 
Syncing all these projects' code one by one is a very time consuming process,
so I decided to write me a threaded mirror updater. Sadly, my perferred language, 
Perl isn't known for it's threading capabilities, and since I needed an excuse to write
something useful in Python and since Python's threading system is one of the better scripting 
language based system and it's subprocess module is very familiar to Perl's IPC::Run module
and finally, on my base server Python is installed as a dependency; that made the choice obvious.

Now I'm not much of a Python fan, it's a fine language but it's very stuffy and I don't like it's 
whitespace rules at all... It's been a belief of mine that whitespace should never result in a fatal error.
Two languages have done this to me, PHP and Python... But I can't deny the fact that Python has it's place
and for this particular case, was the correct tool for the job. 

Now for the credits. The Threading portion of this code was more or less stolen from and ported to it's
current state from http://www.tutorialspoint.com/python/python_multithreading.htm

I'm not particularly thrilled about having to use the dictionaries for the sites and args, 
there's probably a better way and some day, I may futz with it to make this a bit more 'modular' in that
you can use this for one or one hundred mirror syncs by passing in a plain text file listing the args and urls.

But not right now :)
