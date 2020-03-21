# Event-Time-Scheduler-
## Event Time Scheduler manage time  in which user can attend the meeting.

#### Tech stack Used 
* Python 3.6+
* pandas
* datetime
* Flask ( for makeing APIs)
* Flask Rest Plus (Swagger UI)
* Git ( optional)


#### System Environment 
 * Windows
 * Linux
 

#### Procedure to make it working
Download the code on your desktop or clone the repository form github. Install the required package from file requirements.txt 
``` pip install -r requirements.txt ```
Open the file whichever editor you want ( recommended pycharm ). Now run the File ### flask_api.py  ( use command
``` python flask_api.py ``` or run directly from your text editor.
Now open your browser and visit url ``` http://127.0.0.1:5000/ ``` 

### Sample Screenshot 
<a href="https://ibb.co/9tkkLnW"><img src="https://i.ibb.co/FVLLM6z/Screenshot-29.png" alt="Screenshot-29" border="0"></a>

Click on default url, There is seperate endpoint for blocked timeslot, confirmed timeslot and disallowed_timeslot

### Sample Screenshot
<a href="https://ibb.co/HNWbZ2g"><img src="https://i.ibb.co/Q82T0cm/Screenshot-30.png" alt="Screenshot-30" border="0"></a>

Click on any endpoint and press the button try it out. Pass the input in required form which is required by the Api. 
### Sample Input 
```
{
  "user_a_block_slot": [
     {
        "startTime": "2020-03-18 17:10:00",
        "endTime": "2020-03-18 17:25:00"
    },
    {
        "startTime": "2020-03-18 14:00:00",
        "endTime": "2020-03-18 14:15:00"
    }
  ],
  "user_b_block_slot": [
     {
        "startTime": "2020-03-18 08:00:00",
        "endTime": "2020-03-18 08:15:00"
    },
    {
        "startTime": "2020-03-18 11:00:00",
        "endTime": "2020-03-18 11:15:00"
    }
  ],
  "user_a_confirmed_meetings": [
     {
        "startTime": "2020-03-18 12:4:00",
        "endTime": "2020-03-18 12:12:00"
    },
    {
        "startTime": "2020-03-18 15:33:00",
        "endTime": "2020-03-18 15:50:00"
    }
  ],
  "user_b_confirmed_meetings": [
     {
        "startTime": "2020-03-18 15:45:00",
        "endTime": "2020-03-18 16:00:00"
    },
    {
        "startTime": "2020-03-18 18:30:00",
        "endTime": "2020-03-18 18:45:00"
    }
  ],
  "disallowed_slots": [
      {
        "startTime": "2020-03-18 14:18:00",
        "endTime": "2020-03-18 15:06:00"
    },
    {
        "startTime": "2020-03-18 20:30:00",
        "endTime": "2020-03-18 21:30:00"
    }
  ]
}
```

### sample Screenshot 
<a href="https://ibb.co/h72CgJn"><img src="https://i.ibb.co/Lk9v0Xq/Screenshot-23.png" alt="Screenshot-23" border="0"></a>

Click on execute You will get the required output. Do the same process for all the remaining endpoint.

### sample Screenshot ( Here timeslot is divided into time interval of 15 min )
<a href="https://ibb.co/YDMMXK1"><img src="https://i.ibb.co/xm00YcB/Screenshot-24.png" alt="Screenshot-24" border="0"></a>

