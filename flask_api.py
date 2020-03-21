from flask import Flask
from flask_restplus import Resource, Api, fields, Namespace
import func_task

app = Flask(__name__)
api = Api(app)

###################################################################################
#input model data

time_format_model = api.model('Model', {
    "startTime": fields.String,
    "endTime": fields.String,

})
list_model_input = api.model('ModelInput', {
    "user_a_block_slot": fields.List(fields.Nested(time_format_model)),
    "user_b_block_slot" : fields.List(fields.Nested(time_format_model))

})

list_model_confirmed_input = api.model('ModelConfirmed', {
    "user_a_block_slot": fields.List(fields.Nested(time_format_model)),
    "user_b_block_slot" : fields.List(fields.Nested(time_format_model)),
    "user_a_confirmed_meetings" : fields.List(fields.Nested(time_format_model)),
    "user_b_confirmed_meetings" :fields.List(fields.Nested(time_format_model)),
    # 'disallowed_slots' :fields.List(fields.Nested(time_format_model))

})
list_model_disallowed_input = api.model('ModelDisallowed', {
    "user_a_block_slot": fields.List(fields.Nested(time_format_model)),
    "user_b_block_slot" : fields.List(fields.Nested(time_format_model)),
    "user_a_confirmed_meetings" : fields.List(fields.Nested(time_format_model)),
    "user_b_confirmed_meetings" :fields.List(fields.Nested(time_format_model)),
    "disallowed_slots" :fields.List(fields.Nested(time_format_model))

})

######################################################################################

@api.route('/blocked_slot')
class BlockedTimeSlot(Resource):
    ''' endpoint for blocked slot and return relatively available time slot'''

    @api.expect(list_model_input)
    def post(self):
        print(api.payload)
        first_user = api.payload["user_a_block_slot"]
        second_user = api.payload["user_b_block_slot"]
        print(first_user)
        temp = func_task.blocked_slots(first_user, second_user)
        return temp

@api.route('/confirmed_slot')
class ConfirmedTimeSlot(Resource):
    ''' endpoint for confirmed input '''
    @api.expect(list_model_confirmed_input)
    def post(self):
        print(api.payload)
        first_user = api.payload["user_a_block_slot"]
        second_user = api.payload["user_b_block_slot"]
        first_user_confirmed_slot = api.payload['user_a_confirmed_meetings']
        second_user_confirmed_slot = api.payload['user_b_confirmed_meetings']
        print(first_user)
        final_data, flag = func_task.confirmed_block_slot(first_user_confirmed_slot, second_user_confirmed_slot, first_user, second_user)
        if flag:
            return {'status': ' User have same confirmed meeting time slot'}
        else:
            return final_data

@api.route('/disallowed_slot')
class DisallowedTimeSlot(Resource):
    ''' endpoint for disallowed input '''
    @api.expect(list_model_disallowed_input)
    def post(self):
        print(api.payload)
        first_user = api.payload["user_a_block_slot"]
        second_user = api.payload["user_b_block_slot"]
        first_user_confirmed_slot = api.payload['user_a_confirmed_meetings']
        second_user_confirmed_slot = api.payload['user_b_confirmed_meetings']
        disallowed_timed_slot = api.payload['disallowed_slots']
        print(first_user)
        final_data , flag = func_task.disallowed_slot(disallowed_timed_slot, first_user_confirmed_slot, second_user_confirmed_slot, first_user, second_user)
        if flag:
            return {'status': ' User have same confirmed meeting time slot'}
        else:
            return final_data

if __name__ == '__main__':
    app.run(debug=True)












'''  sample input 
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
first_uaser = [
    {
        "startTime": "2020-03-18 17:10:00",
        "endTime": "2020-03-18 17:25:00"
    },
    {
        "startTime": "2020-03-18 14:00:00",
        "endTime": "2020-03-18 14:15:00"
    }
]

second_users = [
    {
        "startTime": "2020-03-18 08:00:00",
        "endTime": "2020-03-18 08:15:00"
    },
    {
        "startTime": "2020-03-18 11:00:00",
        "endTime": "2020-03-18 11:15:00"
    }
]


first_user_confdirmed_slot = [
    {
        "startTime": "2020-03-18 12:4:00",
        "endTime": "2020-03-18 12:12:00"
    },
    {
        "startTime": "2020-03-18 15:33:00",
        "endTime": "2020-03-18 15:50:00"
    }
]
second_user_condfirmed_slot =[

    {
        "startTime": "2020-03-18 15:45:00",
        "endTime": "2020-03-18 16:00:00"
    },
    {
        "startTime": "2020-03-18 18:30:00",
        "endTime": "2020-03-18 18:45:00"
    }
]

disallowed_tijmed_slot = [
    {
        "startTime": "2020-03-18 14:18:00",
        "endTime": "2020-03-18 15:06:00"
    },
    {
        "startTime": "2020-03-18 20:30:00",
        "endTime": "2020-03-18 21:30:00"
    }
]


'''