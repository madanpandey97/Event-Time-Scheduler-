# Assignment -> Event Time Scheduler
# Programmer -> Madan Pandey
# File  ->API Part

################################ Flask Packages  ################################################


from flask import Flask
from flask_restplus import Resource, Api, fields
from func_task import blocked_slots, confirmed_block_slot , disallowed_slot

##################################### Flask App #############################################

app = Flask(__name__)
api = Api(app)

################################## Input Data Model #################################################


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

##################################### Blocked Time Slot #################################################

# end point, check bottom of the page for sample input

@api.route('/blocked_slot')
class BlockedTimeSlot(Resource):
    ''' endpoint for blocked slot and return relatively available time slot
    check function blocked_slots for code understanding you can pass data in json format'''

    @api.expect(list_model_input)
    def post(self):
        data_dict = dict()

        data_dict['user_a_block_slot'] = api.payload["user_a_block_slot"]
        data_dict['user_b_block_slot'] = api.payload["user_b_block_slot"]
        temp = blocked_slots(data_dict)
        return temp

###################################### Confirmed Time Slot #################################################

@api.route('/confirmed_slot')
class ConfirmedTimeSlot(Resource):
    ''' endpoint for confirmed input check function confirmed_block_slot
     for code logic '''
    @api.expect(list_model_confirmed_input)
    def post(self):
        print(api.payload)
        data_dict = dict()

        data_dict['user_a_block_slot'] = api.payload["user_a_block_slot"]

        data_dict['user_b_block_slot'] = api.payload["user_b_block_slot"]

        data_dict['user_a_confirmed_meetings'] = api.payload['user_a_confirmed_meetings']

        data_dict['user_b_confirmed_meetings'] = api.payload['user_b_confirmed_meetings']

        final_data, flag = confirmed_block_slot(data_dict)
        if flag:
            return {'status': ' User have same confirmed meeting time slot'}
        else:
            return final_data


#################################### Disallowed Endpoint #################################################

@api.route('/disallowed_slot')
class DisallowedTimeSlot(Resource):
    ''' endpoint for disallowed input for logic part check function disallowed_slot
    for more detail '''
    @api.expect(list_model_disallowed_input)
    def post(self):
        print(api.payload)
        data_dict = dict()
        data_dict['user_a_block_slot'] = api.payload["user_a_block_slot"]

        data_dict['user_b_block_slot'] = api.payload["user_b_block_slot"]

        data_dict['user_a_confirmed_meetings'] = api.payload['user_a_confirmed_meetings']

        data_dict['user_b_confirmed_meetings'] = api.payload['user_b_confirmed_meetings']

        data_dict['disallowed_slots'] = api.payload['disallowed_slots']

        final_data , flag = disallowed_slot(data_dict)
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

'''

############################ End File ########################################################