## Demo

## Features
- generic endpoint generation
- uniformity of endpoints across channels. But each in a different class

## Operation
- Sales_reps
- leads
- Activities

## Checks
- Working only inside working window
- Not going beyond capacity (single shift per day)

# Notes
- use lead id:1 to create lead with channel info only


### Design Issues
- [ ] We require leads(atleast some leads info) on this side to be able to handle multichannel
- [ ] What happens if sth fails on a lead,, eg username does not exist. Is the slot wasted?
- [ ] Can the workflows be started from here?


### Issues
- [ ] lead score not working. Fix later...
- [ ] Picking leads (coordination with Martin)


