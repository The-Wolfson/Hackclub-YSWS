# Hackclub Events Slackbot
A Slack app to keep you up to date with Hackclub's events. hackathons, and YSWS programs.
`@Hackclub Events` (`<U094ELS98UC>`).

## Usage
### Commands


#### `/ysws` 
##### Arguments
###### `filter:`
- `all`
- `active` *(default)*
- `draft`
- `ended`
###### `sort:`
- `alphabetical`
- `category`
- `date` *(default)*
- `status`
##### Example
`/ysws filter:ended sort:alphabetical` = List of ended YSWS programs sorted in alphabetical order. 


#### `/events` 
##### Arguments
###### `filter:`
- `all`
- `ended`
- `upcoming` *(default)*
###### `sort:`
- `alphabetical`
- `date` *(default)*
###### `type:`
- `all` *(default)*
- `event`
- `ama`
##### Example
`/events filter:all sort:alphabetical type:ama` = List of all Hackclub AMAs sorted in alphabetical order. 


#### `/hackathons` 
##### Arguments
###### `filter:`
- `all`
- `active` *(default)*
- `upcoming`
- `ended`
###### `sort:`
- `alphabetical`
- `modality`
- `date` *(default)*
###### `modality:`
- `all` *(default)*
- `online`
- `in-person`
- `hybrid`
##### Example
`/hackathons filter:upcoming sort:alphabetical modality:online` = List of upcoming online hackathons sorted in alphabetical order. 
