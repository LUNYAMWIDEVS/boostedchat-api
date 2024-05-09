from .sales_rep import SalesRep

"""
Requirements:
One lead can be contacted by multiple sales reps on multiple channels.
Each sales rep-lead communication forms a single thread.
All interactions between sales_reps and leads are saved.
A sandbox channel is used to test prompts
Sandbox sales_reps are used for testing the various channels

Simplification:
1. Each channel has a single account. That is a single sales_rep has a single whatsapp account and a single Ig account, etc
2. When scheduling, leads are read from db and the channel to be used to contact them is also read from db. Incase this is to be decided by workflow, it will need to make the changes in the db.


# For now we will duplicate the dbs.
Leads
    Lead
        username info
    LeadsInstagram
        lead igname
    LeadWhatsapps
        lead whatsappNumber
    Lead LinkedIns
        lead linkedin
    LeadSMS
        lead sms  

    LeadCommunications
        lead salesrep stage activeChannel

    LeadChannels
        list of those channels

    LeadActivities
        lead activity

    LeadMessages
        messageid lead in/out leadchannel
    LeadComments

    LeadLikes

    Log also errors and reasons for errors for all interactions...

Instagram
    Igusernames Status(changed/not available) Status1(Private) (in lists)

Whatsapp
    Numbers Status

LinkedIn
    UserNames Status


    
Lead..

    *** rq::: how to set prompts...

SalesReps...
    *** What will need to be changed here also
    *** Then get down to work.................

    *** Prove this concept with the sandboxes...


    *** prompts??? how we will get the prompts??? Keep it unchanged for now
    


    Also their channel info... Single channel per lead for now...



LeadActivities
    Activity    Type    Message     SalesRepChannel
        Channel



Each sales_rep has multiple channels

With from .sales_rep import SandBoxChannel implementation we are not able to test the various things implemented in the different channels without actually sending the messages.
So we will add sandbox field to the various sales_rep channels to testing the several implementations in the microservices


We also want different sales_reps to be able to contact the same lead on different channels.


ORD::
1. ChannelUserNames
"""